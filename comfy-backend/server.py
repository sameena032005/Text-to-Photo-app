import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from comfy_client import ComfyUIClient

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

comfy = ComfyUIClient()
OUTPUT = Path(os.getenv("COMFYUI_OUTPUT", r"C:\Users\Shaik Sameena\OneDrive\Desktop\the app git\ComfyUI\output"))

class GenRequest(BaseModel):
    prompt: str
    style: str = "Cinematic"
    duration: int = 10
    ratio: str = "16:9"
    quality: str = None

@app.post("/generate")
def generate(req: GenRequest, request: Request):
    try:
        rel_path = comfy.run_generation(prompt=req.prompt, style=req.style, ratio=req.ratio, duration=req.duration)
        # Build absolute URL so it works from both browser (localhost:8000)
        # and Android emulator (10.0.2.2:8000)
        base = str(request.base_url).rstrip("/")
        full_url = f"{base}{rel_path}"
        return {"video_url": full_url}
    except Exception as e:
        return {"video_url": "", "error": str(e)}

MIME_MAP = {".mp4": "video/mp4", ".webm": "video/webm", ".gif": "image/gif", ".png": "image/png", ".jpg": "image/jpeg"}

@app.get("/video/{fname:path}")
def video(fname: str):
    p = OUTPUT / fname
    if p.exists():
        mime = MIME_MAP.get(p.suffix.lower(), "application/octet-stream")
        return FileResponse(p, media_type=mime)
    return {"error": "not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)