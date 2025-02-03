# from fastapi import FastAPI
# from app.routes import router
# from fastapi.middleware.cors import CORSMiddleware
# from app.services.document_service import DocumentService

# app = FastAPI()

# # Create document service instance
# document_service = DocumentService()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with specific origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include the router
# app.include_router(router, prefix="/api/v1")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from app.services.document_service import DocumentService
from app.routes import router

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Initialize services
document_service = DocumentService(qdrant_client)

# Include routers
from app.routes import router
app.include_router(router)