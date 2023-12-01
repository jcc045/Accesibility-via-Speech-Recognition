import tkinter as tk

def enroll():
    # Add your code for the Enroll button action here
    print("Enroll button clicked")

def authenticate():
    # Add your code for the Authenticate button action here
    print("Authenticate button clicked")

# Create the main window
window = tk.Tk()
window.title("Biometric System")

# Create Enroll button
enroll_button = tk.Button(window, text="Enroll", command=enroll)
enroll_button.pack(pady=10)

# Create Authenticate button
authenticate_button = tk.Button(window, text="Authenticate", command=authenticate)
authenticate_button.pack(pady=10)

# Run the GUI
window.mainloop()
