from pydantic import BaseModel
from typing import Optional

class IngestRequest(BaseModel):
    file_url: str
    doctor_id: str
    patient_id: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    doctor_id: str
    patient_id: Optional[str] = None
    limit: int = 5

class SearchResult(BaseModel):
    content: str
    source_file: str
