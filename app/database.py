from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.models import DocumentChunk
import os

class Database:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "company_documents"

    async def store_document_chunks(self, chunks: List[DocumentChunk]):
        # Convert chunks to Qdrant points
        points = [
            models.PointStruct(
                id=i,
                vector=chunk.embedding,
                payload={
                    "content": chunk.content,
                    "metadata": chunk.metadata
                }
            )
            for i, chunk in enumerate(chunks)
        ]
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    async def search_similar_chunks(
        self,
        company_id: str,
        embedding: List[float],
        limit: int = 5
    ):
        # Search for similar vectors
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.company_id",
                        match=models.MatchValue(value=company_id)
                    )
                ]
            ),
            limit=limit
        )
        
        return search_result

def get_db():
    return Database()