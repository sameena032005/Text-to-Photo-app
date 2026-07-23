# AI Video Generator — React Frontend

Premium dark-mode UI for text-to-video generation with ComfyUI backend integration.

## Stack

- React 18 + Vite 6
- Tailwind CSS v4
- Framer Motion
- Axios
- React Router

## Quick start

```bash
cd react-frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Environment

Copy `.env.example` to `.env`:

```
VITE_API_URL=http://localhost:8000
```

You can also set the API URL in **Settings** (persisted in localStorage).

## Backend API

The app expects:

**POST** `{API_URL}/generate`

```json
{
  "prompt": "A futuristic city...",
  "style": "Cinematic",
  "duration": 10,
  "ratio": "16:9",
  "quality": "medium"
}
```

**Response:**

```json
{
  "video_url": "https://..."
}
```

Vite dev server proxies `/api` → `localhost:8000` if you prefer relative URLs.

## Project structure

```
src/
  api/videoApi.js
  components/
  context/AppContext.jsx
  pages/Home.jsx, Settings.jsx
  utils/constants.js
  App.jsx
  main.jsx
```

## Build

```bash
npm run build
npm run preview
```
