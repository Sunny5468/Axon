@echo off
echo Starting NotebookLLM Frontend...
cd frontend
echo.
echo Frontend will open at http://localhost:3000
echo.
python -m http.server 3000
pause
