from pydantic import BaseModel
from typing import List, Optional

class DocumentInput(BaseModel):
    company_id: str
    content: str
    metadata: Optional[dict] = None
    type: str = "text"  # text, pdf, webpage, etc.
    url: Optional[str] = None

class DocumentChunk(BaseModel):
    content: str
    metadata: dict
    embedding: Optional[List[float]] = None

class QueryInput(BaseModel):
    company_id: str
    query: str
    max_results: int = 5
    min_confidence: float = 0.7

class QueryResponse(BaseModel):
    content: str
    confidence: float
    sources: List[dict]