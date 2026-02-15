# AI-Based Patient Support Assistant - Team NIGHTRIDERS

**Team Name**: NIGHTRIDERS  
**Team Leader**: B. Sai Pranav

---

## 🎯 Problem Statement Alignment
This solution is designed to improve **efficiency, understanding, and support** within the healthcare ecosystem...
- **Patient Education**: Simplification of complex medical terms and lab reports.
- **Care Navigation**: Automated appointment scheduling and follow-up guidance.
- **Decision Support**: AI-powered symptom analysis with risk scoring.

> [!IMPORTANT]
> **Data Compliance**: This system uses **synthetic data only** for all testing and demonstration purposes. No real patient data is stored.

## 🛡️ Ethical AI & Responsibility
- **Prominent Disclaimers**: Every AI interaction includes a medical disclaimer.
- **Transparency**: Limitations of AI-driven analysis are clearly stated in [ETHICAL_AI_COMPLIANCE.md](./ETHICAL_AI_COMPLIANCE.md).
- **Workflow Support**: Focused on reducing the burden on healthcare professionals by empowering patients with accurate, verified information.

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
