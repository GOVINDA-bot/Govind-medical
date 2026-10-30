@echo off
echo ========================================================
echo   MediVerse - AI-Powered Digital Healthcare Platform
echo ========================================================
echo Starting FastAPI fullstack application on http://localhost:8000 ...
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
