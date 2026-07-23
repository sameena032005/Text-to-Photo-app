@echo off
echo Creating files...

cd /d AI_Text_To_Video\comfy-backend

REM Create server.py
(
echo from fastapi import FastAPI
echo from fastapi.middleware.cors import CORSMiddleware
echo import os
echo from pathlib import Path
echo
echo app = FastAPI()
echo app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
echo
echo @app.get("/health"^)
echo def health(^):
echo     return {"status": "ok"}
echo
echo @app.post("/generate"^)
echo def generate(body: dict^):
echo     return {"video_url": "/video/sample.mp4"}
echo
echo @app.get("/video/{file_path:path}"^)
echo async def serve_video(file_path: str^):
echo     return {"status": "ok"}
echo
echo if __name__ == "__main__":
echo     import uvicorn
echo     uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True^)
) > server.py

echo ✅ Files created!
echo.
echo Now run:
echo Terminal 1: python server.py
echo Terminal 2: cd ../react-frontend && npm run dev
echo.
pause