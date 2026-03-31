# HealthQR: Emergency Medical Response System

In critical "golden hour" emergencies, seconds save lives. **HealthQR** addresses the dangerous data gap between unconscious patients and first responders.

While currently a side-project, its real-world potential is immense:

- **Universal Accessibility**: Instant access to allergies and blood types without needing a centralized hospital database login.

- **Interoperability**: A low-cost bridge that works across different healthcare providers.

- **Scalability**: A lightweight framework that could be deployed city-wide for rapid medic-to-patient data retrieval.  

---

##  Key Features

- **Citizen Portal**  
  Simple registration for residents to input vitals, allergies, and emergency contacts.

- **Instant QR Generation**  
  Generates a unique, downloadable HealthQR code for physical or digital storage.

- **Secure Medic Scanner**  
  A protected portal for authorized medical personnel with real-time QR decoding.

---

##  Tech Stack

- **Frontend:** Next.js (React), Tailwind CSS, `html5-qrcode`  
- **Backend:** FastAPI (Python), SQLAlchemy  
- **Database:** PostgreSQL  
- **Deployment:** Docker & Docker Compose  

---

##  Installation & Setup

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

---

##  Usage Guide
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

##  Security & Compliance

HealthQR is designed with a **Privacy-First** architecture:

- **Data Isolation**
Medical records are decrypted and displayed only after a successful QR scan using a valid, authenticated token.

- **Containerization**
All services run in isolated containers within a private Docker network.

- **Session Management**
Uses `sessionStorage` to ensure authentication tokens are cleared when browser tabs are closed.
