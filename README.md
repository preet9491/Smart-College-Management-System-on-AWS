<<<<<<< HEAD
# Smart-College-Management-System-on-AWS
AWS-based student registration system using ECS, SQS, Lambda, DynamoDB and SNS.

## Project Overview

The Smart College Management System is a cloud-based student registration application built using AWS services. It accepts student registration details through a web form, processes registration messages asynchronously, stores student records in DynamoDB, and sends notifications through Amazon SNS.

This project demonstrates practical knowledge of AWS networking, containerization, application deployment, serverless processing, database services, and cloud security.

## Architecture

Student Registration Form  
↓  
Application hosted on Amazon ECS / AWS Fargate  
↓  
Amazon SQS  
↓  
AWS Lambda  
↓  
Amazon DynamoDB — student records  
Amazon SNS — email notifications

Additional infrastructure includes Amazon VPC, public and private subnets, Internet Gateway, NAT Gateway, Amazon ECR, Application Load Balancer, IAM roles.

## AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon VPC | Provides isolated cloud networking |
| Public and Private Subnets | Organize resources across the network |
| Internet Gateway | Provides internet connectivity for public resources |
| NAT Gateway | Allows outbound internet access from private subnets when configured |
| Amazon EC2 | Provides cloud computing infrastructure where required |
| Amazon ECR | Stores Docker container images |
| Amazon ECS / AWS Fargate | Runs the containerized web application |
| Application Load Balancer | Routes incoming HTTP requests to the application |
| Amazon SQS | Queues registration messages for processing |
| AWS Lambda | Processes messages from SQS |
| Amazon DynamoDB | Stores student registration records |
| Amazon SNS | Sends registration notification emails |
| AWS IAM | Manages permissions for AWS resources |

## Technologies

- Python
- Flask
- Docker
- AWS ECS / Fargate
- Amazon ECR
- Amazon SQS
- AWS Lambda
- Amazon DynamoDB
- Amazon SNS
- AWS VPC, Security Groups and IAM

## Application Workflow

1. A student submits the registration form.
2. The Flask application sends the registration message to Amazon SQS.
3. AWS Lambda receives and processes the queued message.
4. Student details are stored in DynamoDB.
5. Amazon SNS publishes a registration notification.

## Current Implementation Status

- [x] Student registration web application
- [x] Docker image creation
- [x] Image repository in Amazon ECR
- [x] Application deployment on ECS
- [x] Application Load Balancer configuration
- [x] SQS message queue integration
- [x] Lambda processing of SQS messages
- [x] Student record storage in DynamoDB
- [x] SNS notification integration

## Learning Outcomes

- Building a containerized Python web application
- Deploying applications on AWS ECS
- Using Amazon ECR for container image management
- Configuring VPCs, subnets and security groups
- Implementing asynchronous processing with SQS and Lambda
- Storing application data in DynamoDB
- Configuring SNS notifications and IAM permissions

## Future Improvements

- Integrate RDS/MySQL into the registration workflow.
- Store registration documents or JSON records in S3.
- Improve monitoring and logging with Amazon CloudWatch.
- Add stronger application validation and secure configuration.
- Automate deployment using a CI/CD pipeline.


=======
# Smart College Registration Form

## AWS flow
Browser -> ALB :80 -> ECS Flask :5000 -> SQS `smart-sqs` -> Lambda -> DynamoDB `dynamo-smart`; Lambda optionally publishes to SNS `smart-sns`.

## Files
- `app.py`: form route, validation, SQS send, `/health` retained for ALB health checks
- `templates/register.html`: registration form
- `templates/success.html`: confirmation page
- `lambda_function.py`: SQS -> DynamoDB -> SNS processing example
- `Dockerfile`: packages templates with the Flask app

## ECS configuration
In the ECS task definition container environment, set:
- `AWS_REGION=ap-south-1`
- `SQS_QUEUE_URL=<copy exact Queue URL for smart-sqs>`

Do not hard-code AWS credentials. The ECS **task role** needs `sqs:SendMessage` on the `smart-sqs` queue ARN. The execution role is for pulling ECR images and logs, not application AWS API calls.

For Lambda, set environment variables:
- `DYNAMODB_TABLE=dynamo-smart`
- `SNS_TOPIC_ARN=<exact ARN of smart-sns>`

The DynamoDB table must have partition key `student_id` (String). Lambda role needs `dynamodb:PutItem` on `dynamo-smart` and `sns:Publish` on `smart-sns`. The Lambda SQS trigger also needs permission to read/delete messages. Confirm an SNS email subscription if you want email alerts.

## Local run
Install dependencies with `pip install -r requirements.txt`. Set `AWS_REGION` and `SQS_QUEUE_URL` in your shell and configure AWS credentials securely with an AWS profile. Then run `python app.py` and open `http://127.0.0.1:5000`. Never commit AWS credentials.

## Build and push image
From this folder:
```bash
docker build -t smart-college-app .
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 080949906593.dkr.ecr.ap-south-1.amazonaws.com
docker tag smart-college-app:latest 080949906593.dkr.ecr.ap-south-1.amazonaws.com/smart-college-app:latest
docker push 080949906593.dkr.ecr.ap-south-1.amazonaws.com/smart-college-app:latest
```

## Deploy to ECS
1. ECS -> Task definitions -> `smart-college-task` -> Create new revision.
2. Keep container name `smart-college-container`, port 5000, execution role `smart-college-ecs-execution-role-v2`, task role `smart-college-ecs-task-role`.
3. Add/update `AWS_REGION` and `SQS_QUEUE_URL` on the container definition. Save revision.
4. ECS -> Clusters -> `smart-college-cluster` -> Services -> `smart-college-service` -> Update. Select the new revision and force new deployment if offered.
5. Wait for service deployment and task to reach RUNNING.
6. Keep ALB listener HTTP 80 -> target group IP:5000, health path `/health`. Open the ALB DNS name; `/` should show the form.

## End-to-end test
Submit a test record. Check Lambda CloudWatch logs, then DynamoDB `dynamo-smart` for the generated `STU-...` record. Check SNS subscription/delivery if enabled. SQS messages may disappear quickly because Lambda consumes them.

## Notes
This version sends form data through SQS to DynamoDB. It does not yet store data in RDS MySQL. Keep RDS private. Use dummy data for testing because phone, email and address are personal information.
>>>>>>> df8f905 (Upload project files)
