import os
import platform
from pydub import AudioSegment


if platform.system() == "Linux":
    dir_name = ''
else:
    dir_name = os.path.dirname(__file__).rsplit("/", 1)[0]

cut_dir = os.path.join('data', 'audio', 'Original_Files', 'Road_Noise')

max_length = 30 * 60 * 1000 # 30 minutes of audio


for file in os.listdir(os.path.join(dir_name, cut_dir)):
    audio = AudioSegment.from_wav(os.path.join(dir_name, cut_dir, file))

    for i, chunk in enumerate(audio[::max_length]):

        with open(os.path.join(os.path.join(dir_name, cut_dir, file)), "wb") as f:
            chunk.export(f, format="wav")

        # Only get first 30 minutes of audio clip
        if i == 0:
            break
