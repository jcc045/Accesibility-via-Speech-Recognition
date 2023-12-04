import tkinter as tk
from tkinter import colorchooser
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

class BiometricSystem:
    button_style = {'bg': '#3498db', 'fg': 'white', 'borderwidth': 2, 'relief': tk.GROOVE, 'font': ('Helvetica', 12)}

    def __init__(self, master):
        self.master = master
        self.master.title("Biometric System")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.current_frame = None

        self.create_main_frame()

    def create_main_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        enroll_button = tk.Button(self.current_frame, text="Enroll", command=self.switch_to_name_frame, **self.button_style)
        enroll_button.pack(pady=20)

        authenticate_button = tk.Button(self.current_frame, text="Authenticate", command=self.authenticate_action, **self.button_style)
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

        next_button = tk.Button(self.current_frame, text="Next", command=self.switch_to_color_frame, **self.button_style)
        next_button.pack(pady=20)

    def switch_to_color_frame(self):
        self.name_value = self.name_entry.get()  # Store the name value
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        color_label = tk.Label(self.current_frame, text="Choose a Color:")
        color_label.pack(pady=5)

        color_button = tk.Button(self.current_frame, text="Choose Color", command=self.choose_color)
        color_button.pack(pady=5)

        next_button = tk.Button(self.current_frame, text="Next", command=self.switch_to_audio_frame, **self.button_style)
        next_button.pack(pady=20)

    def switch_to_audio_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        prompt_label = tk.Label(self.current_frame, text=f"Hello, {self.name_value}! Please say the following phrase: Two blue fish swam in the tank.")
        prompt_label.pack(pady=10)

        record_button = tk.Button(self.current_frame, text="Record Audio", command=self.record_audio)
        record_button.pack(pady=10)

        stop_button = tk.Button(self.current_frame, text="Stop Recording", command=self.stop_recording, **self.button_style)
        stop_button.pack(pady=10)

    def choose_color(self):
        self.color = colorchooser.askcolor(title="Choose a color")[1]
        #if self.color:
            #print(f"Chosen color: {self.color}")

    def record_audio(self):
        print(f"Recording...")
        self.audio_data = sd.rec(44100 * 5, samplerate=44100, channels=2, dtype=np.int16)

    def stop_recording(self):
        sd.stop()
        filename = f"{self.name_value}_enrollment_recording.wav"
        wav.write(filename, 44100, self.audio_data)
        print(f"Audio recorded and saved to {filename}")

        with open('enrollment_info.txt', 'a') as file:
            file.write(f"Name: {self.name_value}\nColor: {self.color}\nAudio File: {filename}\n\n")

        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame
        self.create_main_frame()  # Show the main frame again

    def authenticate_action(self):
        print("Authenticate button clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = BiometricSystem(root)
    root.mainloop()
