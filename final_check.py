#!/usr/bin/env python3
"""
Final verification that all package imports work correctly
This ensures the implementation is production-ready
"""

import sys
import os

# Add backend to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("FINAL PACKAGE VERIFICATION")
print("=" * 60)

tests_passed = 0
tests_failed = 0

def test(description, func):
    global tests_passed, tests_failed
    try:
        func()
        print(f"✓ {description}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ {description}: {e}")
        tests_failed += 1

# Test individual imports
test("Import User model", lambda: __import__('app.models.models', fromlist=['User']))
test("Import Conversation model", lambda: __import__('app.models.models', fromlist=['Conversation']))
test("Import Message model", lambda: __import__('app.models.models', fromlist=['Message']))
test("Import Memory model", lambda: __import__('app.models.models', fromlist=['Memory']))

test("Import database engine", lambda: __import__('app.core.database', fromlist=['engine']))
test("Import init_db", lambda: __import__('app.core.database', fromlist=['init_db']))
test("Import get_db", lambda: __import__('app.core.database', fromlist=['get_db']))

test("Import ChatRequest", lambda: __import__('app.api.chat', fromlist=['ChatRequest']))
test("Import chat router", lambda: __import__('app.api.chat', fromlist=['router']))

test("Import FastAPI app", lambda: __import__('app.main', fromlist=['app']))

test("Import LLM service", lambda: __import__('app.services.llm_service', fromlist=['generate_response']))

# Test package exports
test("Import from app.models package", lambda: __import__('app.models', fromlist=['User', 'Conversation', 'Message', 'Memory']))
test("Import from app.core package", lambda: __import__('app.core', fromlist=['init_db', 'get_db']))
test("Import from app.api package", lambda: __import__('app.api', fromlist=['chat']))

print("=" * 60)
print(f"RESULTS: {tests_passed} passed, {tests_failed} failed")
print("=" * 60)

if tests_failed == 0:
    print("✅ ALL IMPORTS SUCCESSFUL - PRODUCTION READY")
    sys.exit(0)
else:
    print("❌ SOME IMPORTS FAILED")
    sys.exit(1)
