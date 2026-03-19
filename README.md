<div align="center">
  <h1>🏥 CareConnect RAG Service</h1>
  <p><i>A powerful Retrieval-Augmented Generation (RAG) engine for CareConnect</i></p>

  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
  ![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
  ![AWS S3](https://img.shields.io/badge/AWS%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
  ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
</div>

---

## 📖 Overview

The **CareConnect RAG Service** is a dedicated microservice built to process, index, and retrieve medical documents (such as PDFs, lab reports, and patient records) using advanced AI capabilities. 

Built with **FastAPI**, **PostgreSQL (`pgvector`)**, and **Google Gemini Embeddings**, this service provides sub-second semantic search. It securely downloads documents from **AWS S3**, converts their content into high-quality vector embeddings, and ensures complete multi-tenancy isolation between different doctors and patients.

## ✨ Key Features

- **📄 Automated Document Ingestion**: Fetches medical PDFs directly from AWS S3, extracts text using PyMuPDF, and robustly chunks content.
- **🧠 Advanced Vector Embeddings**: Leverages Google Generative AI (`models/text-embedding-004`) to generate dense semantic vectors.
- **⚡ Lightning-Fast Semantic Search**: Utilizes PostgreSQL with `pgvector` for efficient exact and approximate nearest-neighbor search.
- **🔒 Multi-tenant Security**: Hardened document isolation by strictly filtering queries based on `Doctor ID` and `Patient ID`.
- **🐳 Fully Containerized**: Ships with a ready-to-use Docker environment for frictionless deployment.

## 🏗️ Architecture

```mermaid
graph TD
    Client[Client / Main API] -->|POST /ingest| RAG_API(FastAPI RAG Service)
    Client -->|POST /query| RAG_API
    
    RAG_API -->|1. Fetch PDF| S3[(AWS S3)]
    RAG_API -->|2. Extract & Chunk| PyMuPDF[PyMuPDF Parser]
    PyMuPDF -->|3. Text Chunks| Gemini[Google Gemini API]
    Gemini -->|4. Vector Embeddings| RAG_API
    
    RAG_API -->|5. Store / Query| DB[(PostgreSQL + pgvector)]
```

## 💻 Tech Stack

- **Core**: Python 3.10+, FastAPI, Uvicorn
- **AI/ML**: Google Generative AI SDK (Gemini), PyMuPDF
- **Database**: PostgreSQL 16, SQLAlchemy, `pgvector`
- **Cloud/Infra**: AWS S3 (boto3), Docker, Docker Compose

## 📁 Project Structure

```text
careConnect-rag-server/
├── app/
│   ├── api/            # FastAPI route handlers
│   ├── services/       # Core business logic, parsers, and AWS integrations
│   ├── models.py       # SQLAlchemy ORM models
│   ├── schemas.py      # Pydantic validation schemas
│   ├── database.py     # DB connection and session management
│   ├── config.py       # Configuration & Env vars
│   └── main.py         # Application factory and entrypoint
├── test_ingest.py      # Test scripts for ingestion
├── docker-compose.yml  # Docker environment orchestration
├── Dockerfile          # Container build instructions
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose
- AWS IAM Credentials with S3 Read access
- Google Gemini API Key

### 1. Clone & Setup
```bash
git clone https://github.com/sharma-dikshant/careConnect-rag-server.git
cd careConnect-rag-server
```

### 2. Configure Environment
Create a `.env` file in the root directory and configure the secrets:
```env
# Database Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=ragdb
DATABASE_HOST=db
DATABASE_PORT=5432

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# AI Platform
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Build and Run
Start the entire stack (PostgreSQL + API) seamlessly via Docker:
```bash
docker compose up --build
```
*The API will be available at `http://localhost:8080` (mapped from container port 8000).*

## 🔌 API Reference

### 1. Ingest Document
Downloads a PDF from S3, generates embeddings, and indexes them in the vector database.

- **URL**: `/ingest`
- **Method**: `POST`
- **Payload**:
```json
{
  "bucket_name": "careconnect-medical-records",
  "s3_key": "reports/123/patient_456_blood_test.pdf",
  "doctor_id": "doc-123",
  "patient_id": "pat-456"
}
```

### 2. Semantic Query
Searches the vector database for text segments semantically similar to the prompt.

- **URL**: `/query`
- **Method**: `POST`
- **Payload**:
```json
{
  "query": "What are the patient's cholesterol levels?",
  "doctor_id": "doc-123",
  "patient_id": "pat-456",
  "limit": 5
}
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
