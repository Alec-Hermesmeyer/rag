from typing import List
from app.models.document import Document, DocumentCreate
import uuid

class DocumentService:
    def __init__(self):
        self.documents = {}  # In-memory storage for demo purposes

    async def create_document(self, doc: DocumentCreate) -> Document:
        doc_id = str(uuid.uuid4())
        document = Document(
            id=doc_id,
            content=doc.content,
            metadata=doc.metadata
        )
        self.documents[doc_id] = document
        return document

    async def delete_document(self, doc_id: str):
        if doc_id in self.documents:
            del self.documents[doc_id]

    async def search_documents(self, query: str, limit: int = 10) -> List[Document]:
        # Simple search implementation for demo purposes
        # In a real app, you'd want to use a proper search engine
        results = []
        for doc in self.documents.values():
            if query.lower() in doc.content.lower():
                results.append(doc)
                if len(results) >= limit:
                    break
        return results