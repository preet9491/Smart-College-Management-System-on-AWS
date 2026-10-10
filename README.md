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


