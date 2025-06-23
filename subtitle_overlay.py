# subtitle_overlay.py - Live CC-style Subtitle Overlay

import tkinter as tk
import time
import os

class SubtitleOverlay:
    def __init__(self, update_interval=1.5):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)  # Semi-transparent

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.label = tk.Label(
            self.root,
            text="Waiting for speech...",
            font=("Segoe UI", 18, "bold"),
            bg="#000000",
            fg="#00FFAA",
            wraplength=screen_width - 100,
            justify="center",
            padx=20,
            pady=10
        )
        self.label.pack()

        self.root.geometry(f"{screen_width}x100+0+{screen_height - 120}")
        self.update_interval = update_interval
        self.file_path = "output/output.txt"

    def read_subtitle(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return ""

    def update_loop(self):
        last_text = ""
        while True:
            text = self.read_subtitle()
            if text != last_text:
                self.label.config(text=text)
                last_text = text
            self.root.update()
            time.sleep(self.update_interval)

    def start(self):
        self.update_loop()

if __name__ == "__main__":
    overlay = SubtitleOverlay()
    overlay.start()



