import google.generativeai as genai
from app.config import settings

class EmbeddingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = 'models/text-embedding-004'

    def get_embedding(self, text: str) -> list[float]:
        if not text:
            return []
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def get_query_embedding(self, text: str) -> list[float]:
        if not text:
            return []
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

embedding_service = EmbeddingService()
