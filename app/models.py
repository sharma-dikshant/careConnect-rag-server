from sqlalchemy import Column, Integer, String, DateTime, Text
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String, index=True, nullable=False)
    patient_id = Column(String, index=True, nullable=True)
    
    content = Column(Text, nullable=False)
    # Gemini text-embedding-001 is 3072 dimensions
    embedding = Column(Vector(3072)) 
    
    source_file = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
