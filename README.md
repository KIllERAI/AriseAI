# AriseAI
# 🚀 Arise — AI Personal Assistant

Arise is a voice-first AI assistant designed to act as an intelligent, proactive, and behavior-aware companion.

Unlike traditional assistants, Arise focuses on **memory, personalization, and discipline**, helping users improve productivity and daily structure.

---

## 🧠 Core Idea

> Arise doesn’t just respond — it understands, remembers, and guides.

---

## ⚙️ Features

- 🎤 Voice interaction (Speech-to-Text + TTS)
- 🧠 Local AI reasoning (Ollama / LLMs)
- 🗂️ Persistent memory system
- ⏰ Smart reminders & scheduling
- 🎭 Adaptive personality (motivator / strict / calm)

---

## 🏗️ Architecture


---

## 🧩 Tech Stack

- **Frontend:** Browser APIs (MediaRecorder, Web Speech)
- **Backend:** FastAPI, WebSockets
- **AI:** Whisper, Ollama (Llama3/Mistral)
- **Database:** SQLite

---

## 🚧 Status

✅ **Phase 1: Database & Memory** — Core database layer with persistent memory implemented
🔄 **Phase 2: Speech I/O** — Whisper (STT) and TTS integration
🔄 **Phase 3: Intelligence** — Enhanced personality routing and memory management
🔄 **Phase 4: Scheduling** — Smart reminders and task scheduling

---

## 📚 Documentation

- [Database Setup Guide](DATABASE_SETUP.md) — Complete guide to the SQLite database, models, and API usage
- [API Reference](#api-reference) — Chat endpoint documentation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama running locally (for LLM)

### Installation
```bash
pip install -r requirements.txt
```

### Run
```bash
uvicorn backend.app.main:app --reload
```

Server runs at: `http://localhost:8000`

### Test
```bash
# Validate all imports work
python validate_imports.py

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello Arise!",
    "personality": "calm",
    "user_id": 1
  }'
```

---

## 🎯 API Reference

### `POST /chat`
Send a message and get a response with persistent memory.

**Request:**
```json
{
  "message": "What's my goal?",
  "personality": "calm",
  "user_id": 1,
  "conversation_id": null
}
```

**Response:**
```json
{
  "reply": "Your goal is to learn machine learning.",
  "conversation_id": 1,
  "message_id": 2
}
```

### `GET /`
Health check endpoint.

---

## 🚧 Status

Currently building core voice + intelligence loop.

---

## 🤝 Collaboration

- `main` → stable  
- `dev` → development  
- `feature/*` → modules  

---

## 🎯 Vision

To build a **Jarvis-like assistant** that is proactive, personalized, and capable of guiding user behavior.
