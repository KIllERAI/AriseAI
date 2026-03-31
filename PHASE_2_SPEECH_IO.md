# Phase 2: Speech I/O Implementation

## Overview
Phase 2 adds voice-first capabilities to AriseAI using OpenAI Whisper for speech-to-text and pyttsx3 for text-to-speech.

## Status: IMPLEMENTED ✅

---

## New Dependencies Added

```txt
openai-whisper==20240314      # Speech-to-text
pyttsx3==2.90                 # Text-to-speech
pydub==0.25.1                 # Audio processing
soundfile==0.12.1             # Audio file I/O
numpy==1.24.3                 # Numerical operations
librosa==0.10.0               # Audio analysis
python-multipart==0.0.6       # File uploads
```

### Installation
```bash
pip install -r requirements.txt
```

---

## New Files Created

### 1. Speech Service (`backend/app/services/speech_service.py`)
Core speech processing functions:
- `transcribe_audio(audio_file_path, language)` - Speech-to-text using Whisper
- `synthesize_speech(text, output_file_path, rate)` - Text-to-speech using pyttsx3
- `quick_speak(text)` - Direct speech output without file saving
- Automatic model caching for performance

### 2. Speech API Endpoints (`backend/app/api/speech.py`)
REST endpoints on `/api/v1/speech/`:
- `POST /transcribe` - Upload audio file, get text
- `POST /synthesize` - Input text, get audio file
- `GET /audio/{filename}` - Retrieve generated audio
- `POST /status` - Check speech service status

---

## API Endpoints

### Transcribe Audio
**Endpoint:** `POST /api/v1/speech/transcribe`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/speech/transcribe" \
  -F "audio=@recording.wav" \
  -F "language=en"
```

**Response:**
```json
{
  "text": "Hello, this is a test message",
  "language": "en",
  "duration": 2.5,
  "model": "whisper"
}
```

---

### Synthesize Speech
**Endpoint:** `POST /api/v1/speech/synthesize`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/speech/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, I am Arise AI",
    "rate": 150
  }'
```

**Response:**
```json
{
  "audio_url": "/api/v1/speech/audio/arise_tts_1712003456.mp3",
  "text_length": 24,
  "duration_estimate": 3.2
}
```

---

### Get Audio File
**Endpoint:** `GET /api/v1/speech/audio/{filename}`

**Usage:**
```bash
curl "http://localhost:8000/api/v1/speech/audio/arise_tts_1712003456.mp3" \
  --output my_audio.mp3
```

---

### Check Service Status
**Endpoint:** `POST /api/v1/speech/status`

**Response:**
```json
{
  "whisper": "ready",
  "tts": "ready",
  "transcribe_endpoint": "/api/v1/speech/transcribe",
  "synthesize_endpoint": "/api/v1/speech/synthesize",
  "phase": "2 - Speech I/O",
  "status": "operational"
}
```

---

## Architecture

```
User Audio Input
    ↓
POST /transcribe (Whisper)
    ↓
Text Output
    ↓
POST /chat (Chat API - from Phase 1)
    ↓
LLM Response
    ↓
POST /synthesize (pyttsx3)
    ↓
Audio Output
    ↓
GET /audio/{filename}
    ↓
User Hears Response
```

---

## Configuration

### Speech Synthesis Rate
Adjust words-per-minute in synthesize requests:
```json
{
  "text": "Hello world",
  "rate": 100  // Slower (0-300 range)
}
```

### Language Detection
Auto-detect or specify language in transcribe:
```bash
-F "language=en"    # English
-F "language=es"    # Spanish
-F "language=fr"    # French
-F "language="      # Auto-detect
```

---

## Integration with Phase 1

The Speech I/O layer integrates seamlessly with Phase 1 database layer:
- Audio messages are converted to text via Whisper
- Text goes through existing chat API
- Response is converted back to audio via pyttsx3
- All messages still persisted to database
- Conversation history maintained

---

## Testing

### Test Transcription
```bash
# Create a test audio file (requires audio recording tools)
curl -X POST "http://localhost:8000/api/v1/speech/transcribe" \
  -F "audio=@test_audio.wav"
```

### Test Synthesis
```bash
curl -X POST "http://localhost:8000/api/v1/speech/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing text to speech"}' \
  --output test_audio.mp3
```

### Verify Status
```bash
curl -X POST "http://localhost:8000/api/v1/speech/status"
```

---

## Performance Considerations

### Whisper Model Sizes
- `tiny` - Fastest, least accurate
- `base` - Balanced (default)
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Highest accuracy, slowest

Change model size in `speech_service.py`:
```python
get_whisper_model(model_size="small")  # Instead of "base"
```

### Caching
- Whisper model is automatically cached in memory
- First transcription takes 30-60s (model loading)
- Subsequent transcriptions are fast (<5s)

---

## Next Phases

**Phase 3: Smart Memory** (2-3 weeks)
- Auto-extract key information from conversations
- Long-term memory system
- Context-aware responses

**Phase 4: Personality System** (2-3 weeks)
- Dynamic personality adaptation
- Emotion detection
- Response personalization

**Phase 5: Scheduling** (3-4 weeks)
- Reminder system
- Calendar integration
- Task scheduling

---

## Troubleshooting

### Whisper Fails to Load
```
Error: Model not found
```
**Solution:** Download model manually:
```python
import whisper
whisper.load_model("base")  # Downloads ~140MB
```

### TTS Not Working
```
Error: Engine initialization failed
```
**Solution:** Install system TTS engine:
- **Windows:** Built-in (should work automatically)
- **Mac:** `brew install espeak` or `homebrew install festival`
- **Linux:** `sudo apt-get install espeak festival`

### Audio File Format Error
```
Error: Unsupported format
```
**Solution:** Use supported formats: WAV, MP3, FLAC, M4A, OGG

---

## File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py (updated - includes speech)
│   │   ├── chat.py
│   │   └── speech.py (NEW - Phase 2)
│   ├── services/
│   │   ├── llm_service.py
│   │   └── speech_service.py (NEW - Phase 2)
│   ├── models/
│   ├── core/
│   └── main.py (updated - includes speech router)
└── requirements.txt (updated - speech dependencies)
```

---

## Summary

Phase 2 adds complete speech I/O capabilities:
- ✅ Whisper integration for speech-to-text
- ✅ pyttsx3 for text-to-speech
- ✅ REST API endpoints for both
- ✅ Audio file handling
- ✅ Service caching for performance
- ✅ Language support
- ✅ Rate control

**Status:** READY TO TEST

**Server Command:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Test with curl commands above, or integrate into frontend (Phase 2B).
