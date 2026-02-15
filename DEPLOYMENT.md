# 🚀 DEPLOYMENT GUIDE - Team NIGHTRIDERS

## Quick Start (For Hackathon Judges)

This guide will get the AI Patient Support Assistant running locally in under 5 minutes.

### Prerequisites
- Docker & Docker Compose
- Flutter SDK (for frontend)

### Step 1: Clone Repository
```bash
git clone https://github.com/PuneethPeela/h2s.git
cd h2s
```

### Step 2: Start Backend Services
```bash
# Start PostgreSQL, MongoDB, and Flask API
docker-compose up -d

# Wait 10 seconds for services to initialize
sleep 10
```

### Step 3: Initialize Database
```bash
# Create database tables
docker exec -it ai_patient_assistant-backend-1 python3 -c "from app import app; from extensions import db; app.app_context().push(); db.create_all(); print('✅ Database initialized!')"
```

### Step 4: Verify Backend
```bash
curl http://localhost:5000/health
# Expected: {"status": "healthy", "service": "AI Patient Assistant API"}
```

### Step 5: Run Frontend (Optional)
```bash
cd frontend
flutter pub get
flutter run -d web-server --web-port=8080
```

---

## 🧪 Test the APIs

### 1. Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@nightriders.com","password":"secure123","full_name":"Demo User"}'
```

### 2. Login & Get JWT Token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@nightriders.com","password":"secure123"}'
```

### 3. Test Real-Time Features
Use the JWT token from step 2 in the Authorization header to test:

#### Medication Reminders
```bash
curl -X GET http://localhost:5000/api/meds/reminders \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

#### Appointments
```bash
curl -X GET http://localhost:5000/api/appointments/ \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

#### AI Chat
```bash
curl -X POST http://localhost:5000/api/ai/chat \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is diabetes?"}'
```

---

## 📁 Key Files for Review

- `/backend/routes/` - All REST API endpoints
- `/frontend/lib/features/` - Flutter UI modules
- `/backend/data/synthetic_symptoms.json` - 100% synthetic dataset
- `/ETHICAL_AI_COMPLIANCE.md` - Responsibility documentation
- `/README.md` - Project overview

---

## 🔐 Security Features Verified

✅ **Email Validation**: Try registering with `bad-email` - should fail  
✅ **JWT Protection**: Try accessing` /api/meds/reminders` without token - should fail  
✅ **Synthetic Data**: Check `/backend/data/` - only synthetic datasets used

---

## 🏆 Hackathon Compliance

✅ **Team Name**: NIGHTRIDERS  
✅ **Leader**: B. Sai Pranav  
✅ **Category**: AI for Healthcare & Life Sciences  
✅ **Synthetic Data**: 100% compliance  
✅ **Medical Disclaimers**: Present in all AI responses  
✅ **Real-Time Features**: All modules (Chat, Meds, Lab, Care) are fully integrated

---

**For detailed verification results, see `/walkthrough.md`**
