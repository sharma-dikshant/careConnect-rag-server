from sqlalchemy.orm import Session
from app.models import DocumentChunk
from typing import List, Optional

class VectorStoreService:
    def store_chunks(self, db: Session, chunks: List[str], embeddings: List[List[float]], doctor_id: str, patient_id: Optional[str], source_file: str):
        db_chunks = []
        for content, embedding in zip(chunks, embeddings):
            db_chunk = DocumentChunk(
                doctor_id=doctor_id,
                patient_id=patient_id,
                content=content,
                embedding=embedding,
                source_file=source_file
            )
            db_chunks.append(db_chunk)
        
        db.add_all(db_chunks)
        db.commit()

    def search(self, db: Session, query_embedding: List[float], doctor_id: str, patient_id: Optional[str] = None, limit: int = 5):
        filters = [DocumentChunk.doctor_id == doctor_id]
        if patient_id:
            filters.append(DocumentChunk.patient_id == patient_id)
        
        # Using cosine distance (operator <=>)
        # We order by distance ascending (closest meaning smallest distance)
        results = db.query(DocumentChunk).filter(
            *filters
        ).order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        ).limit(limit).all()
        
        return results

    def get_stats(self, db: Session, doctor_id: str):
        # Helper to check data
        return db.query(DocumentChunk).filter(DocumentChunk.doctor_id == doctor_id).count()

vector_store_service = VectorStoreService()
