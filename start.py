#!/usr/bin/env python3
"""
AriseAI Backend Setup and Startup Script
This script handles all initial setup steps and starts the FastAPI server
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        print(f"✅ {description} complete")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 AriseAI Backend - Setup & Startup")
    print("=" * 60)
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if dependencies are installed
    print("\n🔍 Checking environment...")
    try:
        import fastapi
        print("✅ Dependencies already installed")
    except ImportError:
        print("❌ Dependencies not found. Installing...")
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
            print("Failed to install dependencies")
            return False
    
    # Validate imports
    print("\n🔍 Validating imports...")
    if not run_command(f"{sys.executable} validate_imports.py", "Validating imports"):
        print("⚠️  Import validation failed")
        return False
    
    # Run tests
    print("\n🧪 Running tests...")
    if not run_command(f"{sys.executable} test_imports.py", "Running import tests"):
        print("⚠️  Tests failed")
        return False
    
    # Start server
    print("\n" + "=" * 60)
    print("🚀 Starting FastAPI Server...")
    print("=" * 60)
    print("\n📍 Server running at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop\n")
    
    cmd = f"{sys.executable} -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"
    os.system(cmd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
