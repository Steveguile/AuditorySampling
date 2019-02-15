
from pydub import AudioSegment
import os

audio_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Converted\\"
output_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\\"

# Folder Names (Can be changed for anything)
road_noise = r"\Road_Noise\\"
added_audio = r"\Added_Audio\\"

# PyDub does things in milliseconds
# ten_seconds = 10 * 1000
# first_10_seconds = audio[:10000]
# last_5_seconds = audio[-5000:]

# split audio in 5-second slices
# audio = audio_path + 'road_noise_2.wav'
# road_noise = AudioSegment.from_wav(audio)
# slices = road_noise[::5000]


def the_slicer(audio, filename):
    for i, chunk in enumerate(audio[::10000]):
        with open(filename + "-%s.wav" % i, "wb") as f:
            chunk.export(f, format="wav")


def main():

    # Road noise slicer
    for filename in os.listdir(audio_path + road_noise):
        audio = AudioSegment.from_wav(audio_path + road_noise + filename)
        the_slicer(audio, output_path + r"No_Traffic_Incident\\" + filename.split('.')[0])


main()

# Play code
# wav_obj = sa.WaveObject.from_wave_file(audio)
# play_obj = wav_obj.play()
# play_obj.wait_done()
