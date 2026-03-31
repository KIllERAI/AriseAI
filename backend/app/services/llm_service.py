import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_response(message: str, personality: str, memory: str):
    system_prompt = f"""
You are Arise, an AI assistant.

Personality: {personality}

Memory:
{memory}

Rules:
- Keep replies short (1-2 lines)
- Be slightly opinionated
"""

    try:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": message,
                "system": system_prompt,
                "stream": False
            },
            timeout=120
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error: {str(e)}"
