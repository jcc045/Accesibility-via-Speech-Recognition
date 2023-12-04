import tkinter as tk
from tkinter import ttk

def display_matched_user_frame(master, matched_user, user_color):
        # Create a new frame for displaying the matched username
        matched_user_frame = tk.Frame(master)
        matched_user_frame.pack(fill=tk.BOTH, expand=True)

        # Display the matched username in their selected color
        matched_user_label = tk.Label(matched_user_frame, text=f"Hello {matched_user}!", font=('Helvetica', 20), fg=user_color)
        matched_user_label.pack(pady=50)

        # Wait for 10 seconds
        master.after(10000, lambda: temp_frame(matched_user_frame))

def temp_frame(frame_to_destroy):
        # Destroy the frame used for displaying the matched username
        frame_to_destroy.destroy()

