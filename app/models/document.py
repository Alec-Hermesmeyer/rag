from pydantic import BaseModel
from typing import List, Optional, Dict

class DocumentCreate(BaseModel):
    content: str
    metadata: Optional[Dict] = None

class Document(BaseModel):
    id: str
    content: str
    metadata: Optional[Dict] = None

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 10

class SearchResponse(BaseModel):
    results: List[Document]
    total: int