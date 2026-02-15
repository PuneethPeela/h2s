# System Design Document

## 1. Architecture Overview
The system follows a microservices-ready monolithic architecture.

- **Frontend**: Flutter-based mobile/web app using a Clean Architecture pattern (Features -> Core -> Widgets).
- **Backend**: Python Flask REST API orchestrating AI services and data layers.
- **AI Layer**: OpenAI GPT-4 for conversation, TensorFlow for condition prediction, and AWS Textract for OCR.
- **Data Layer**: Hybrid storage using PostgreSQL for relational data and MongoDB for medical knowledge and chat logs.

## 2. Database Design

### 2.1 PostgreSQL (Relational)
- `users`: Authentication and core profile.
- `medical_history`: Past conditions and status.
- `prescriptions`: Medication details.
- `reminders`: Schedule and adherence tracking.
- `appointments`: Care navigation data.

### 2.2 MongoDB (Unstructured)
- `medical_knowledge`: Symptom-disease mapping and lifestyle advice.
- `chat_history`: Threaded messages with context.
- `lab_reports`: OCR metadata and simplified summaries.

## 3. Component Interaction

### 3.1 AI Chat Flow
1. User sends message via Flutter UI.
2. Flask API retrieves session context from MongoDB.
3. OpenAI GPT-4 processes input with health-specific system prompt.
4. Response is streamed/sent back and saved to MongoDB.

### 3.2 Lab Analysis Flow
1. User uploads PDF to S3 (via Flask).
2. Flask triggers AWS Textract for OCR.
3. Raw data is processed by GPT-4 for simplification.
4. Resulting summary is stored in MongoDB and displayed to user.

## 4. Infrastructure Design
- **Local**: `docker-compose` for PG, Mongo, and Flask.
- **Production**:
  - AWS ECS (Fargate) for API.
  - AWS RDS (PostgreSQL).
  - MongoDB Atlas.
  - AWS S3 for storage.
  - CloudFront for frontend distribution.
