from record_audio import record_audio
from voice_stt import transcribe_audio
from voice_tts import speak_text
from gemini_engine import extract_meeting_details
from calendar_utils import find_free_slots

def voice_scheduler():
    record_audio(5)
    user_text = transcribe_audio("audio.wav")
    print("🧠 User said:", user_text)

    parsed = extract_meeting_details(user_text)
    if not parsed:
        speak_text("Sorry, I couldn't understand your request.")
        return

    slots = find_free_slots(duration_minutes=parsed["duration"])
    day = parsed["preferred_day"].lower()
    time_pref = parsed["time_range"]

    filtered = []
    for start, end in slots:
        if day in start.strftime('%A').lower():
            if time_pref == "morning" and start.hour < 12:
                filtered.append((start, end))
            elif time_pref == "afternoon" and 12 <= start.hour <= 17:
                filtered.append((start, end))

    if not filtered:
        speak_text(f"You're fully booked on {day.title()}. Want to try another day?")
        return

    suggestions = [s.strftime('%I:%M %p') for s, _ in filtered[:2]]
    text = f"I found {suggestions[0]} or {suggestions[1]} on {parsed['preferred_day']}. Which one do you prefer?"
    print("🤖:", text)
    speak_text(text)
