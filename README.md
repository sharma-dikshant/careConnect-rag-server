# CareConnect RAG AI Service

This service provides the intelligent Retrieval-Augmented Generation (RAG) backend for the CareConnect application. Built using FastAPI, PostgreSQL (with pgvector), and Google Gemini, it empowers users to chat with large medical context, extracting relevant insights and answers.

## 🚀 Features

- **Automated PDF Processing**: Ingests files (via pre-signed URLs), extracts their text using PyMuPDF, and robustly chunks the content into semantic blocks.
- **Embedded AI Search**: Generates vector embeddings for your documents using Google Generative AI (Gemini) and stores them natively in PostgreSQL using the highly efficient `pgvector` extension.
- **Context-Aware Querying**: Leverages Gemini to dynamically summarize information sourced accurately from chunked and retrieved document excerpts in response to search queries.
- **Multi-Tenant Ready**: Uses metadata tagging (`doctor_id` and `patient_id`) within the vector store to effectively fence boundaries around document queries, ensuring private context.

## 🛠️ Tech Stack

- **API Framework:** FastAPI
- **Database:** PostgreSQL 16.0 + pgvector
- **ORM Tool:** SQLAlchemy
- **Vector & LLM Engine:** Google Gemini (Generative AI)
- **PDF Extraction:** PyMuPDF (Fitz)
- **Storage Strategy:** Presigned URLs (S3) integration
- **Containerization:** Docker Compose

## 📂 Project Structure

```bash
careConnect-rag-server/
├── app/
│   ├── api/            # Controller layer including API routes.
│   ├── services/       # Core business logic (chunking, embeddings, PDF parsing, llm wrappers).
│   ├── schemas.py      # Request/Response Pydantic validation schemas.
│   ├── models.py       # SQLAlchemy database models for vector storing.
│   ├── database.py     # SQLAlchemy DB connection handler.
│   ├── config.py       # Environment configuration loading.
│   └── main.py         # App entrypoint and lifecycle events.
├── docker-compose.yml  # Local stack orchestration containing pgvector db and ai-server.
├── Dockerfile          # Steps to build the application container.
└── requirements.txt    # Python dependencies.
```

## ⚙️ Getting Started

### Prerequisites
- Docker and Docker Compose installed
- A valid Google Gemini API Key
- Supported S3 storage infrastructure for handling files.

### Installation

1. Create an environment file (`.env`) in the root directory:
```env
# Database Credentials
POSTGRES_USER=user
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ragdb
DATABASE_HOST=rag-db
DATABASE_PORT=5432

# Cloud Infrastructure
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=your_region

# AI Keys
GEMINI_API_KEY=your_google_gemini_api_key
```

2. Start the services using Docker Compose:
```bash
docker compose up --build -d
```
The AI backend will start up and run initialization scripts automatically to create the internal pgvector extension and schemas.

## 📡 API Endpoints

The service primarily handles two endpoints:

### 1. Ingest a Document
Downloads the PDF payload structure, chunks it, generates vector weights, and commits them to `pgvector` tied to the patient record. This endpoint blocks appropriately to track upload success.

**`POST /ingest`**
```json
{
  "file_url": "https://s3.your-region.amazonaws.com/your-bucket/path/to/report.pdf?X-Amz-Signature=...",
  "doctor_id": "doc-555",
  "patient_id": "pat-123"
}
```

### 2. Query Knowledge Base
Performs a similarity semantic search over `pgvector` via the input question, generates a direct textual answer utilizing Gemini, and outlines the precise source texts utilized inline.

**`POST /query`**
```json
{
  "query": "What symptoms did the patient present with?",
  "doctor_id": "doc-555",
  "patient_id": "pat-123",
  "limit": 5
}
```

### 3. Health Check
Endpoint used by `docker-compose.yml` to ensure API route stability.

**`GET /health`**
```json
{
  "status": "healthy"
}
```

## 🧠 Logical Flow

1.  **Ingestion Phase**:
    *   Hits `POST /ingest`.
    *   Downloads presigned S3 url document to memory.
    *   Applies `PyMuPDF` to rip raw, valid text out.
    *   Passes extracted content into `app.services.chunking.text_chunker`.
    *   Submits blocks to Google Gemini for generating mathematically embedded vectors.
    *   Commits chunk + embeddings + related medical metadata into Postgres.

2.  **Retrieval & Querying**:
    *   Hits `POST /query`.
    *   Converts user's natural language question into a vector using the same embedding logic.
    *   Queries PostgreSQL running `pgvector` by calculating similarity mathematically (cosine distance).
    *   Filters chunks tightly via `doctor_id` and `patient_id`.
    *   Combines nearest chunks explicitly as prompt context back to Gemini.
    *   Yields both summarized human-readable text and root search context sources.
