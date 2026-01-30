from google import genai
from google.genai import types
from app.config import settings

class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = 'gemini-embedding-001'

    def get_embedding(self, text: str) -> list[float]:
        if not text:
            return []
        result = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        return result.embeddings[0].values
    
    def get_query_embedding(self, text: str) -> list[float]:
        if not text:
            return []
        result = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        return result.embeddings[0].values

embedding_service = EmbeddingService()
