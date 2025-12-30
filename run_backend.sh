#!/bin/bash
echo "Starting NotebookLLM Backend..."
cd backend
pip install -r requirements.txt
echo ""
echo "Backend is starting on http://localhost:8000"
echo "Press Ctrl+C to stop"
python main.py
