import tkinter as tk
from tkinter import messagebox
from live_transcribe import record_audio, transcribe_audio
from utils.grammar import correct_grammar
from utils.translator import translate_indian_to_us
from subtitle_overlay import subtitle_screen
from utils.tts import speak_text  # ✅ NEW
# Keep the rest as-is...

def run_transcription():
    try:
        audio_file = record_audio()
        text = transcribe_audio(audio_file)
        corrected = correct_grammar(text)
        final = translate_indian_to_us(corrected)
        
        subtitle_screen(final, duration=5)
        result_text.set(final)
        speak_text(final)  # ✅ Speak it out loud
    except Exception as e:
        messagebox.showerror("Error", str(e))


# UI setup
root = tk.Tk()
root.title("Indian English → US English (Live Caption)")

tk.Label(root, text="🎙️ Speak for 5 seconds").pack(pady=10)
tk.Button(root, text="Start", command=run_transcription, font=("Arial", 14)).pack(pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=400, font=("Arial", 12), fg="blue").pack(pady=10)

root.mainloop()
