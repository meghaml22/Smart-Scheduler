import whisper

def transcribe_audio(filename="audio.wav"):
    model = whisper.load_model("base")  # or "small", "medium", "large"
    result = model.transcribe(filename)
    print("📝 Transcription:", result["text"])
    return result["text"]
