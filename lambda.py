import json
import logging
import os
import boto3
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "dynamo-smart")
SNS_TOPIC_ARN = os.environ.get(
    "SNS_TOPIC_ARN",
    "arn:aws:sns:us-east-1:302186542112:smart-sns"
)

dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    failures = []

    for record in event.get("Records", []):
        message_id = record.get("messageId", "unknown")

        try:
            body = json.loads(record["body"])

            student_id = str(body["student_id"])
            student_name = body.get("name") or body.get("student_name")

            if not student_name:
                raise ValueError("Student name is missing from SQS message")

            course = body.get("course", "Not specified")
            timestamp = datetime.now(timezone.utc).isoformat()

            # Save student details to DynamoDB
            item = {
                "student_id": student_id,
                "student_name": student_name,
                "course": course,
                "created_at": timestamp
            }

            # Save optional form fields if provided
            for field in ["email", "phone", "date_of_birth", "city", "address"]:
                if body.get(field):
                    item[field] = str(body[field])

            table.put_item(Item=item)

            # Publish notification to SNS
            notification = {
                "student_id": student_id,
                "student_name": student_name,
                "email": body.get("email", ""),
                "course": course,
                "action": "STUDENT_REGISTERED",
                "created_at": timestamp
            }

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Smart College - New Student Registration",
                Message=json.dumps(notification, indent=2)
            )

            logger.info("Processed SQS message: %s", message_id)

        except Exception:
            logger.exception(
                "Failed to process SQS message: %s", message_id
            )
            failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": failures}

