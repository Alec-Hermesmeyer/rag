from pydantic import BaseModel
from typing import Dict, Any, Optional

class DocumentCreate(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = {}

class Document(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5

class SearchResponse(BaseModel):
    results: list[Document]
    total: int