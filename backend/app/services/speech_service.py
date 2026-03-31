"""
Speech I/O Service - Phase 2
Handles speech-to-text (Whisper) and text-to-speech (TTS)
"""

import whisper
import pyttsx3
import os
import tempfile
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Initialize Whisper model (cached after first load)
WHISPER_MODEL = None

def get_whisper_model(model_size: str = "base"):
    """Load Whisper model (cached)"""
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        logger.info(f"Loading Whisper model: {model_size}")
        WHISPER_MODEL = whisper.load_model(model_size)
    return WHISPER_MODEL


def transcribe_audio(audio_file_path: str, language: str = None) -> str:
    """
    Transcribe audio file to text using Whisper
    
    Args:
        audio_file_path: Path to audio file (WAV, MP3, etc.)
        language: Language code (e.g., 'en', 'es'). None = auto-detect
        
    Returns:
        Transcribed text
    """
    try:
        model = get_whisper_model()
        
        logger.info(f"Transcribing audio: {audio_file_path}")
        result = model.transcribe(audio_file_path, language=language)
        
        text = result.get("text", "").strip()
        logger.info(f"Transcription complete: {len(text)} characters")
        
        return text
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return f"Error: Could not transcribe audio - {str(e)}"


def synthesize_speech(text: str, output_file_path: str = None, rate: int = 150) -> str:
    """
    Synthesize text to speech using pyttsx3
    
    Args:
        text: Text to convert to speech
        output_file_path: Path to save audio file. If None, creates temp file
        rate: Speech rate (words per minute)
        
    Returns:
        Path to generated audio file
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        
        # Use provided path or create temp file
        if output_file_path is None:
            temp_dir = tempfile.gettempdir()
            output_file_path = os.path.join(temp_dir, f"arise_tts_{int(time.time())}.mp3")
        
        logger.info(f"Synthesizing speech: {len(text)} characters -> {output_file_path}")
        engine.save_to_file(text, output_file_path)
        engine.runAndWait()
        
        logger.info(f"Speech synthesis complete: {output_file_path}")
        return output_file_path
        
    except Exception as e:
        logger.error(f"Speech synthesis error: {str(e)}")
        raise


def quick_speak(text: str) -> None:
    """
    Quickly speak text without saving to file
    
    Args:
        text: Text to speak
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        logger.info(f"Spoke text: {len(text)} characters")
    except Exception as e:
        logger.error(f"Quick speak error: {str(e)}")


# Try to import time (may not be available in all environments)
try:
    import time
except ImportError:
    import sys
    class time:
        @staticmethod
        def time():
            return 0
