@echo off
cd /d "%~dp0"
if not exist "node_modules\vite\bin\vite.js" (
  echo Installing dependencies - first run can take several minutes...
  call npm install
  if errorlevel 1 (
    echo npm install failed. Check internet / SSL settings in .npmrc
    pause
    exit /b 1
  )
)
echo Starting UI at http://localhost:5173
call npm run dev
