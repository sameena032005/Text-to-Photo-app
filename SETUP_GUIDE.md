# AI Video Generator — Setup & Run Guide

## Why `npm run dev` was hanging

`node_modules` was **never installed** (npm failed silently due to SSL/OneDrive). Without Vite, the command appears to hang forever.

**Fix applied:**
- Slimmer `package.json` (fewer packages)
- `.npmrc` with `strict-ssl=false` for corporate SSL issues
- `start-frontend.bat` runs `npm install` then `npm run dev`

```powershell
cd react-frontend
npm install
npm run dev
```

You should see: `VITE ready` and `http://localhost:5173/`

---

## Run everything (3 terminals)

### Option A — double-click
Run `START_ALL.bat` in `AI_Text_To_Video/`

### Option B — manual

**Terminal 1 — ComfyUI** (port 8188)
```powershell
cd "..\..\ComfyUI"
python main.py --listen 127.0.0.1 --port 8188
```

**Terminal 2 — API backend** (port 8000)
```powershell
cd comfy-backend
pip install -r requirements.txt
python server.py
```

**Terminal 3 — React UI** (port 5173)
```powershell
cd react-frontend
npm install
npm run dev
```

Open **http://localhost:5173** in Chrome.

In **Settings**, API URL = `http://127.0.0.1:8000`

---

## Android emulator

1. Start emulator: `flutter emulators --launch Pixel_4`
2. Ensure React + API are running (above)
3. Run Flutter shell:
```powershell
cd frontend
flutter pub get
flutter run -d emulator-5554
```

The Flutter app loads the React UI via WebView at `http://10.0.2.2:5173`.

### If Gradle fails with SSL / PKIX error

Your PC cannot verify HTTPS certificates (common on school/corporate networks).

**Fix options:**
1. Install your organization’s root CA certificate into Windows + Java
2. Or move the project **out of OneDrive** to `C:\dev\ai-video`
3. Run the **browser** instead of emulator: open `http://localhost:5173`

**Windows desktop (no Gradle):**
```powershell
cd frontend
flutter run -d windows
```

---

## API flow

```
React UI  →  POST http://localhost:8000/generate
Backend   →  ComfyUI http://127.0.0.1:8188/prompt
ComfyUI   →  returns image/video URL
React     →  displays in VideoPlayer
```

---

## ComfyUI requirements

- At least one **checkpoint** in `ComfyUI/models/checkpoints/`
- ComfyUI running before generating

Without ComfyUI you’ll see: *"ComfyUI is not running"* with a **Retry** button.
