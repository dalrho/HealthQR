# HealthQR: City-Wide Emergency Medical Response System

HealthQR is a secure, decentralized digital health platform designed to provide emergency responders with instant access to life-saving medical data. By bridging the gap between citizens and medics through encrypted QR technology, HealthQR aims to reduce response times and improve patient outcomes in critical situations.

---

## 🚀 Key Features

- **Citizen Portal**  
  Simple registration for residents to input vitals, allergies, and emergency contacts.

- **Instant QR Generation**  
  Generates a unique, downloadable HealthQR code for physical or digital storage.

- **Secure Medic Scanner**  
  A protected portal for authorized medical personnel with real-time QR decoding.

- **JWT Security**  
  Role-Based Access Control (RBAC) ensuring only verified medics can access sensitive health records.

- **Session Protection**  
  Automatic session clearing and route guarding to prevent unauthorized data exposure.

- **Audit-Ready Architecture**  
  Backend designed with logging and emergency override capabilities.

---

## 🛠 Tech Stack

- **Frontend:** Next.js (React), Tailwind CSS, `html5-qrcode`  
- **Backend:** FastAPI (Python), SQLAlchemy  
- **Database:** PostgreSQL  
- **Deployment:** Docker & Docker Compose  

---

## 📦 Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthqr.git
cd healthqr
```      

### 2. Configure Environment

The system is pre-configured for local development.
Verify that docker-compose.yml reflects your desired environment variables, especially:

- Database credentials
- Backend secrets (JWT, etc.)

### 3. Launch the System

Execute the command to build and start all services (Database, Backend, Frontend):

```bash
docker compose up --build -d
```

### 4. Seed the Initial Medic Account

To access the Medic Portal, you must create an authorized medic user inside the secure database.

Run the following command while the containers are running:

```bash
docker exec -it healthqr_backend python seed_medic.py
```

**Default Credentials (Development Only):**

- **Username: admin**

- **Password: naga123**

⚠️ Important: Change these credentials immediately in production.

---

## 🖥 Usage Guide
### For Citizens

**1.** Navigate to:
 `http://localhost:3000/register`

**2.** Fill in your medical details.

**3.** Click Generate QR.

**4.** Download and store your HealthQR (print or keep digitally).

### For Medics

**1.** Navigate to:
`http://localhost:3000/login`

**2.** Enter authorized medic credentials.

**3.** Access the Scanner interface.

**4.** Point the camera at a citizen’s HealthQR.

**5.** View real-time, critical medical data.

## 🔒 Security & Compliance

HealthQR is designed with a **Privacy-First** architecture:

- **Data Isolation**
Medical records are decrypted and displayed only after a successful QR scan using a valid, authenticated token.

- **Containerization**
All services run in isolated containers within a private Docker network.

- **Session Management**
Uses `sessionStorage` to ensure authentication tokens are cleared when browser tabs are closed.
