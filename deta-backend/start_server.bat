@echo off
echo Starting PDF to DOCX Conversion Server...
echo.
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
cd /d "d:\toolkit-main\deta-backend"
D:\toolkit-main\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
