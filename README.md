# CareConnect RAG Service

A Retrieval-Augmented Generation (RAG) service for CareConnect, built with FastAPI, PostgreSQL (pgvector), and Google Gemini Embeddings. This service processes medical documents (PDFs) from AWS S3, generates embeddings, and enables semantic search for relevant context.

## Features

- **Document Ingestion**: Downloads PDFs from AWS S3, extracts text, and chunks content.
- **Vector Embeddings**: Uses Google Gemini (`models/text-embedding-004`) to generate high-quality text embeddings.
- **Semantic Search**: Stores and retrieves context using PostgreSQL with `pgvector` extension.
- **Multi-tenancy Support**: Isolates documents by Doctor ID and Patient ID.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 16 + pgvector
- **ORM**: SQLAlchemy
- **Embeddings**: Google Generative AI (Gemini)
- **PDF Processing**: PyMuPDF
- **Storage**: AWS S3
- **Containerization**: Docker & Docker Compose

## Folder Structure

```
careConnect-rag/
├── app/
│   ├── api/            # API Routes
│   ├── services/       # Business logic (PDF parser, Embeddings, Vector Store)
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   ├── database.py     # Database connection
│   ├── config.py       # Configuration & Env vars
│   └── main.py         # Application entrypoint
├── docker-compose.yml  # Docker orchestration
├── Dockerfile          # App container image
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```

## Setup Guide

### Prerequisites

- Docker & Docker Desktop
- AWS Credentials (access to S3 bucket)
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd careConnect-rag
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=ragdb
DATABASE_HOST=db
DATABASE_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```
The API will be available at `http://localhost:8080` (mapped from container port 8000).

## API Usage

### Ingest Document

**Endpoint**: `POST /ingest`

Downloads a file from S3, processes it, and stores embeddings.

**Request Body**:
```json
{
  "bucket_name": "my-bucket",
  "s3_key": "path/to/report.pdf",
  "doctor_id": "doc-123",
  "patient_id": "pat-456"
}
```

### Query Documents

**Endpoint**: `POST /query`

Searches for relevant context based on a natural language query.

**Request Body**:
```json
{
  "query": "What are the patient's symptoms?",
  "doctor_id": "doc-123",
  "patient_id": "pat-456",
  "limit": 5
}
```

## How It Works

1.  **Ingestion**:
    *   The service downloads the specified PDF from S3.
    *   `PyMuPDF` extracts raw text from the file.
    *   The text is split into overlapping chunks (default 1000 chars).
    *   Each chunk is passed to Google Gemini to generate a vector embedding.
    *   The chunk text and its vector are stored in PostgreSQL.

2.  **Retrieval**:
    *   The user's query is converted into a vector embedding.
    *   `pgvector` calculates the cosine distance between the query vector and stored document vectors.
    *   The most similar text chunks are returned as usage context (e.g., for an LLM to generate an answer).
