#!/usr/bin/env python3
"""
Verification script to check if Render deployment is properly configured
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def main():
    print("🔍 Verifying Render deployment configuration...\n")
    
    # Check if we're in the right directory
    if not Path("render.yaml").exists():
        print("❌ Please run this script from the project root directory")
        return False
    
    all_good = True
    
    # Essential files for Render deployment
    essential_files = [
        ("render.yaml", "Render configuration"),
        ("render-backend/main.py", "FastAPI application"),
        ("render-backend/requirements.txt", "Python dependencies"),
        ("render-backend/runtime.txt", "Python runtime specification"),
        (".renderignore", "Render ignore file")
    ]
    
    for filepath, description in essential_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print()
    
    # Check render.yaml content
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
            if "env: python" in content:
                print("✅ render.yaml specifies Python environment")
            else:
                print("❌ render.yaml does not specify Python environment")
                all_good = False
            
            if "rootDir: render-backend" in content:
                print("✅ render.yaml points to render-backend directory")
            else:
                print("❌ render.yaml does not specify render-backend as rootDir")
                all_good = False
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        all_good = False
    
    print()
    
    # Check if package.json was moved
    if not Path("package.json").exists():
        print("✅ Root package.json removed/renamed (prevents Node.js detection)")
    else:
        print("⚠️  Root package.json still exists - this might cause Node.js detection")
    
    if Path("frontend-package.json").exists():
        print("✅ Frontend package.json preserved as frontend-package.json")
    
    print()
    
    # Check Python backend files
    backend_files = [
        "render-backend/main.py",
        "render-backend/requirements.txt",
        "render-backend/runtime.txt"
    ]
    
    for filepath in backend_files:
        if Path(filepath).exists():
            size = Path(filepath).stat().st_size
            print(f"✅ {filepath} ({size} bytes)")
        else:
            print(f"❌ Missing: {filepath}")
            all_good = False
    
    print()
    
    if all_good:
        print("🎉 All checks passed! Ready for Render deployment.")
        print("\nNext steps:")
        print("1. Go to your Render dashboard")
        print("2. Connect your GitHub repository")
        print("3. Render should automatically detect the render.yaml configuration")
        print("4. Deploy and check the logs for successful Python build")
    else:
        print("❌ Some issues found. Please fix them before deploying.")
    
    return all_good

if __name__ == "__main__":
    main()
