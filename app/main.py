from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from .routes import router
from .services.document_service import DocumentService

# Initialize Qdrant client
qdrant_client = QdrantClient(":memory:")  # For development, use in-memory storage
# For production, use:
# qdrant_client = QdrantClient(host="localhost", port=6333)

# Initialize document service
document_service = DocumentService(qdrant_client)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000"  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api")