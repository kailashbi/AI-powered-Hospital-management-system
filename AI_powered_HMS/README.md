# 🏥 KAIre Health - AI-Powered Hospital Management System & Real-Time Telemetry Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue.svg)](https://vitejs.dev/)
[![Flask](https://img.shields.io/badge/Backend-Flask%20REST-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL%20%2F%20Supabase-orange.svg)](https://www.mysql.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML%20Engine-Scikit--Learn%20%2B%20XGBoost-red.svg)](https://scikit-learn.org/)
[![Kafka](https://img.shields.io/badge/Event%20Streaming-Apache%20Kafka-black.svg?logo=apachekafka)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Orchestration-Docker%20Compose-2496ED.svg?logo=docker)](https://www.docker.com/)

**KAIre Health** is a production-ready, full-stack Hospital Management System (HMS) combining clinical electronic health records (EHR), multi-role portals (Doctor, Nurse, Patient, Administrator), an integrated Machine Learning diagnostic pipeline, and an **Apache Kafka Event Streaming Engine** for real-time vitals telemetry and emergency triage alerts.

---

## 🌟 Key System Features

### 🧠 1. Machine Learning Diagnostic Engine
- **Heart Disease Classifier**: `RandomForestClassifier` (180 trees) trained on 14 cardiovascular features (**Accuracy: 85.36%, ROC-AUC: 0.9134**).
- **Type-2 Diabetes Predictor**: `LogisticRegression` with `StandardScaler` on Pima diagnostic biomarkers (**Accuracy: 88.61%, ROC-AUC: 0.9615**).
- **Stroke Risk Stratifier**: `XGBClassifier` with `OneHotEncoder` categorical pipelines for cerebrovascular risk (**Accuracy: 95.14%**).
- **Explainable AI (XAI)**: Live feature importance percentages (SHAP weights) explaining why a patient was flagged for high risk.
- **Model Versioning & EHR Persistence**: Tracks model version tags (`v1.2.0-rf-xgboost`) and physician review statuses (`Confirmed`, `Pending Review`) in the relational database.

### 👨‍⚕️ 2. Doctor Portal & Clinical Workflow
- **Physician Dashboard**: Today's appointments, assigned patients, and critical risk alerts.
- **Patient EHR Directory**: Interactive patient profiles, medical history timeline, and vitals telemetry charts.
- **Interactive AI Diagnostics**: Real-time clinical input sliders with live risk probability gauge and SHAP weight explanations.
- **Care Plans & Reminders**: Send real-time appointment reminders and customized health care plans directly to patient portals.

### 👩‍⚕️ 3. Nurse Triage Station
- **Ward Triage Dashboard**: Live telemetry records across department beds.
- **Vitals Recording Form**: Temperature, Blood Pressure (Systolic/Diastolic), Heart Rate, SpO2, Blood Glucose, Weight, and clinical notes.
- **Automated Emergency Dispatch**: Immediate alert generation when physiological vitals exceed safe thresholds (Systolic ≥ 160, HR ≥ 120, SpO2 ≤ 90%).
- **Shift & Ward Management**: Duty status toggles, assigned ward/bed units, and shift schedules.

### 🧑‍🤝‍🧑 4. Patient Portal
- **Personalized Health Dashboard**: Upcoming consultations, latest vitals summary, and AI risk scores.
- **Appointment Booking**: Online scheduling with doctors across various departments.
- **EHR & Prescriptions Timeline**: Chronological medical history, diagnostic reports, and physician prescriptions.
- **AI Explanations**: Accessible view of AI health risk predictions and physician treatment recommendations.

### 🛡️ 5. Administrator Governance HQ
- **Hospital Operations Analytics**: Bed occupancy rate, department patient volume, and doctor-to-patient staff ratios.
- **User Management**: Complete CRUD operations, account activation/deactivation, and role assignment (Doctor, Nurse, Patient, Admin).
- **HIPAA Audit Log**: Immutable audit trails recording every system event, diagnostic run, login, and prescription dispatch.
- **Kafka Live Stream Dashboard**: Dedicated real-time topic telemetry monitor (`/admin/kafka-stream`) displaying event payloads, message counts, broker connectivity status, and a manual event publishing test bench.

### ⚡ 6. Apache Kafka Event Streaming Engine
- **6 Dedicated Event Topics**: Real-time vitals, emergency triage alerts, ML prediction completions, appointment state changes, care plan notifications, and HIPAA audit trails.
- **Graceful In-Memory Fallback**: Automatically falls back to an in-memory event bus if Kafka brokers are offline, guaranteeing zero API downtime.

### ⚡ 7. 1-Click Quick Demo Persona Switcher
- Instantly switch between **Doctor**, **Nurse**, **Patient**, and **Admin** personas directly from the login page or top navigation bar pill.

---

## 🏗️ System Architecture & Code Base Structure

```
KAIre Health/
├── client/                     # React 18 + Vite Frontend (Glassmorphism UI)
│   ├── src/
│   │   ├── components/         # StatCards, Modals, Badges, DataTable, VitalsChart, RiskGauge
│   │   ├── context/            # AuthContext (JWT Auth + Quick Role Switcher)
│   │   ├── layouts/            # AdminLayout, DoctorLayout, NurseLayout, PatientLayout
│   │   ├── pages/              # Auth, Admin, Doctor, Nurse, Patient, & Kafka Monitor pages
│   │   ├── services/           # Axios API services (Auth, Admin, Doctor, Nurse, Patient, Prediction)
│   │   ├── routes/             # Protected routes with Role-Based Access Control (RBAC)
│   │   ├── App.jsx & main.jsx
│   │   └── index.css           # Modern Healthcare Design System & HSL token system
│   ├── package.json
│   └── vite.config.js
│
├── server/                     # Flask RESTful API & Machine Learning Backend
│   ├── app/
│   │   ├── config/             # Environment configuration (MySQL / SQLite / Supabase PostgreSQL)
│   │   ├── middleware/         # JWT Authentication & Global Error Handlers
│   │   ├── models/             # SQLAlchemy ORM (User, Doctor, Nurse, Patient, Vital, Prediction, etc.)
│   │   ├── routes/             # REST Blueprints (Auth, Admin, Doctor, Nurse, Patient, Predictions, Kafka)
│   │   ├── services/           # PredictionService, KafkaService, NotificationService
│   │   └── utils/              # Audit logger, Input validators, Decorators
│   ├── run.py                  # Server entrypoint
│   └── requirements.txt        # Python dependency list
│
├── ml/                         # Machine Learning Diagnostic Engine
│   ├── datasets/               # heart.csv, diabetes.csv, stroke.csv
│   ├── training/               # train_heart.py, train_diabetes.py, train_stroke.py
│   ├── models/                 # Pre-trained artifacts (.pkl)
│   ├── evaluation/             # Metrics text and JSON reports
│   ├── inference/
│   │   └── predictor.py        # Unified DiseasePredictor with explainable SHAP weights
│   ├── train_all.py            # Automated master training runner
│   └── generate_datasets.py    # Benchmark dataset generator
│
├── database/
│   ├── schema.sql              # Relational MySQL / PostgreSQL Schema
│   └── seed.sql                # Realistic Hospital Demo Dataset
│
├── docker/
│   ├── client.Dockerfile       # Multi-stage Node + Nginx Container
│   └── server.Dockerfile       # Python 3.11 + ML Environment Container
├── docker-compose.yml          # Full Orchestration (Client, Server, MySQL, Kafka, Zookeeper)
├── .env & .env.example         # Environment variables template
├── ml_results.txt              # Master ML performance benchmark results
└── README.md                   # Main Documentation
```

### Data Flow Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["Client Layer (React + Vite)"]
        UI["React Single Page Application"]
        KafkaUI["Admin Kafka Live Stream Monitor"]
    end

    subgraph ServerLayer ["Backend REST API (Flask)"]
        API["Flask REST Controller"]
        Auth["JWT Auth & Middleware"]
        ML["DiseasePredictor (Scikit-Learn / XGBoost)"]
        KafkaService["KAIreKafkaService (Producer & Consumer)"]
    end

    subgraph Persistence ["Database & Storage"]
        DB[("MySQL / PostgreSQL / Supabase")]
    end

    subgraph Streaming ["Event Streaming Infrastructure"]
        KafkaBroker["Apache Kafka Broker / Upstash Cloud Kafka"]
        T1["kaire-vitals-stream"]
        T2["kaire-emergency-alerts"]
        T3["kaire-ml-predictions"]
        T4["kaire-appointments"]
        T5["kaire-notifications"]
        T6["kaire-audit-logs"]
    end

    UI -->|HTTPS JSON REST| API
    API -->|Authenticate & Validate| Auth
    Auth -->|Execute Queries| DB
    API -->|Run AI Inference| ML
    API -->|Publish Events| KafkaService
    KafkaService -->|Stream Events| KafkaBroker
    KafkaBroker --> T1 & T2 & T3 & T4 & T5 & T6
    KafkaService -->|Background Consume| DB
    KafkaService -->|Fetch Telemetry| KafkaUI
```

---

## 🧠 Machine Learning Engine & Benchmark Results

### 1. Kaggle Datasets Used
- **Heart Disease**: [Kaggle Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith82/heart-disease-dataset) $\rightarrow$ `ml/datasets/heart.csv`
- **Type-2 Diabetes**: [Kaggle Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database) $\rightarrow$ `ml/datasets/diabetes.csv`
- **Stroke Risk**: [Kaggle Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) $\rightarrow$ `ml/datasets/stroke.csv`

### 2. Performance Summary Table

| Disease Model | Algorithm Used | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Serialized Artifact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **🫀 Heart Disease** | `RandomForestClassifier` (180 trees) | **85.36%** | 85.96% | 82.46% | 84.18% | **0.9134** | `ml/models/heart_model.pkl` |
| **🩸 Type-2 Diabetes** | `LogisticRegression` + `StandardScaler` | **88.61%** | 41.89% | 87.76% | 56.71% | **0.9615** | `ml/models/diabetes_model.pkl` |
| **🧠 Stroke Risk** | `XGBClassifier` + `ColumnTransformer` | **95.14%** | 33.33% | 0.21% | 0.41% | **0.5009** | `ml/models/stroke_model.pkl` |

### 3. Run Training Locally
```bash
python ml/train_all.py
```
This trains all 3 models, serializes binary `.pkl` artifacts into `ml/models/`, and generates text performance metric reports in `ml/evaluation/` and `ml_results.txt`.

---

## ⚡ Apache Kafka Event Topics & Schemas

KAIre Health incorporates 6 dedicated Apache Kafka topics:

| Topic Name | Trigger Event | Primary Purpose | Priority |
| :--- | :--- | :--- | :--- |
| `kaire-vitals-stream` | Nurse records vitals | Real-time streaming of physiological vitals | High |
| `kaire-emergency-alerts` | Systolic ≥ 160, HR ≥ 120, SpO2 ≤ 90% | Critical alert dispatch for emergency triage | Critical |
| `kaire-ml-predictions` | Doctor runs ML disease prediction | AI diagnostic assessment completion events | High |
| `kaire-appointments` | Patient books or doctor updates appointment | Appointment state transition updates | Medium |
| `kaire-notifications` | Doctor publishes care plan | System and patient care alerts | Medium |
| `kaire-audit-logs` | User action / record modification | Immutable HIPAA audit logging | Low |

### Payload Example (`kaire-vitals-stream`)
```json
{
  "event_id": "evt_08fa213e",
  "event_type": "VITAL_RECORDED",
  "topic": "kaire-vitals-stream",
  "timestamp": "2026-09-14T02:15:00Z",
  "payload": {
    "vital_id": 12,
    "patient_id": 1,
    "recorded_by_user_id": 5,
    "temperature": 101.4,
    "blood_pressure_systolic": 165,
    "blood_pressure_diastolic": 105,
    "heart_rate": 124,
    "spo2": 92,
    "blood_glucose": 145.0,
    "notes": "Patient reporting severe chest discomfort"
  }
}
```

---

## 🔑 Demo Login Credentials

You can log in with any of the following pre-configured persona accounts:

| Role | Email | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| 🛡️ **Admin** | `admin@kairehealth.com` | `password123` | Hospital HQ, Staff Roster, User CRUD, Audit Logs, Kafka Live Stream |
| 👨‍⚕️ **Doctor** | `dr.sarah@kairehealth.com` | `password123` | Patient EHR, AI Disease Predictor, Prescriptions, Appointments |
| 👩‍⚕️ **Nurse** | `nurse.emily@kairehealth.com` | `password123` | Record Vitals (Streams to Kafka), Bed & Ward Management |
| 🧑‍🤝‍🧑 **Patient** | `john.doe@gmail.com` | `password123` | Book Appointments, View AI Risk Results, EHR Prescriptions |

> 💡 **Quick Test Flow**:
> 1. Log in as **Nurse** (`nurse.emily@kairehealth.com` / `password123`).
> 2. Go to **Record Vitals** and submit critical vitals (e.g., BP `165/105`, HR `124`).
> 3. Log out and log in as **Admin** (`admin@kairehealth.com` / `password123`).
> 4. Go to **Kafka Event Stream** (`/admin/kafka-stream`).
> 5. View live `VITAL_RECORDED` and `CRITICAL_VITALS_ALERT` topic messages!

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js**: v18+ or v20+
- **Python**: 3.10+ or 3.11+
- **MySQL**: 8.0+ *(Optional: SQLite is enabled by default for zero-config local testing)*

---

### Option 1: Standalone Local Setup

#### 1. Setup Backend API & Machine Learning Engine
```bash
# Navigate to backend directory
cd server
pip install -r requirements.txt

# Run ML dataset generation & model training (Optional - pre-trained models included)
cd ..
python ml/train_all.py

# Run Flask REST API Server (Runs on http://localhost:5000)
python server/run.py
```

#### 2. Setup Frontend Client
```bash
# In a new terminal window:
cd client
npm install
npm run dev
# React Client runs on http://localhost:3000
```

---

### Option 2: Docker Compose (Recommended)

Docker Compose orchestrates 5 containerized services:
- `kaire_health_client` (Nginx + React SPA on port `3000`)
- `kaire_health_server` (Python 3.11 + Flask API + ML on port `5000`)
- `kaire_health_mysql` (MySQL 8.0 Database on port `3307`)
- `kaire_health_kafka` (Apache Kafka Broker on port `9092`)
- `kaire_health_zookeeper` (Zookeeper Coordination on port `2181`)

```bash
# Build and launch all 5 services in detached mode:
docker-compose up --build -d
```

#### Verification Endpoints
- **React Frontend**: `http://localhost:3000`
- **Swagger OpenAPI Docs**: `http://localhost:5000/apidocs`
- **Backend API Health**: `curl http://localhost:5000/api/health`
- **Kafka Status Endpoint**: `curl http://localhost:5000/api/kafka/status`
- **Kafka Admin Live Monitor**: `http://localhost:3000/admin/kafka-stream`

---

## 🌐 Production Cloud Deployment Guide

| Component | Cloud Platform | Build / Start Command | Environment Variables |
| :--- | :--- | :--- | :--- |
| **Frontend** | **Vercel** | Build: `npm run build`<br>Output: `dist` | `VITE_API_URL=https://your-api-url.onrender.com/api` |
| **Backend & ML** | **Render** | Build: `pip install -r server/requirements.txt`<br>Start: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 server.run:app` | `FLASK_ENV=production`<br>`DATABASE_URL=postgresql://...`<br>`ENABLE_KAFKA=true` |
| **Database** | **Supabase** | Managed PostgreSQL Instance | `DATABASE_URL=postgresql://postgres.xxx:yyy@...` |
| **Kafka Cluster** | **Upstash Kafka** | Serverless SASL_SSL Kafka | `KAFKA_BOOTSTRAP_SERVERS=...`<br>`KAFKA_SECURITY_PROTOCOL=SASL_SSL`<br>`KAFKA_SASL_MECHANISM=SCRAM-SHA-250` |

---

## 🛡️ Security & HIPAA Compliance Features

- **Authentication**: Stateless JSON Web Tokens (JWT) with configurable expiration (`JWT_SECRET_KEY`).
- **Password Security**: Irreversible `bcrypt` hashing with salt rounds for all user accounts.
- **Role-Based Access Control (RBAC)**: Strict role checking across endpoints (`Admin`, `Doctor`, `Nurse`, `Patient`).
- **Audit Trails**: Immutable HIPAA log table tracking timestamp, user ID, IP address, action type, and JSON metadata.
- **Environment Isolation**: Zero hardcoded credentials; all secrets stored in `.env`.

---

## 📄 License

This project is open-source and licensed under the **[MIT License](LICENSE)**.
