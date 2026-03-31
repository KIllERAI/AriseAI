"""
Speech I/O API Endpoints - Phase 2
Routes for speech-to-text and text-to-speech operations
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import tempfile
import logging
from app.services.speech_service import transcribe_audio, synthesize_speech

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/speech", tags=["speech"])


class TranscribeResponse(BaseModel):
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None
    model: str = "whisper"


class SynthesizeRequest(BaseModel):
    text: str
    rate: int = 150  # Words per minute


class SynthesizeResponse(BaseModel):
    audio_url: str
    text_length: int
    duration_estimate: float


class VoiceChatRequest(BaseModel):
    """Combined voice chat request"""
    user_id: int
    conversation_id: Optional[int] = None
    personality: str = "calm"
    audio_file_path: Optional[str] = None  # For pre-uploaded audio


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_endpoint(
    audio: UploadFile = File(...),
    language: Optional[str] = None
):
    """
    Transcribe audio file to text using Whisper
    
    Returns:
        - text: Transcribed text
        - language: Detected language code
    """
    try:
        # Save uploaded file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, audio.filename or "audio.wav")
        
        with open(temp_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        logger.info(f"Received audio file: {audio.filename} ({len(content)} bytes)")
        
        # Transcribe
        text = transcribe_audio(temp_path, language=language)
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return TranscribeResponse(
            text=text,
            language=language,
            model="whisper"
        )
        
    except Exception as e:
        logger.error(f"Transcribe endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize_endpoint(request: SynthesizeRequest):
    """
    Convert text to speech
    
    Returns:
        - audio_url: URL to generated audio file
        - text_length: Length of input text
        - duration_estimate: Estimated audio duration in seconds
    """
    try:
        if not request.text or len(request.text) < 1:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Estimate duration (rough: 150 words/min = 2.5 chars per second)
        text_length = len(request.text)
        duration_estimate = (text_length / 150) * 2.4  # Rough estimate
        
        logger.info(f"Synthesizing: {text_length} characters, rate={request.rate} wpm")
        
        # Generate TTS audio
        audio_path = synthesize_speech(
            request.text,
            rate=request.rate
        )
        
        # Return path relative to server (in production, upload to storage)
        audio_filename = os.path.basename(audio_path)
        audio_url = f"/api/v1/speech/audio/{audio_filename}"
        
        return SynthesizeResponse(
            audio_url=audio_url,
            text_length=text_length,
            duration_estimate=duration_estimate
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Synthesize endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Retrieve generated audio file
    """
    try:
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, filename)
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        # Return audio file as streaming response
        from fastapi.responses import FileResponse
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get audio error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/status")
async def speech_status():
    """
    Get speech service status
    """
    return {
        "whisper": "ready",
        "tts": "ready",
        "transcribe_endpoint": "/api/v1/speech/transcribe",
        "synthesize_endpoint": "/api/v1/speech/synthesize",
        "phase": "2 - Speech I/O",
        "status": "operational"
    }
