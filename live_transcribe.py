import whisper
import pyaudio
import wave
import os
import string  # ✅ Needed for cleaning

MODEL = whisper.load_model("base")
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
TEMP_FILE = "temp_live.wav"

def record_audio():
    p = pyaudio.PyAudio()
    print("🎙️ Recording from mic...")
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(TEMP_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return TEMP_FILE

def transcribe_audio(path):
    print("🧠 Transcribing...")
    result = MODEL.transcribe(path)
    text = result["text"]

    # ✅ Clean non-printable characters
    cleaned_text = ''.join(filter(lambda x: x in string.printable, text))
    return cleaned_text

if __name__ == "__main__":
    audio_path = record_audio()
    text = transcribe_audio(audio_path)
    print("📜 Transcribed Text:", text)
    os.remove(audio_path)

    
