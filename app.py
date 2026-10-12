import json, os, re, uuid
from datetime import date
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, flash, render_template, request

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")
REGION = os.environ.get("AWS_REGION", "ap-south-1")
QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")
sqs = boto3.client("sqs", region_name=REGION) if QUEUE_URL else None
COURSES = ["B.Tech", "BCA", "MCA", "BBA", "MBA", "B.Sc", "B.Com", "Other"]

@app.get("/health")
def health():
    return {"status": "healthy"}, 200

@app.get("/")
def home():
    return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form={})

@app.post("/register")
def register():
    student = {
        "student_id": "STU-" + uuid.uuid4().hex[:10].upper(),
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "phone": request.form.get("phone", "").strip(),
        "course": request.form.get("course", "").strip(),
        "date_of_birth": request.form.get("date_of_birth", "").strip(),
        "city": request.form.get("city", "").strip(),
        "address": request.form.get("address", "").strip()
    }
    required = ["name", "email", "phone", "course", "date_of_birth", "city"]
    if any(not student[k] for k in required):
        flash("Please complete all required fields.", "error")
        return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form=student), 400
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", student["email"]):
        flash("Enter a valid email address.", "error")
        return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form=student), 400
    if student["course"] not in COURSES:
        flash("Choose a valid course.", "error")
        return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form=student), 400
    if not QUEUE_URL:
        app.logger.error("SQS_QUEUE_URL is not configured")
        flash("Registration is temporarily unavailable. Please try again later.", "error")
        return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form=student), 500
    try:
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(student))
    except (BotoCoreError, ClientError):
        app.logger.exception("SQS send_message failed")
        flash("We could not submit your registration. Please try again.", "error")
        return render_template("register.html", courses=COURSES, today=date.today().isoformat(), form=student), 502
    return render_template("success.html", student=student), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
