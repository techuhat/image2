#!/bin/bash
echo "Starting FastAPI application..."
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo "Python version:"
python --version
echo "Installed packages:"
pip list | grep -E "(fastapi|uvicorn|gunicorn)"
echo "Starting server..."
exec gunicorn -k uvicorn.workers.UvicornWorker main:app --host 0.0.0.0 --port $PORT --timeout 120 --workers 1