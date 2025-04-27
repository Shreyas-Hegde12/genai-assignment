import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import threading
import os
from TTS.api import TTS
import pygame

# Initialize TTS model once
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Predefined characters
CHARACTERS = {
    "Trump": "characters-voices/trump.wav",
    "Obama": "characters-voices/obama.wav",
    "Modi": "characters-voices/modi.wav",
}

# Initialize pygame for audio playback
pygame.mixer.init()

# Function to handle TTS generation
def generate_speech():
    text = text_entry.get("1.0", tk.END).strip()
    character = character_choice.get()
    speaker_wav = CHARACTERS.get(character)

    if not text:
        messagebox.showerror("Error", "Please enter some text.")
        return

    loading_label.config(text="Loading...")
    root.update_idletasks()

    def worker():
        try:
            tts.tts_to_file(
                text=text,
                file_path="output.wav",
                speaker_wav=speaker_wav,
                language="en"
            )
            loading_label.config(text="Done!")
            play_audio()
        except Exception as e:
            loading_label.config(text="Error")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=worker).start()

# Function to play audio
def play_audio():
    if os.path.exists("output.wav"):
        pygame.mixer.music.load("output.wav")
        pygame.mixer.music.play()

# Build UI
root = tk.Tk()
root.title("Voice Cloner")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Dropdown for characters
character_choice = ttk.Combobox(root, values=list(CHARACTERS.keys()), state="readonly")
character_choice.current(0)
character_choice.pack(pady=10)

# Text box
text_entry = tk.Text(root, height=8, width=40)
text_entry.pack(pady=10)

# Generate button
generate_button = ttk.Button(root, text="Generate Voice", command=generate_speech)
generate_button.pack(pady=10)

# Loading label
loading_label = tk.Label(root, text="", bg="#f0f0f0", fg="blue")
loading_label.pack(pady=5)

# Main loop
root.mainloop()
