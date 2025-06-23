# utils/stt.py
import whisper
import pyaudio
import wave
import threading

MODEL = whisper.load_model("base")
TEMP_FILE = "temp_live.wav"
recording = False

def record_and_transcribe_async():
    """Start recording in background thread."""
    global recording
    recording = True
    thread = threading.Thread(target=_record_audio)
    thread.start()
    return "Recording..."

def _record_audio():
    global recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(TEMP_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def stop_and_transcribe(lang_code="en"):
    """Stop recording and return transcribed text in the specified language (e.g., 'hi' for Hindi)."""
    global recording
    recording = False
    result = MODEL.transcribe(TEMP_FILE, language=lang_code)
    return result["text"].strip()







