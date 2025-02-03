from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

class DocumentService:
    def __init__(self, qdrant_client: QdrantClient):
        self.client = qdrant_client
        self.collection_name = "documents"
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the collection exists"""
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )