from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from typing import List
import uuid
from ..models.document import Document, DocumentCreate

class DocumentService:
    def __init__(self, client: QdrantClient):
        self.client = client
        self.collection_name = "documents"
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the collection exists"""
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )

    def _encode_text(self, text: str) -> List[float]:
        """Simple encoding for demo purposes"""
        # In production, use a proper text embedding model
        return list(np.random.random(384))

    async def create_document(self, doc: DocumentCreate) -> Document:
        """Create a new document"""
        doc_id = str(uuid.uuid4())
        vector = self._encode_text(doc.content)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=vector,
                    payload={
                        "content": doc.content,
                        "metadata": doc.metadata
                    }
                )
            ]
        )

        return Document(
            id=doc_id,
            content=doc.content,
            metadata=doc.metadata
        )

    async def delete_document(self, doc_id: str):
        """Delete a document"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[doc_id]
            )
        )

    async def search_documents(self, query: str, limit: int = 5) -> List[Document]:
        """Search for documents"""
        query_vector = self._encode_text(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        return [
            Document(
                id=str(r.id),
                content=r.payload["content"],
                metadata=r.payload["metadata"],
                score=r.score
            )
            for r in results
        ]