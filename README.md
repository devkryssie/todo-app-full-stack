# Todo API MVP

A production-grade, highly organized FastAPI backend for a Todo application. This application implements two distinct systems: an Authenticated User Todo System (fully isolated) and a Public Guest Todo System.

## 🛠️ Tech Stack
- **Backend Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL (PostgreSQL 15)
- **ORM:** SQLAlchemy (with declarative mapping)
- **Database Migrations:** Alembic
- **Authentication:** JWT Bearer (python-jose)
- **Hashing:** Bcrypt
- **Orchestration:** Docker & Docker Compose
- **Production Server:** Gunicorn with Uvicorn workers

---

## 📂 Project Architecture

The project is cleanly separated into backend and frontend systems:

```text
TodoApp/
├── docker-compose.yml  # Orchestrator
├── .env.example
├── .env
├── README.md
├── verify.py           # Integration validation client
├── backend/            # Python / FastAPI Backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── core/       # Security & config loader
│   │   ├── db/         # SQLAlchemy connection
│   │   ├── models/     # SQLAlchemy DB models
│   │   ├── schemas/    # Pydantic validation schemas
│   │   ├── crud/       # DB queries and modifications
│   │   └── api/        # Versioned endpoints (/api/v1)
│   └── alembic/        # Alembic environment & migrations
└── frontend/           # Vanilla JS & Tailwind Frontend
    ├── index.html      # Landing & guest todos
    ├── register.html   # Account registration
    ├── login.html      # Account login
    ├── dashboard.html  # Secure private task dashboard
    ├── css/
    │   └── style.css   # Main styles & Inter font
    └── js/
        ├── api.js      # Fetch client wrapper
        ├── auth.js     # Auth events
        ├── guest.js    # Guest events
        └── dashboard.js# User private task events
```

---

## 🚀 Setup & Execution

### 1. Configure Ports
Ensure the host ports defined in `docker-compose.yml` are free. By default, the application maps:
- PostgreSQL: **5435**
- FastAPI App: **8081**

### 2. Start the Stack
Run the following command to build and spin up the services:
```bash
docker compose up --build -d
```

### 3. Run Alembic Migrations
Run the migrations inside the running container to initialize the schemas:
```bash
docker exec -e PYTHONPATH=. todo_fastapi_web alembic upgrade head
```

---

## 🚦 Integration Testing & Validation

An automated verification test client is included in `verify.py`. To run the integration tests on the host, execute:
```bash
python3 verify.py
```

The script verifies:
1. API Healthcheck and OpenAPI documentation availability.
2. User registration with input validation and duplicate detection (Conflict 409).
3. JWT authorization flow and credentials verification.
4. Total data isolation: confirming a user is forbidden (403) from updating, deleting, or viewing another user's todos.
5. Enum-based status transitions (`PENDING` -> `COMPLETED`) updating `updated_at`.
6. Guest todo public access.
