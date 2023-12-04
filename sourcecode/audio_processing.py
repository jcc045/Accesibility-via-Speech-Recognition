from pydub import AudioSegment
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def trim_silence(audio_data, threshold_db):
    # Convert numpy array to PyDub AudioSegment
    audio_segment = AudioSegment(
        audio_data.tobytes(),
        frame_rate=44100,  # Adjust the frame rate according to your audio data
        sample_width=audio_data.dtype.itemsize,
        channels=len(audio_data.shape)
    )

    # Use PyDub's built-in silence trimming
    trimmed_audio_segment = audio_segment.strip_silence(
        silence_thresh=threshold_db,  # Adjust threshold based on your needs
        silence_len=500  # Adjust the minimum silence duration as needed
    )

    # Convert the trimmed AudioSegment back to numpy array
    trimmed_audio_data = np.array(trimmed_audio_segment.get_array_of_samples()).reshape(-1, audio_data.shape[1])

    return trimmed_audio_data


