# Adaptive Workflow Intelligence System

A production-style backend system built using FastAPI, PostgreSQL, Redis, Celery, Docker, and async Python architecture.

This project focuses on modern backend engineering concepts including:

* asynchronous APIs
* distributed task processing
* background workers
* Dockerized infrastructure
* CI/CD pipelines
* modular backend architecture
* AI workflow orchestration foundations

---

# Features

## Authentication System

* JWT-based authentication
* User registration and login
* Protected routes
* Password hashing with bcrypt

## Async FastAPI Backend

* Built using FastAPI
* Async SQLAlchemy integration
* Modular domain-driven architecture
* Dependency injection

## PostgreSQL Integration

* Async PostgreSQL database connection
* SQLAlchemy ORM models
* Alembic migrations
* Relationship management

## Redis + Celery Background Jobs

* Distributed task processing
* Redis message broker
* Celery worker integration
* Async task execution
* Task status tracking

## AI Workflow Processing

* AI workflow summary generation
* Intelligence service layer
* Ollama integration support
* Workflow analytics foundation

## Dockerized Infrastructure

* Docker Compose setup
* API container
* Celery worker container
* PostgreSQL container
* Redis container

## CI/CD Pipeline

* GitHub Actions integration
* Automated testing
* Black formatting checks
* isort validation
* flake8 linting

---

# Tech Stack

| Category          | Technology       |
| ----------------- | ---------------- |
| Backend Framework | FastAPI          |
| Database          | PostgreSQL       |
| ORM               | SQLAlchemy Async |
| Background Jobs   | Celery           |
| Message Broker    | Redis            |
| Authentication    | JWT              |
| Containerization  | Docker           |
| Migrations        | Alembic          |
| Testing           | Pytest           |
| CI/CD             | GitHub Actions   |
| AI Integration    | Ollama           |

---

# System Architecture

```text
Client
   ↓
FastAPI API Layer
   ↓
Redis Queue
   ↓
Celery Worker
   ↓
PostgreSQL Database
```

---

# Project Structure

```text
app/
├── api/
├── core/
│   ├── celery/
│   ├── config/
│   ├── database/
│   ├── logging/
│   └── security/
│
├── domains/
│   ├── auth/
│   ├── intelligence/
│   ├── project/
│   ├── task/
│   └── workspace/
│
├── integrations/
│   └── ollama/
│
└── workers/
    └── ai_tasks.py
```

---

# Async Task Workflow

## Generate AI Summary

### Create Background Task

```http
POST /api/v1/intelligence/generate-summary
```

### Response

```json
{
  "task_id": "uuid",
  "status": "processing"
}
```

---

## Check Task Status

### Endpoint

```http
GET /api/v1/intelligence/task-status/{task_id}
```

### Example Response

```json
{
  "task_id": "uuid",
  "status": "SUCCESS",
  "result": "AI-generated summary for project: Adaptive Workflow System"
}
```

---

# Local Development Setup

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd adaptive-workflow-system
```

---

## 2. Create Environment File

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/adaptive_workflow_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_secret_key
```

---

## 3. Start Docker Containers

```bash
docker compose up --build
```

---

## 4. Run Database Migrations

```bash
alembic upgrade head
```

---

## 5. Access API Docs

```text
http://localhost:8000/docs
```

---

# Running Tests

```bash
pytest
```

---

# CI/CD

GitHub Actions pipeline automatically performs:

* formatting checks using Black
* import sorting checks using isort
* linting using flake8
* automated testing using pytest

---

# Key Backend Engineering Concepts Practiced

* Async backend development
* Distributed task queues
* Docker networking
* Background job processing
* Database migrations
* API versioning
* JWT authentication
* Modular architecture
* CI/CD pipelines
* Container orchestration basics
* Redis messaging systems
* Celery workers

---

# Future Improvements

* Real-time WebSocket updates
* AI-powered workflow optimization
* Task analytics dashboard
* Notification system
* Role-based access control
* Production deployment

---

# Author

Dhruv Kaura
