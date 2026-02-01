from fastapi import APIRouter, Depends, HTTPException, Body
from urllib.parse import urlparse, unquote
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import IngestRequest, QueryRequest, SearchResult, QueryResponse
from app.services.s3_service import s3_service
from app.services.pdf_parser import pdf_parser
from app.services.chunking import text_chunker
from app.services.embedding import embedding_service
from app.services.vector_store import vector_store_service
from app.services.llm_service import llm_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/ingest")
def ingest_document(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        # Await S3 download (blocking for now is fine for MVP, async boto3 is complex)
        file_source = ""
        if not request.file_url:
            raise HTTPException(status_code=400, detail="file_url is required")

        # Download from Presigned URL
        file_obj = s3_service.download_file_from_url(request.file_url)
        
        # Extract filename from URL for validation and metadata
        parsed_url = urlparse(request.file_url)
        path = unquote(parsed_url.path)
        file_source = os.path.basename(path)

        
        if file_source.lower().endswith(".pdf"):
            text = pdf_parser.extract_text(file_obj)
        else:
           raise HTTPException(status_code=400, detail=f"Only PDF files are supported currently. Got: {file_source}")
           
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from document")

        chunks = text_chunker.chunk_text(text)
        
        # Generate embeddings
        # Note: In production, consider batching or async
        embeddings = [embedding_service.get_embedding(chunk) for chunk in chunks]
        
        vector_store_service.store_chunks(
            db=db,
            chunks=chunks,
            embeddings=embeddings,
            doctor_id=request.doctor_id,
            patient_id=request.patient_id,
            source_file=file_source
        )
        
        return {"status": "success", "chunks_processed": len(chunks), "source_file": file_source}
        
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        # If it's just a key error or something, 404 might be better, but 500 is safe catch-all
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        query_embedding = embedding_service.get_query_embedding(request.query)
        
        results = vector_store_service.search(
            db=db,
            query_embedding=query_embedding,
            doctor_id=request.doctor_id,
            patient_id=request.patient_id,
            limit=request.limit
        )
        
        # Extract content for LLM context
        context = [res.content for res in results]
        
        # Generate Answer
        answer = llm_service.generate_answer(request.query, context)
        print(answer)
        sources = []
        for res in results:
            sources.append(SearchResult(
                content=res.content,
                source_file=res.source_file
            ))
            
        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
