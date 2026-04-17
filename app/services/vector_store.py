from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models import DocumentChunk
from typing import List, Optional
from sqlalchemy import and_, or_, case


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

    def search(
        db: Session,
        query_embedding,
        doctor_id: int,
        patient_id: int | None,
        limit: int = 5
    ):
        try:
            # ---------- FILTER ----------
            if patient_id is None:
                filter_condition = and_(
                    DocumentChunk.doctor_id == doctor_id,
                    DocumentChunk.patient_id.is_(None)
                )
            else:
                filter_condition = and_(
                    DocumentChunk.doctor_id == doctor_id,
                    or_(
                        DocumentChunk.patient_id == patient_id,
                        DocumentChunk.patient_id.is_(None)
                    )
                )

            # ---------- PRIORITY ----------
            if patient_id is None:
                # No prioritization needed (only NULL records exist)
                priority_order = 0
            else:
                priority_order = case(
                    (DocumentChunk.patient_id == patient_id, 0),  # highest priority
                    else_=1
                )

            # ---------- QUERY ----------
            query = (
                db.query(DocumentChunk)
                .filter(filter_condition)
            )

            # ---------- ORDERING ----------
            if patient_id is None:
                query = query.order_by(
                    # Only similarity matters
                    DocumentChunk.embedding.cosine_distance(query_embedding)
                )
            else:
                query = query.order_by(
                    priority_order,
                    DocumentChunk.embedding.cosine_distance(query_embedding)
                )

            results = query.limit(limit).all()
            return results

        except Exception as e:
            print(f"Vector search failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Vector search failed")

    def get_stats(self, db: Session, doctor_id: str):
        # Helper to check data
        return db.query(DocumentChunk).filter(DocumentChunk.doctor_id == doctor_id).count()


vector_store_service = VectorStoreService()
