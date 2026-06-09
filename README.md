# Voice Workspace

Unified voice synthesis and cloning environment for Ralph's projects.

## Status

| Tool | Status | Port | Notes |
|------|--------|------|-------|
| **OmniVoice Studio** | ✅ Live | 3900 | TTS + voice cloning + dubbing. MPS backend active. |
| **Voicebox** | ✅ Live | 17493 | 7 TTS engines (Kokoro, Qwen, LuxTTS, etc.). Qwen3-TTS downloading (~4.5 GB). |
| **Miso TTS 8B** | ⚠️ Memory-limited | N/A | 31 GB downloaded, requires ~24 GB VRAM. Cannot load on 24 GB unified memory. |

## Hardware
- Mac Mini M4 Pro, 24 GB unified memory
- MPS available (Apple Silicon Metal GPU)
- 81 GB disk free

---

## OmniVoice Studio (Production)

Fast, zero-shot voice cloning and multilingual TTS.

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
- `POST http://localhost:3900/generate` — generate speech (multipart)
- `POST http://localhost:3900/v1/audio/speech` — OpenAI-compatible TTS
- `POST http://localhost:3900/v1/audio/transcriptions` — Whisper transcription

### Voice Cloning
```bash
curl -s -X POST http://localhost:3900/generate \
  -F "text=Hello, this is my cloned voice speaking." \
  -F "language=en" \
  -F "ref_audio=@your_voice_sample.wav" \
  -F "ref_text=Transcript of your sample." \
  -o cloned.wav
```

---

## Voicebox (Feature-Rich Studio)

7-engine voice studio with profiles, effects, and agent integration.

### Start
```bash
cd /Users/ralph/voice-workspace/voicebox
export PYTHONPATH=/Users/ralph/voice-workspace/voicebox/backend
backend/.venv/bin/python -m backend.main --host 0.0.0.0 --port 17493
```

### Endpoints
- `GET http://localhost:17493/health` — server status
- `GET http://localhost:17493/docs` — Swagger UI
- `GET http://localhost:17493/profiles` — list voice profiles
- `POST http://localhost:17493/profiles` — create a profile
- `POST http://localhost:17493/speak` — generate speech
- `POST http://localhost:17493/transcribe` — STT

### Create Profile + Generate
```bash
# Create a Kokoro profile
curl -s -X POST http://localhost:17493/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "My Voice", "engine": "kokoro", "voice_id": "af_bella", "language": "en"}'

# Generate (use returned profile id)
curl -s -X POST http://localhost:17493/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from Voicebox.", "profile": "<profile_id>"}'
```

---

## Miso TTS 8B (Cloud GPU Target)

8B-parameter open-weight expressive TTS. Requires high VRAM.

```bash
cd /Users/ralph/voice-workspace/MisoTTS
# Requires 24+ GB VRAM. Runs on RunPod, Vast.ai, or local A100.
.venv/bin/python run_misotts.py
```

**Options:**
- RunPod A100 40GB: ~$1.50/hr
- Vast.ai RTX 4090 24GB: ~$0.40/hr

---

## Integration Script

`/Users/ralph/voice-workspace/scripts/voice_generate.py`

```bash
# OmniVoice wrapper
python3 scripts/voice_generate.py generate \
  -t "Your text here" -o output.wav

python3 scripts/voice_generate.py health
```

---

## Comparison

| Feature | OmniVoice | Voicebox | Miso 8B |
|---------|-----------|----------|---------|
| Voice cloning | ✅ Zero-shot | ✅ Zero-shot | ✅ Prompt-based |
| Engines | 1 (built-in) | 7 (Kokoro, Qwen, LuxTTS, Chatterbox, etc.) | 1 (Miso) |
| Languages | 600+ | 23+ | English only |
| Emotive speech | Good | Excellent (paralinguistic tags) | Excellent (best-in-class) |
| Latency | Fast | Medium (model download on first use) | Slow (8B params) |
| Local RAM/VRAM | ~2 GB | ~2–4 GB | ~24 GB |
| API | FastAPI + OpenAI-compat | FastAPI + MCP | Python API |
| Audio effects | No | Yes (pitch, reverb, chorus, etc.) | No |
| Video dubbing | Yes | No | No |
| Dictation (STT) | No | Yes (global hotkey) | No |

---

## Project Integration

| Project | Domain | Use Case |
|---------|--------|----------|
| MENA Electrical | ee.photogralph.com | Training narration for Albert |
| Chicago PCB CRM | deep.photogralph.com | AI call summaries, voice notes |
| Tennis Manager | tennis.photogralph.com | Announcements, alerts |

---

## Repo

**`hollywoodralph/voice-workspace`** — GitHub
