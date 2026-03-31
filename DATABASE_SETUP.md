# AriseAI Database Setup Guide

## Overview
The AriseAI backend uses **SQLAlchemy ORM** with **SQLite** database. The schema is defined in both Prisma and Python for flexibility.

## Database Schema

### Models (Tables)

#### User
- `id` (Integer): Primary key
- `name` (String): User name
- `personality_type` (String): Default personality ("calm", "strict", "motivator", etc.)
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

#### Conversation
- `id` (Integer): Primary key
- `user_id` (Integer): Foreign key to User
- `title` (String): Chat title (default: "Untitled Chat")
- `created_at` (DateTime): Conversation creation timestamp
- `updated_at` (DateTime): Last update timestamp

#### Message
- `id` (Integer): Primary key
- `conversation_id` (Integer): Foreign key to Conversation
- `role` (String): "user" or "assistant"
- `content` (Text): Message content
- `created_at` (DateTime): Message timestamp

#### Memory
- `id` (Integer): Primary key
- `user_id` (Integer): Foreign key to User
- `key` (String): Memory context type ("goals", "preferences", "behavior", etc.)
- `value` (Text): What Arise remembers about the user
- `created_at` (DateTime): Memory creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `httpx` - HTTP client for Ollama
- `python-dotenv` - Environment variable management

### 2. Configure Environment
Create or verify `.env` file:
```
DATABASE_URL="sqlite:///./arise.db"
```

### 3. Verify Setup
Run the import validation script:
```bash
python validate_imports.py
```

Expected output:
```
✓ Testing imports...
  ✓ Models imported successfully
  ✓ Database utilities imported successfully
  ✓ Chat API imported successfully
  ✓ LLM service imported successfully
  ✓ FastAPI app imported successfully

✅ All imports successful! Database layer is ready.
```

### 4. Start the Server
```bash
uvicorn backend.app.main:app --reload
```

Server runs at: `http://localhost:8000`

## API Usage

### Chat Endpoint: `POST /chat`

**Request:**
```json
{
  "message": "Hello Arise!",
  "personality": "calm",
  "user_id": 1,
  "conversation_id": null
}
```

**Response:**
```json
{
  "reply": "AI response here",
  "conversation_id": 1,
  "message_id": 2
}
```

**Features:**
- Automatically creates new conversation if `conversation_id` is null
- Automatically creates user if user_id doesn't exist
- Fetches user's memory before calling LLM
- Saves both user and assistant messages to database
- Persists memory context for future interactions

### Root Endpoint: `GET /`

**Response:**
```json
{
  "message": "Arise backend running 🚀"
}
```

## Database Operations

### Query Examples

**Get all conversations for a user:**
```python
from sqlalchemy.orm import Session
from app.models import Conversation

conversations = db.query(Conversation).filter(Conversation.user_id == 1).all()
```

**Get all messages in a conversation:**
```python
messages = db.query(Message).filter(Message.conversation_id == 1).all()
```

**Get user's memory:**
```python
memories = db.query(Memory).filter(Memory.user_id == 1).all()
```

**Add new memory:**
```python
from app.models import Memory

memory = Memory(
    user_id=1,
    key="goals",
    value="Learn machine learning"
)
db.add(memory)
db.commit()
```

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py            # Chat endpoint
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py        # Database config & session
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy models
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py     # Ollama integration
│   ├── memory/
│   │   └── __init__.py
│   └── core/
│       └── __init__.py
├── __init__.py
prisma/
├── schema.prisma              # Prisma schema (reference only)
├── migrations/                # Generated migrations
arise.db                        # SQLite database (auto-created)
.env                           # Environment variables
requirements.txt               # Python dependencies
validate_imports.py            # Import validation script
```

## Key Features Implemented

✅ **Persistent Memory** - User data and conversation history stored in database
✅ **Multi-User Support** - Each user has separate conversations and memory
✅ **Message Logging** - All interactions tracked with timestamps
✅ **Context Retrieval** - User memory fetched before each LLM call
✅ **Cascading Deletes** - Deleting user deletes all related data
✅ **Auto-Initialization** - Database creates tables on first run

## Next Steps

1. **Speech Integration** - Add Whisper (STT) and TTS endpoints
2. **Memory Management** - Implement smart memory updating logic
3. **Personality Adaptation** - Enhance personality-based routing
4. **Scheduling** - Add reminder and scheduling system
5. **Testing** - Write unit tests for database operations

## Troubleshooting

**Error: "ModuleNotFoundError: No module named 'app'"**
- Ensure you're running from the project root
- Install dependencies: `pip install -r requirements.txt`
- Run: `uvicorn backend.app.main:app --reload`

**Error: "sqlite3.OperationalError: unable to open database file"**
- Check .env DATABASE_URL is correct
- Ensure `backend/` directory is writable

**Database locked error**
- Close other processes using the database
- Delete `arise.db` to restart fresh (will lose all data)

## Database Backup

To backup your database:
```bash
cp arise.db arise.db.backup
```

To restore:
```bash
cp arise.db.backup arise.db
```
