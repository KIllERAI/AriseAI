#!/usr/bin/env python3
"""
Quick validation script to verify all imports work correctly
Run this after installing requirements to ensure the database layer is working
"""

import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("✓ Testing imports...")
    
    # Test model imports
    from app.models import User, Conversation, Message, Memory, Base
    print("  ✓ Models imported successfully")
    
    # Test database imports
    from app.core import init_db, get_db, engine, SessionLocal
    print("  ✓ Database utilities imported successfully")
    
    # Test API imports
    from app.api.chat import ChatRequest
    print("  ✓ Chat API imported successfully")
    
    # Test services
    from app.services.llm_service import generate_response
    print("  ✓ LLM service imported successfully")
    
    # Test main app
    from app.main import app
    print("  ✓ FastAPI app imported successfully")
    
    print("\n✅ All imports successful! Database layer is ready.")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start the server: uvicorn backend.app.main:app --reload")
    print("3. Test the chat endpoint: POST http://localhost:8000/chat")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
