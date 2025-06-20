import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(duration=5, filename='audio.wav'):
    fs = 44100  # Sample rate
    print("🎙 Recording for", duration, "seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait for recording to finish
    write(filename, fs, recording)
    print(f"✅ Saved recording to {filename}")
