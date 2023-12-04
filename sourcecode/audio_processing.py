from pydub import AudioSegment
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def trim_silence(audio_data, threshold_db):

    # Convert numpy array to PyDub AudioSegment
    # Adjust the frame rate according to your audio data
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=44100, sample_width=audio_data.dtype.itemsize, channels=len(audio_data.shape))

    # Use PyDub's built-in silence trimming adjust threshold based on your needs
    # Adjust the minimum silence duration as needed
    trimmed_audio_segment = audio_segment.strip_silence(silence_thresh=threshold_db, silence_len=500)

    # Convert the trimmed AudioSegment back to numpy array
    trimmed_audio_data = np.array(trimmed_audio_segment.get_array_of_samples()).reshape(-1, audio_data.shape[1])

    return trimmed_audio_data


