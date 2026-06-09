# Voice Workspace

Unified voice synthesis and cloning environment for Ralph's projects.

## Status

| Tool | Status | Notes |
|------|--------|-------|
| **OmniVoice Studio** | ✅ Live on port 3900 | TTS + voice cloning + dubbing. MPS (Apple Silicon) backend active. |
| **Miso TTS 8B** | ⚠️ Memory-limited | 31 GB downloaded, but 8B model requires ~24 GB VRAM. Cannot load on 24 GB unified memory. CPU path possible but slow. |

## Hardware
- Mac Mini M4 Pro, 24 GB unified memory
- MPS available (Apple Silicon Metal GPU)
- 81 GB disk free

## OmniVoice Studio (Production)

### Start
```bash
cd /Users/ralph/voice-workspace/OmniVoice-Studio
export OMNIVOICE_BIND_HOST=0.0.0.0
export OMNIVOICE_SERVER_MODE=1
export OMNIVOICE_DATA_DIR=/Users/ralph/voice-workspace/omnivoice_data
uv run python backend/main.py
```

### Endpoints
- `GET http://localhost:3900/health` — server status
- `GET http://localhost:3900/system/info` — system info
- `GET http://localhost:3900/engines` — list TTS/ASR engines
- `POST http://localhost:3900/generate` — generate speech (multipart/form-data)
  - `text` (required)
  - `language` (optional, e.g. `en`)
  - `ref_audio` (optional, UploadFile) — voice clone reference
  - `ref_text` (optional) — transcript of reference audio
- `POST http://localhost:3900/v1/audio/speech` — OpenAI-compatible endpoint
- `POST http://localhost:3900/v1/audio/transcriptions` — Whisper transcription

### Voice Cloning Example
```bash
curl -s -X POST http://localhost:3900/generate \
  -F "text=Hello, this is my cloned voice speaking." \
  -F "language=en" \
  -F "ref_audio=@/path/to/your/voice_sample.wav" \
  -F "ref_text=This is the transcript of my voice sample." \
  -o output_cloned.wav
```

## Miso TTS 8B (Future / Cloud GPU)

```bash
cd /Users/ralph/voice-workspace/MisoTTS
# Requires 24+ GB VRAM. Runs on RunPod, Vast.ai, or local A100.
uv sync --python 3.11
.venv/bin/python run_misotts.py
```

## Projects Integration

| Project | Domain | Use Case |
|---------|--------|----------|
| MENA Electrical | ee.photogralph.com | Training narration for Albert |
| Chicago PCB CRM | deep.photogralph.com | AI call summaries, voice notes |
| Tennis Manager | tennis.photogralph.com | Announcements, alerts |

## Cron Integration

Voice generation can be called from cron jobs via the local API:
```bash
curl -s -X POST http://localhost:3900/generate \
  -F "text=$TEXT" \
  -F "language=en" \
  -o /tmp/voice_output.wav
```
