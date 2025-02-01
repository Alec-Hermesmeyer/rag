from fastapi import APIRouter, Depends
from .services.document_service import DocumentService
from .models.document import DocumentCreate, Document, SearchQuery, SearchResponse

router = APIRouter()

def get_document_service():
    # In a real app, you'd get this from a dependency injection container
    from .main import document_service
    return document_service

@router.post("/documents", response_model=Document)
async def create_document(
    doc: DocumentCreate,
    service: DocumentService = Depends(get_document_service)
):
    return await service.create_document(doc)

@router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    service: DocumentService = Depends(get_document_service)
):
    await service.delete_document(doc_id)
    return {"status": "success"}

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    query: SearchQuery,
    service: DocumentService = Depends(get_document_service)
):
    results = await service.search_documents(query.query, query.limit)
    return SearchResponse(
        results=results,
        total=len(results)
    )