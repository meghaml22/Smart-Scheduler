import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use stateless model
model = genai.GenerativeModel('gemini-1.5-flash')

def chat_with_gemini(user_input: str) -> str:
    chat = model.start_chat(history=[])
    response = chat.send_message(user_input)
    return response.text

def extract_meeting_details(text: str) -> dict:
    prompt = f"""
    You are a scheduling assistant. Extract meeting details from the text below:
    
    "{text}"

    Return JSON in this format:
    {{
        "duration": 30,
        "preferred_day": "Thursday",
        "time_range": "afternoon"
    }}
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except Exception:
        return {}

def extract_with_constraints(text: str) -> dict:
    prompt = f"""
    Extract meeting request from:
    "{text}"

    Return structured JSON with optional constraints like:
    {{
        "duration": 45,
        "deadline": "2025-06-20T18:00:00",
        "latest_end": "2025-06-20T17:15:00",
        "preferred_day": "Friday",
        "time_range": "any"
    }}
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except Exception:
        return {}
