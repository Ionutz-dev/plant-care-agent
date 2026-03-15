"""
Main entry point for the Plant Care Card Generator API.
Run this file to start the FastAPI server.
"""
import uvicorn
from config import config

if __name__ == "__main__":
    print("Starting Plant Care Card Generator API...")
    print(f"Server will run on http://{config.API_HOST}:{config.API_PORT}")
    print("Access the API documentation at http://localhost:8000/docs")

    uvicorn.run(
        "api.app:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True  # Auto-reload on code changes
    )