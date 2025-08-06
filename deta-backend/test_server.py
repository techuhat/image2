#!/usr/bin/env python3
"""
Test script to verify the PDF to DOCX conversion API
"""

import requests
import json
import sys
import os

def test_server():
    """Test if the server is running and endpoints work"""
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is running!")
            print(f"Service: {data['service']}")
            print(f"Status: {data['status']}")
            print(f"Available methods: {data['available_methods']}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {str(e)}")
        return False

def test_with_sample_pdf():
    """Test the conversion endpoint with a sample PDF"""
    
    # This would require a sample PDF file
    print("\n📄 To test PDF conversion:")
    print("1. Start the server: uvicorn main:app --host 0.0.0.0 --port 8000")
    print("2. Use a tool like Postman or curl to send a PDF file to /convert")
    print("3. Example curl command:")
    print("   curl -X POST http://localhost:8000/convert -F 'file=@sample.pdf' -o converted.docx")

if __name__ == "__main__":
    print("🚀 Testing PDF to DOCX Conversion API")
    print("=" * 50)
    
    # Test if server is running
    if test_server():
        test_with_sample_pdf()
    else:
        print("\n💡 To start the server, run:")
        print("uvicorn main:app --host 0.0.0.0 --port 8000")
