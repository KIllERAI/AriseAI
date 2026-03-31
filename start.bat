@echo off
REM AriseAI Backend - Windows Startup Script

echo.
echo ============================================================
echo   ^>^> AriseAI Backend - Setup ^& Startup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Validate imports
echo.
echo Validating imports...
python validate_imports.py
if errorlevel 1 (
    echo WARNING: Import validation failed
    pause
    exit /b 1
)

REM Run tests
echo.
echo Running import tests...
python test_imports.py
if errorlevel 1 (
    echo WARNING: Tests failed
    pause
    exit /b 1
)

REM Start server
echo.
echo ============================================================
echo   ^>^> Starting FastAPI Server
echo ============================================================
echo.
echo Server will run at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo Press Ctrl+C to stop
echo.

python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

pause
