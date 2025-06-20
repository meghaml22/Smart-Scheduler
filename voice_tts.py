from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key="sk_d9f5eb33f3c4c3314adcedda58db94a36cb0cab279b95af5")

def speak_text(text, voice_id="EXAVITQu4vr4xnSDxMaL"):  # Default: Rachel
    # Generate audio using the correct structure
    audio = client.text_to_speech.convert(
        text=text,
        model_id="eleven_multilingual_v2",
        voice_id=voice_id,
    )
    play(audio)
