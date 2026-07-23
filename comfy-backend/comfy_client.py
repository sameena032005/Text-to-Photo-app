from __future__ import annotations
import json, os, random, uuid
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
import httpx, websocket

STYLE_PREFIX = {"Cinematic": "cinematic film still, dramatic lighting, 4k, ", "Anime": "anime style, vibrant colors, detailed illustration, ", "Realistic": "photorealistic, ultra detailed, natural lighting, ", "3D": "3d render, octane render, highly detailed, ", "Cartoon": "cartoon style, bold colors, clean lines, ", "Cyberpunk": "cyberpunk, neon lights, futuristic city, "}
RATIO_SIZE = {"16:9": (768, 432), "9:16": (432, 768), "1:1": (512, 512)}

class ComfyUIClient:
    def __init__(self, host: str | None = None, port: int | None = None):
        host = host or os.getenv("COMFYUI_HOST", "127.0.0.1")
        port = port or int(os.getenv("COMFYUI_PORT", "8188"))
        self.base = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.client_id = str(uuid.uuid4())

    def is_online(self) -> bool:
        try:
            r = httpx.get(f"{self.base}/system_stats", timeout=5.0)
            return r.status_code == 200
        except: return False

    def get_checkpoints(self) -> list[str]:
        try:
            r = httpx.get(f"{self.base}/object_info/CheckpointLoaderSimple", timeout=15.0)
            r.raise_for_status()
            info = r.json()
            return info["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"][0]
        except: return []

    def build_workflow(self, prompt: str, style: str, ratio: str, seed: int | None = None) -> dict[str, Any]:
        template_path = Path(__file__).parent / "workflows" / "text_to_video_base.json"
        workflow = json.loads(template_path.read_text(encoding="utf-8"))
        checkpoints = self.get_checkpoints()
        ckpt = checkpoints[0] if checkpoints else "v1-5-pruned-emaonly.safetensors"
        width, height = RATIO_SIZE.get(ratio, (512, 512))
        style_text = STYLE_PREFIX.get(style, "")
        full_prompt = f"{style_text}{prompt}"
        workflow = deepcopy(workflow)
        workflow["4"]["inputs"]["ckpt_name"] = ckpt
        workflow["5"]["inputs"]["width"] = width
        workflow["5"]["inputs"]["height"] = height
        workflow["6"]["inputs"]["text"] = full_prompt
        workflow["3"]["inputs"]["seed"] = seed if seed is not None else random.randint(1, 2**31 - 1)
        return workflow

    def queue_prompt(self, workflow: dict[str, Any]) -> str:
        payload = {"prompt": workflow, "client_id": self.client_id}
        r = httpx.post(f"{self.base}/prompt", json=payload, timeout=30.0)
        r.raise_for_status()
        data = r.json()
        if "error" in data: raise RuntimeError(data["error"])
        return data["prompt_id"]

    def wait_for_completion(self, prompt_id: str, timeout: float = 600.0) -> None:
        ws = websocket.WebSocket()
        ws.connect(f"{self.ws_url}?clientId={self.client_id}")
        ws.settimeout(timeout)
        try:
            while True:
                raw = ws.recv()
                if not isinstance(raw, str): continue
                msg = json.loads(raw)
                if msg.get("type") == "executing":
                    data = msg.get("data", {})
                    if data.get("node") is None and data.get("prompt_id") == prompt_id: break
        finally: ws.close()

    def get_outputs(self, prompt_id: str) -> list[dict[str, str]]:
        r = httpx.get(f"{self.base}/history/{prompt_id}", timeout=30.0)
        r.raise_for_status()
        history = r.json().get(prompt_id, {})
        outputs: list[dict[str, str]] = []
        for node_out in history.get("outputs", {}).values():
            for key in ("images", "gifs", "videos"):
                if key not in node_out: continue
                for item in node_out[key]:
                    outputs.append({"filename": item["filename"], "subfolder": item.get("subfolder", ""), "type": item.get("type", "output")})
        return outputs

    def image_to_gif(self, image_path: Path, duration: int = 5) -> Path:
        """Create an animated GIF with slow zoom — uses only Pillow, always works."""
        import math
        try:
            from PIL import Image
            gif_path = image_path.with_suffix(".gif")
            img = Image.open(image_path).convert("RGB").resize((480, 270))
            w, h = img.size
            num_frames = 24
            frames = []
            for i in range(num_frames):
                zoom = 1.0 + 0.12 * math.sin(math.pi * i / num_frames)
                nw, nh = int(w / zoom), int(h / zoom)
                left, top = (w - nw) // 2, (h - nh) // 2
                frame = img.crop((left, top, left + nw, top + nh)).resize((w, h), Image.LANCZOS)
                frames.append(frame)
            frames[0].save(
                gif_path, save_all=True, append_images=frames[1:],
                duration=int(duration * 1000 / num_frames), loop=0
            )
            if gif_path.exists() and gif_path.stat().st_size > 1000:
                return gif_path
        except Exception:
            pass
        return image_path

    def image_to_mp4(self, image_path: Path, duration: int = 5) -> Path:
        """Convert a still image to an MP4 video. Tries ffmpeg first, then cv2, then imageio."""
        import subprocess, shutil
        mp4_path = image_path.with_suffix(".mp4")

        # ── 1. Find ffmpeg (check PATH + common Windows install locations) ──
        ffmpeg_candidates = [
            shutil.which("ffmpeg"),
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
            str(Path(__file__).resolve().parents[2] / "ComfyUI" / "python_embeded" / "Scripts" / "ffmpeg.exe"),
        ]
        ffmpeg_cmd = next((p for p in ffmpeg_candidates if p and Path(p).exists()), None)

        if ffmpeg_cmd:
            try:
                fps = 24
                cmd = [
                    ffmpeg_cmd, "-y",
                    "-loop", "1", "-i", str(image_path),
                    "-vf", "scale=768:432:force_original_aspect_ratio=decrease,"
                           "pad=768:432:(ow-iw)/2:(oh-ih)/2",
                    "-c:v", "libx264", "-t", str(duration),
                    "-pix_fmt", "yuv420p", "-an",
                    str(mp4_path),
                ]
                r = subprocess.run(cmd, capture_output=True, timeout=90)
                if r.returncode == 0 and mp4_path.exists():
                    return mp4_path
            except Exception:
                pass

        # ── 2. Fall back to cv2 (usually present in ComfyUI's venv) ──
        try:
            import cv2, numpy as np
            from PIL import Image as PILImage
            img = np.array(PILImage.open(image_path).convert("RGB").resize((768, 432)))
            img_bgr = img[:, :, ::-1]
            fps = 24
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(str(mp4_path), fourcc, fps, (768, 432))
            for _ in range(fps * duration):
                out.write(img_bgr)
            out.release()
            if mp4_path.exists() and mp4_path.stat().st_size > 1000:
                return mp4_path
        except Exception:
            pass

        # ── 3. Fall back to imageio ──
        try:
            import imageio
            from PIL import Image as PILImage
            img = PILImage.open(image_path).convert("RGB").resize((768, 432))
            import numpy as np
            frame = np.array(img)
            frames = [frame] * (24 * duration)
            imageio.mimwrite(str(mp4_path), frames, fps=24, codec="libx264")
            if mp4_path.exists() and mp4_path.stat().st_size > 1000:
                return mp4_path
        except Exception:
            pass

        # ── 4. Last resort: return the original image ──
        return image_path

    def file_url(self, filename: str, subfolder: str = "") -> str:
        if subfolder: rel_path = f"{subfolder}/{filename}"
        else: rel_path = filename
        return f"/video/{rel_path}"

    def run_generation(self, prompt: str, style: str, ratio: str, duration: int = 10) -> str:
        if not self.is_online():
            raise ConnectionError("ComfyUI is not running. Start it with: python main.py --listen 127.0.0.1 --port 8188")
        workflow = self.build_workflow(prompt, style, ratio)
        prompt_id = self.queue_prompt(workflow)
        self.wait_for_completion(prompt_id)
        outputs = self.get_outputs(prompt_id)
        if not outputs: raise RuntimeError("ComfyUI finished but produced no output files.")
        out = outputs[-1]
        subfolder = out.get("subfolder", "")
        filename = out["filename"]

        # Convert image output to animated GIF using Pillow (always available)
        _output_dir = Path(os.getenv("COMFYUI_OUTPUT", r"C:\Users\Shaik Sameena\OneDrive\Desktop\the app git\ComfyUI\output"))
        try:
            img_path = _output_dir / subfolder / filename if subfolder else _output_dir / filename
            if img_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                dur = max(3, min(duration, 8))
                result_path = self.image_to_gif(img_path, duration=dur)
                filename = result_path.name
        except Exception:
            pass  # fallback to returning original file

        return self.file_url(filename, subfolder)