import torch
import sounddevice as sd
import numpy as np

import modules


torch.hub.set_dir('tts_models')
sample_rate = 48000
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language='ru',
                                     speaker='v3_1_ru')  # Speaker model for Russian (e.g., 'aidar', 'baya', 'kseniya', 'xenia', 'random')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

modules.load_models += 1

# Function to generate and play speech
def speak(text):
    # Generate speech
    audio = model.apply_tts(text=text,
                            speaker='aidar',
                            sample_rate=sample_rate)

    # Convert to numpy array and normalize
    audio_np = audio.cpu().numpy()
    audio_np = audio_np / np.max(np.abs(audio_np))

    # Play the audio
    sd.play(audio_np, sample_rate)
    sd.wait()
