from typing import List
import numpy as np
from app.models import QueryInput, QueryResponse
from app.database import Database
from langchain.embeddings import OpenAIEmbeddings

class QueryService:
    def __init__(self, db: Database):
        self.db = db
        self.embeddings = OpenAIEmbeddings()

    async def process_query(self, query: QueryInput) -> QueryResponse:
        # Generate embedding for query
        query_embedding = await self.embeddings.embed_query(query.query)
        
        # Search for similar chunks
        similar_chunks = await self.db.search_similar_chunks(
            company_id=query.company_id,
            embedding=query_embedding,
            limit=query.max_results
        )
        
        # Calculate confidence score (average similarity)
        confidence = np.mean([chunk.similarity for chunk in similar_chunks])
        
        # Format sources
        sources = [
            {
                "title": chunk.metadata.get("title", "Document Chunk"),
                "url": chunk.metadata.get("source_url"),
                "content": chunk.content,
                "similarity": chunk.similarity
            }
            for chunk in similar_chunks
        ]
        
        return QueryResponse(
            content="\n\n".join([chunk.content for chunk in similar_chunks]),
            confidence=float(confidence),
            sources=sources
        )