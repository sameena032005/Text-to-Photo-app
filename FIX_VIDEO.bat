@echo off
title FIX VIDEO - Restarting Backend
echo Stopping old backend...
taskkill /F /IM python.exe 2>nul
ping 127.0.0.1 -n 3 >nul

echo Installing Pillow...
pip install Pillow

echo.
echo Starting backend with GIF support...
cd /d "%~dp0comfy-backend"
python server.py
