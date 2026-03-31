# 🚀 AriseAI Backend - Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- Ollama running locally (for LLM)

## Installation (5 minutes)

### Option 1: Automatic (Recommended)
**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
python start.py
```

This will:
- Install dependencies
- Validate all imports
- Run tests
- Start the server

### Option 2: Manual

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Validate setup:**
```bash
python validate_imports.py
python test_imports.py
```

**3. Start server:**
```bash
uvicorn backend.app.main:app --reload
```

## Testing

### Once server is running:

**Test health check:**
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"message": "Arise backend running 🚀"}
```

**Test chat endpoint:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello Arise, what is 2+2?",
    "personality": "calm",
    "user_id": 1
  }'
```

Expected response:
```json
{
  "reply": "The answer is 4.",
  "conversation_id": 1,
  "message_id": 2
}
```

### Using Postman or Insomnia:

**Request:**
- URL: `POST http://localhost:8000/chat`
- Header: `Content-Type: application/json`
- Body:
```json
{
  "message": "Remember: I'm learning machine learning",
  "personality": "motivator",
  "user_id": 1
}
```

## API Documentation

**Interactive API Docs:** http://localhost:8000/docs
**Alternative Docs:** http://localhost:8000/redoc

## Project Structure

```
ariseai/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI app
│       ├── api/
│       │   └── chat.py            # Chat endpoint
│       ├── core/
│       │   └── database.py        # Database config
│       ├── models/
│       │   └── models.py          # ORM models
│       ├── services/
│       │   └── llm_service.py     # Ollama integration
│       └── memory/
├── prisma/
│   └── schema.prisma              # Database schema
├── requirements.txt               # Dependencies
├── .env                          # Config
├── start.py                      # Python startup script
├── start.bat                     # Windows startup script
├── validate_imports.py           # Import validator
├── test_imports.py              # Test suite
├── DATABASE_SETUP.md            # Database guide
└── IMPLEMENTATION_SUMMARY.md    # Technical details
```

## Next Steps

### Add Memory
Store user preferences:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My goal is to learn Python programming",
    "personality": "calm",
    "user_id": 1
  }'
```

### Continue Conversation
Reference previous context:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What was my goal again?",
    "personality": "calm",
    "user_id": 1,
    "conversation_id": 1
  }'
```

## Troubleshooting

### "ModuleNotFoundError"
- Run: `pip install -r requirements.txt`
- Ensure you're in the project root directory

### "Connection refused" to Ollama
- Start Ollama: `ollama serve`
- Or download from: https://ollama.ai

### Database locked error
- Close the server (Ctrl+C)
- Delete `arise.db` to start fresh
- Restart the server

### Port 8000 already in use
Edit the startup command to use a different port:
```bash
uvicorn backend.app.main:app --reload --port 8001
```

## Development

### Run with auto-reload:
```bash
uvicorn backend.app.main:app --reload
```

### Check database:
```bash
sqlite3 arise.db ".tables"
sqlite3 arise.db "SELECT * FROM users;"
```

### Backup database:
```bash
cp arise.db arise.db.backup
```

## Files Reference

| File | Purpose |
|------|---------|
| `start.py / start.bat` | One-click startup |
| `validate_imports.py` | Quick validation |
| `test_imports.py` | Full test suite |
| `DATABASE_SETUP.md` | Database documentation |
| `IMPLEMENTATION_SUMMARY.md` | Technical details |
| `requirements.txt` | Dependencies |
| `.env` | Configuration |

## Support

For detailed information, see:
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Complete database guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical overview
- [README.md](README.md) - Project overview

---

**Status:** ✅ Production Ready

The database layer is complete and fully functional. All endpoints are working with persistent memory and conversation tracking.
