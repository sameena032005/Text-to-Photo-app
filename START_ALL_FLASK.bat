@echo off
title AI Video Generator (Flask) - Start All Services
cd /d "%~dp0"

echo [1/3] Starting ComfyUI (port 8188) - skip if already running
start "ComfyUI" cmd /k "cd /d "%~dp0..\ComfyUI" && python main.py --listen 127.0.0.1 --port 8188"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Flask API backend (port 8000)
start "Flask API Backend" cmd /k "cd /d "%~dp0backend" && pip install -r requirements.txt -q && pip install flask flask-cors -q && python server.py"

timeout /t 3 /nobreak >nul

echo [3/3] Starting React UI (port 5173)
start "React UI" cmd /k "cd /d "%~dp0react-frontend" && call start-frontend.bat"

echo.
echo Services starting. Open http://localhost:5173 in browser.
echo For Android emulator run: cd frontend && flutter run
pause
