#!/usr/bin/env python3
"""
Test script to verify the backend can start properly
"""
import sys
import os

# Add the render-backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the main app
    from main import app
    print("✅ Successfully imported FastAPI app")
    
    # Try to get the health check endpoint
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    
    if response.status_code == 200:
        print("✅ Health check endpoint working")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Health check failed with status {response.status_code}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install fastapi uvicorn gunicorn python-multipart pdf2docx aiofiles python-docx PyMuPDF Pillow")
    
except Exception as e:
    print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Backend test completed.")
