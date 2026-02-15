# AWS Deployment Architecture

This document describes the production deployment architecture for the AI Patient Assistant.

## Components & Services

### 1. Frontend (Flutter)
- **Web/Desktop**: Hosted on **AWS Amplify** or S3 + CloudFront.
- **Mobile**: Distributed via TestFlight/Google Play Store.

### 2. Backend (Flask API)
- **Containerization**: Use **Amazon ECS (Elastic Container Service)** with Fargate.
- **Load Balancing**: **Application Load Balancer (ALB)** for traffic distribution and SSL termination.
- **CI/CD**: **AWS CodePipeline** and **CodeBuild**.

### 3. Databases
- **SQL**: **Amazon RDS** (PostgreSQL) for structured patient data.
- **NoSQL**: **MongoDB Atlas** (AWS Integrated) for knowledge base and chat logs.

### 4. AI Services
- **OCR**: **AWS Textract** for lab report extraction.
- **Models**: **Amazon SageMaker** for custom TensorFlow symptom models.
- **LLM**: Integrated via OpenAI API (proxied through Lambda for security if needed).

## Security & Compliance
- **VPC Implementation**: All services inside a Private VPC.
- **Data Encryption**: **AWS KMS** for encryption at rest (S3, RDS, EBS).
- **Audit Logging**: **CloudWatch** and **CloudTrail**.
- **Compliance**: Adhere to HIPAA/GDPR best practices by never storing PII in clear text.
