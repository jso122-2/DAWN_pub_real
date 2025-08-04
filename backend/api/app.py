"""
DAWN API - FastAPI application initialization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="DAWN Neural System API",
    description="Real-time neural metrics and WebSocket streaming for DAWN",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Import routes after app is created to avoid circular imports
from ...routes import router
app.include_router(router) 