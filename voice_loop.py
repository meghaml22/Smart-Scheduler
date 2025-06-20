from record_audio import record_audio
from voice_stt import transcribe_audio
from voice_tts import speak_text

def voice_conversation():
    record_audio(5)  # Step 1: Record
    user_text = transcribe_audio("audio.wav")  # Step 2: Transcribe
    print("User said:", user_text)

    # Example: Use hardcoded response (can connect GPT here later)
    bot_reply = "Got it. I'm checking for 1-hour slots on Tuesday afternoon."
    print("Bot says:", bot_reply)
    speak_text(bot_reply)  # Step 3: Speak back
