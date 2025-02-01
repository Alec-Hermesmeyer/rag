from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key header is missing"
        )
    
    expected_api_key = os.getenv("API_KEY")
    if api_key != f"Bearer {expected_api_key}":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return api_key