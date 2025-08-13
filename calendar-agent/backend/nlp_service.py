import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

async def extract_meeting_details(message: str):
    prompt = f"""
    Extract meeting details from the following message and return as JSON with keys: title, datetime, attendees, link, duration_minutes.
    Message: {message}
    """
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        # Gemini returns text, so parse JSON from response
        import json
        try:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
        except Exception:
            return None
