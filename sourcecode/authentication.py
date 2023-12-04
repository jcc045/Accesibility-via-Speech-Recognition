import os
import scipy.spatial.distance as distance
import torch
import torchaudio
import torchaudio.transforms as T
from torchvision.models import vgg19
from torchvision import transforms
import warnings

warnings.filterwarnings("ignore")

def match_recordings(self, threshold):
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
                similarity = compare_audio(user_audio_file, audio_data_path)
                user = os.path.basename(user_audio_file).split("_")[0].strip()
                print(user)
                print("\n")
                print(similarity)
                print("\n\n")

                if similarity >= threshold and similarity > max_similarity:
                    max_similarity = similarity
                    matched_user = os.path.basename(user_audio_file).split("_")[0].strip()
                    matched_color = user_color

    return matched_user, matched_color

def compare_audio(saved_audio_data, audio_data):
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

    transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(),])

    saved_mfcc_resized = transform(saved_mfcc_image)
    audio_mfcc_resized = transform(audio_mfcc_image)

    model = vgg19(pretrained=True)
    model.features[0] = torch.nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    model.eval()

    saved_features = model.features(saved_mfcc_resized.unsqueeze(0))
    audio_features = model.features(audio_mfcc_resized.unsqueeze(0))
    similarity = 1 - distance.cosine(saved_features.flatten().detach().numpy(),
                                         audio_features.flatten().detach().numpy())

    return similarity