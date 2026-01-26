from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import IngestRequest, QueryRequest, SearchResult
from app.services.s3_service import s3_service
from app.services.pdf_parser import pdf_parser
from app.services.chunking import text_chunker
from app.services.embedding import embedding_service
from app.services.vector_store import vector_store_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ingest")
def ingest_document(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        # Await S3 download (blocking for now is fine for MVP, async boto3 is complex)
        file_obj = s3_service.download_file(request.bucket_name, request.s3_key)
        
        if request.s3_key.lower().endswith(".pdf"):
            text = pdf_parser.extract_text(file_obj)
        else:
           raise HTTPException(status_code=400, detail="Only PDF files are supported currently")
           
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
            source_file=request.s3_key
        )
        
        return {"status": "success", "chunks_processed": len(chunks)}
        
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        # If it's just a key error or something, 404 might be better, but 500 is safe catch-all
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=list[SearchResult])
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
        
        response = []
        for res in results:
            response.append(SearchResult(
                content=res.content,
                source_file=res.source_file
            ))
            
        return response

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
