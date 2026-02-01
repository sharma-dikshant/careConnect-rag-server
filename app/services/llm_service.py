from google import genai
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = 'gemini-2.5-flash'
    def generate_answer(self, query: str, context: list[str]) -> str:
        print(f"Generating answer for query: {query}")
        print(f"Context: {context}")
        if not context:
            return "I couldn't find any relevant information to answer your question."

        print(context)
        context_str = "\n\n".join(context)
        
        prompt = f"""You are a helpful assistant for CareConnect. 
                    Answer the user's question using the context provided below. 
                    Context:
                    {context_str}

                    Question: 
                    {query}

                    Answer:"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "I encountered an error while generating the answer."

llm_service = LLMService()
