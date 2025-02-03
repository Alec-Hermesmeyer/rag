from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.services.document_service import DocumentService

app = FastAPI()

# Create document service instance
document_service = DocumentService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api/v1")