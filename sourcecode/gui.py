import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from gui_helper import display_matched_user_frame
from audio_processing import trim_silence
from authentication import match_recordings
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import warnings

warnings.filterwarnings("ignore")


class BiometricSystem:
    DATA_FOLDER = "data"
    ENROLLMENT_INFO_FILE = "enrollment_info.txt"

    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.current_frame = None
        self.name_value = ""
        self.color = ""
        self.audio_data = None

        self.silence_threshold_db = -46

        # Adjust the threshold for the match scores
        self.match_threshold = 0.92

        self.create_main_frame()

    def create_data_folder(self):
        # Create the data folder if it doesn't exist
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

    def create_main_frame(self):
        self.create_data_folder()

        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        enroll_button = ttk.Button(self.current_frame, text="Enroll", command=self.switch_to_name_frame)
        enroll_button.pack(pady=20)

        authenticate_button = ttk.Button(self.current_frame, text="Authenticate", command=self.authenticate_action)
        authenticate_button.pack(pady=20)

    def switch_to_name_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        name_label = tk.Label(self.current_frame, text="Enter Your Name:")
        name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.current_frame, width=30)
        self.name_entry.pack(pady=5)

        next_button = ttk.Button(self.current_frame, text="Next", command=self.switch_to_color_frame)
        next_button.pack(pady=20)

    def switch_to_color_frame(self):
        self.name_value = self.name_entry.get()  # Store the name value

        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        color_label = tk.Label(self.current_frame, text="Choose a Color:")
        color_label.pack(pady=5)

        color_button = ttk.Button(self.current_frame, text="Choose Color", command=self.choose_color)
        color_button.pack(pady=5)

        next_button = ttk.Button(self.current_frame, text="Next", command=self.switch_to_audio_frame)
        next_button.pack(pady=20)

    def switch_to_audio_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        prompt_label = tk.Label(self.current_frame, text=f"Please say a phrase\n Ex: Two blue fish swam in the tank.\n")
        prompt_label.pack(pady=10)

        record_button = ttk.Button(self.current_frame, text="Record Audio", command=self.record_audio)
        record_button.pack(pady=10)

        stop_button = ttk.Button(self.current_frame, text="Stop Recording", command=self.stop_recording)
        stop_button.pack(pady=10)

    def authenticate_action(self):

        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        prompt_label = tk.Label(self.current_frame, text="Please say a phrase\n Ex: Two blue fish swam in the tank.\n")
        prompt_label.pack(pady=10)

        record_button = ttk.Button(self.current_frame, text="Record Audio", command=self.record_audio)
        record_button.pack(pady=10)

        stop_button = ttk.Button(self.current_frame, text="Stop Recording", command=self.stop_recording_authenticate)
        stop_button.pack(pady=10)

        back_button = ttk.Button(self.current_frame, text="Back", command=self.switch_to_main_frame)
        back_button.pack(pady=10)

    def switch_to_main_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame
        self.create_main_frame()

    def record_audio(self):
        
        print(f"Recording...")
        self.audio_data = sd.rec(44100 * 5, samplerate=44100, channels=1, dtype=np.int16)
        sd.wait()

        # Trim silence using a threshold (adjust threshold as needed)
        trimmed_audio_data = trim_silence(self.audio_data, self.silence_threshold_db)

        self.audio_data = trimmed_audio_data

    def stop_recording(self):
        sd.stop()

        filename = os.path.join(self.DATA_FOLDER, f"{self.name_value}_enrollment_recording.wav")
        wav.write(filename, 44100, self.audio_data)

        print(f"Audio recorded and saved to {filename}")

        with open(os.path.join(self.DATA_FOLDER, self.ENROLLMENT_INFO_FILE), 'a') as file:
            file.write(f"Color: {self.color}\nAudio File: {filename}\n\n")

        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame
        self.create_main_frame()  # Show the main frame again

    def stop_recording_authenticate(self):
        sd.stop()

        filename = os.path.join(self.DATA_FOLDER, f"temp_auth_recording.wav")
        wav.write(filename, 44100, self.audio_data)

        # Compare the recorded audio with saved recordings
        matched_user, matched_color = match_recordings(self, self.match_threshold)

        if matched_user:
            print(f"Authentication successful! Welcome, {matched_user}.")
            # Display the matched username frame
            display_matched_user_frame(self.current_frame, matched_user, matched_color)
        else:
            print("Authentication failed. Please try again.")

    def choose_color(self):
        _, self.color = colorchooser.askcolor(title="Choose a color")