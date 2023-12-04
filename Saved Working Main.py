import os
import tkinter as tk
from tkinter import colorchooser
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import scipy.spatial.distance as distance
import torch
import torchvision.models as models
from PIL import Image
import torchaudio
import torchaudio.transforms as T
from torchvision.models import vgg19
from torchvision import transforms
import warnings
warnings.filterwarnings("ignore")

class BiometricSystem:
    DATA_FOLDER = "data"
    ENROLLMENT_INFO_FILE = "enrollment_info.txt"

    button_style = {'bg': '#3498db', 'fg': 'white', 'borderwidth': 2, 'relief': tk.GROOVE, 'font': ('Helvetica', 12)}

    def __init__(self, master):
        self.master = master
        self.master.title("Biometric System")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.current_frame = None
        self.name_value = ""
        self.color = ""
        self.audio_data = None

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
        _, self.color = colorchooser.askcolor(title="Choose a color")

    def record_audio(self):
        print(f"Recording...")
        self.audio_data = sd.rec(44100 * 5, samplerate=44100, channels=2, dtype=np.int16)        
        sd.wait()

        # Trim silence using a threshold (adjust threshold as needed)
        threshold = 0.01
        trimmed_audio_data = self.trim_silence(self.audio_data, threshold)

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

    def authenticate_action(self):
        if self.current_frame:
            self.current_frame.pack_forget()

        authentication_frame = tk.Frame(self.master)
        authentication_frame.pack()

        prompt_label = tk.Label(authentication_frame, text="Please say the authentication phrase: Two blue fish swam in the tank.")
        prompt_label.pack(pady=10)

        record_button = tk.Button(authentication_frame, text="Record Audio", command=self.record_audio_authenticate)
        record_button.pack(pady=10)

        stop_button = tk.Button(authentication_frame, text="Stop Recording", command=self.stop_recording_authenticate, **self.button_style)
        stop_button.pack(pady=10)

    def record_audio_authenticate(self):
        print(f"Recording...")
        self.audio_data = sd.rec(44100 * 5, samplerate=44100, channels=2, dtype=np.int16)
        sd.wait()

        # Trim silence using a threshold (adjust threshold as needed)
        threshold = 0.02
        trimmed_audio_data = self.trim_silence(self.audio_data, threshold)

        self.audio_data = trimmed_audio_data

    def stop_recording_authenticate(self):
        
        sd.stop()

        filename = os.path.join(self.DATA_FOLDER, f"temp_auth_recording.wav")
        wav.write(filename, 44100, self.audio_data)

        # Compare the recorded audio with saved recordings
        match_threshold = 0.7
        matched_user = self.match_recordings(self.audio_data, match_threshold)

        if matched_user:
            print(f"Authentication successful! Welcome, {matched_user}.")
        else:
            print("Authentication failed. Please try again.")

        # Hide the current frame after authentication
        if self.current_frame:
            self.current_frame.pack_forget()

        # Show the main frame again only if it's not already created
        if not hasattr(self, 'main_frame_created') or not self.main_frame_created:
            self.create_main_frame()
            self.main_frame_created = True

    def match_recordings(self, audio_data, threshold):
        max_similarity = -1
        matched_user = None
        audio_data_path = os.path.join(self.DATA_FOLDER, 'temp_auth_recording.wav')

        with open(os.path.join(self.DATA_FOLDER, self.ENROLLMENT_INFO_FILE), 'r') as file:
            lines = file.readlines()
            
            # Iterate over lines with step 3 to handle each user's information
            for i in range(0, len(lines), 3):

                color_line = lines[i].strip()
                audio_file_line = lines[i + 1].strip()
                

                if color_line.startswith("Color:") and audio_file_line.startswith("Audio File:"):
                    # Extract user information
                    user_color = color_line.split(":")[1].strip()
                    user_audio_file = audio_file_line.split(":")[1].strip()

                    # Compare the audio data with the new recording
                    similarity = self.compare_audio(user_audio_file, audio_data_path)

                    if similarity >= threshold and similarity > max_similarity:
                        max_similarity = similarity
                        matched_user = os.path.basename(user_audio_file).split("_")[0].strip()

        return matched_user
    
    def compare_audio(self, saved_audio_data, audio_data):
        saved_waveform, saved_sample_rate = torchaudio.load(saved_audio_data)
        mfcc_transform = T.MFCC()
        saved_mfcc = mfcc_transform(saved_waveform)

        audio_waveform, audio_sample_rate = torchaudio.load(audio_data)
        audio_mfcc = mfcc_transform(audio_waveform)

        to_pil = transforms.ToPILImage()

        saved_mfcc_image = to_pil(saved_mfcc.squeeze(0))
        audio_mfcc_image = to_pil(audio_mfcc.squeeze(0))

        saved_mfcc_image = saved_mfcc_image.convert("L")
        audio_mfcc_image = audio_mfcc_image.convert("L")

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        saved_mfcc_resized = transform(saved_mfcc_image)
        audio_mfcc_resized = transform(audio_mfcc_image)

        model = vgg19(pretrained=True)
        model.features[0] = torch.nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        model.eval()

        saved_features = model.features(saved_mfcc_resized.unsqueeze(0))
        audio_features = model.features(audio_mfcc_resized.unsqueeze(0))
        similarity = 1 - distance.cosine(saved_features.flatten().detach().numpy(), audio_features.flatten().detach().numpy())

        return similarity

    def trim_silence(self, audio_data, threshold):
        # Find indices where audio amplitude is above the threshold
        indices = np.where(np.max(np.abs(audio_data), axis=1) > threshold)[0]

        # Trim silence
        trimmed_audio_data = audio_data[indices[0]:indices[-1]+1, :]

        return trimmed_audio_data

if __name__ == "__main__":
    root = tk.Tk()
    app = BiometricSystem(root)
    root.mainloop()