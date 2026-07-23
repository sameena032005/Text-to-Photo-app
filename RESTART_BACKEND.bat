@echo off
echo ============================================
echo  Stopping any existing backend on port 8000
echo ============================================
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F 2>nul
)
timeout /t 2 /nobreak >nul

echo ============================================
echo  Installing Pillow (needed for GIF output)
echo ============================================
cd /d "%~dp0comfy-backend"
pip install Pillow --break-system-packages 2>nul || pip install Pillow
echo.

echo ============================================
echo  Starting API backend...
echo ============================================
start "API Backend" cmd /k "cd /d "%~dp0comfy-backend" && python server.py"
echo Done! Backend is restarting in a new window.
echo.
echo Now go to your Flutter terminal and press Shift+R to hot-reload.
pause
