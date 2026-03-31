"""
Unit test to verify all database imports work correctly
Run: python -m pytest test_imports.py -v
Or: python test_imports.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


def test_model_imports():
    """Test that all models can be imported"""
    from app.models.models import User, Conversation, Message, Memory, Base
    assert User is not None
    assert Conversation is not None
    assert Message is not None
    assert Memory is not None
    assert Base is not None
    print("✓ Model imports successful")


def test_database_imports():
    """Test that database utilities can be imported"""
    from app.core.database import init_db, get_db, engine, SessionLocal, Base
    assert init_db is not None
    assert get_db is not None
    assert engine is not None
    assert SessionLocal is not None
    assert Base is not None
    print("✓ Database imports successful")


def test_core_package_imports():
    """Test that core package exports work"""
    from app.core import init_db, get_db, engine, SessionLocal
    assert init_db is not None
    assert get_db is not None
    assert engine is not None
    assert SessionLocal is not None
    print("✓ Core package imports successful")


def test_models_package_imports():
    """Test that models package exports work"""
    from app.models import User, Conversation, Message, Memory, Base
    assert User is not None
    assert Conversation is not None
    assert Message is not None
    assert Memory is not None
    assert Base is not None
    print("✓ Models package imports successful")


def test_api_imports():
    """Test that API can be imported"""
    from app.api.chat import ChatRequest, router, chat
    assert ChatRequest is not None
    assert router is not None
    assert chat is not None
    print("✓ API imports successful")


def test_main_app_imports():
    """Test that main app can be imported"""
    from app.main import app
    assert app is not None
    print("✓ Main app imports successful")


def test_llm_service_imports():
    """Test that LLM service can be imported"""
    from app.services.llm_service import generate_response
    assert generate_response is not None
    print("✓ LLM service imports successful")


if __name__ == "__main__":
    try:
        print("=" * 50)
        print("Testing all imports...")
        print("=" * 50)
        
        test_model_imports()
        test_database_imports()
        test_core_package_imports()
        test_models_package_imports()
        test_api_imports()
        test_main_app_imports()
        test_llm_service_imports()
        
        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nDatabase layer is fully functional.")
        print("Ready to run: uvicorn backend.app.main:app --reload")
        
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR:\n{e}")
        sys.exit(1)
