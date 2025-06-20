from record_audio import record_audio
from voice_stt import transcribe_audio
from voice_tts import speak_text

def test_voice_pipeline():
    # Step 1: Record your voice
    record_audio(duration=5, filename="audio.wav")

    # Step 2: Transcribe voice to text
    text = transcribe_audio("audio.wav")
    print("📝 Transcribed Text:", text)

    # Step 3: Speak a test reply (bot-style)
    reply = "Thanks! I heard you say: " + text
    print("🤖 Bot Reply:", reply)

    # Step 4: Speak it
    speak_text(reply)

test_voice_pipeline()
