@echo off
cd /d "%~dp0"
echo Installing Python dependencies...
pip install -r requirements.txt
echo Starting API server on http://localhost:8000
python server.py
