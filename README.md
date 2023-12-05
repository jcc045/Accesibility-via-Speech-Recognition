# Biometric System - Speaker Identification

## Overview
This biometric system implements speaker identification using voice recordings. Users can enroll by recording their voice, and the system authenticates individuals based on their unique voice characteristics. The program is developed in Python and utilizes the Tkinter library for the graphical user interface.

## Features
- **Enrollment:** Users can enroll by providing their name, selecting a color preference, and recording an enrollment phrase.
- **Authentication:** The system authenticates users by comparing recorded voice samples with enrolled voice samples.
- **User Interface:** A user-friendly Tkinter GUI facilitates easy interaction, making the system accessible to all users.

## Installation
1. Ensure Python is installed on your system.
2. Install required dependencies using: `pip install -r requirements.txt`

## How to Run
Execute the program by running `python main.py` in the terminal or command prompt.

## Usage
1. Click "Enroll" to register a new user.
2. Enter your name, choose a color, and record an enrollment phrase.
3. Click "Authenticate" to verify identity. Record the authentication phrase when prompted.
4. The system displays the username of the authenticated user in the color they chose.

## Dependencies
- Tkinter
- Sounddevice
- Numpy
- Scipy
- Torch
- Torchaudio
- Pydub

