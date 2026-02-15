# AI-Based Patient Support Assistant

A production-ready intelligent healthcare guidance platform built for the Kiro style hackathon.

## 🚀 Key Features

- **AI Chat Assistant**: Real-time medical guidance using OpenAI GPT.
- **Symptom Checker**: TensorFlow-powered condition prediction and risk analysis.
- **Lab Report Analysis**: OCR-based extraction and simplification of medical reports using AWS Textract.
- **Medication Reminders**: Subscription-based tracking and adherence monitoring.
- **Care Navigation**: Appointment scheduling and follow-up guidance.
- **Secure Auth**: JWT-based authentication with encrypted patient history.

## 🛠 Tech Stack

- **Frontend**: Flutter (Cross-platform, premium design system)
- **Backend**: Python Flask (REST API)
- **Database**: PostgreSQL (Structured) + MongoDB (Unstructured)
- **AI**: OpenAI, TensorFlow, AWS Textract
- **DevOps**: Docker, AWS (ECS, RDS, S3)

## 📦 Getting Started

### Prerequisites
- Docker & Docker Compose
- Flutter SDK (to run the mobile app)
- Python 3.9+ (for local backend development)

### Local Development (Backend)
1. Clone the repository.
2. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_key
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_key
   ```
3. Run the orchestration:
   ```bash
   docker-compose up --build
   ```

### Running the App (Frontend)
1. Navigate to `frontend/`.
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app:
   ```bash
   flutter run
   ```

## 🛡 Security & Compliance
- Full data encryption at rest and in transit.
- Medical disclaimer included in all AI interactions.
- Audit logging for all sensitive user actions.

## 📄 License
MIT License. Created for hackathon purposes.
