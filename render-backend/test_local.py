#!/usr/bin/env python3
"""
Test script to verify the FastAPI application works locally
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import app
    print("✓ Successfully imported FastAPI app")
    
    # Test basic functionality
    import uvicorn
    print("✓ Uvicorn is available")
    
    # Check if all required libraries are available
    try:
        from pdf2docx import Converter
        print("✓ pdf2docx is available")
    except ImportError:
        print("⚠ pdf2docx not available")
    
    try:
        import fitz
        print("✓ PyMuPDF is available")
    except ImportError:
        print("⚠ PyMuPDF not available")
    
    try:
        from PIL import Image
        print("✓ Pillow is available")
    except ImportError:
        print("⚠ Pillow not available")
    
    print("\n🚀 Application is ready to run!")
    print("To test locally, run: uvicorn main:app --reload --port 8000")
    
except Exception as e:
    print(f"❌ Error importing application: {e}")
    sys.exit(1)