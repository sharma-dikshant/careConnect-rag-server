class TextChunker:
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        if not text:
            return []
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            # Ensure we don't go out of bounds (python slicing handles this gracefully) but simple logic is fine
            chunks.append(text[i : i + chunk_size])
        return chunks

text_chunker = TextChunker()
