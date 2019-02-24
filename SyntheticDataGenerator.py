
from pydub import AudioSegment
import os
from random import *
# import AttributeGenerator as ag

# File paths
audio_path_in = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Converted\\"
audio_path_out = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\\"

# Input Folder Names (Can be changed for anything)
road_noise = r"\Road_Noise\\"
added_audio = r"\Added_Audio\\"

# Output Folder Names (Can be changed for anything)
no_traffic_incident = r"\No_Traffic_Incident\\"
traffic_incident = r"\Traffic_Incident\\"

# PyDub does things in milliseconds
# ten_seconds = 10 * 1000
# first_10_seconds = audio[:10000]
# last_5_seconds = audio[-5000:]

# xxxxxxxxxxxxxxxxxxxxx Configure Parameters xxxxxxxxxxxxxxxxxxxxx
max_from_source = 50
audio_length = 100 # 100ms chunks
class_ratio = 10 # How many traffic accident clips vs non-traffic accident clips
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def the_slicer(audio, filename):
    for i, chunk in enumerate(audio[::audio_length]):
        with open(filename + "-%s.wav" % (i + 1) , "wb") as f:
            chunk.export(f, format="wav")

        if i == max_from_source - 1:  # Only really want x amount of instances from any single audio file
            break


def get_crash_audio():
    audio_file = randint(0, len(os.listdir(audio_path_in + added_audio)))
    read_file = audio_path_in + added_audio + os.listdir((audio_path_in + added_audio))[audio_file - 1]
    audio = AudioSegment.from_wav(read_file)

    if len(audio) > audio_length:
        random_start_point = randint(0, len(audio) - audio_length) # Always allow for audio length parameter
        audio_segment = audio[random_start_point : random_start_point + audio_length]
    else:
        audio_segment = audio

    # audio_segment.export(open(output_path + traffic_incident + "test.wav", "wb"), format="wav")
    return audio_segment, read_file


# TODO: Make it so original road audio is never used twice, can be solved by TODO under "Road noise with crash"
def get_road_audio():
    audio_file = randint(0, len(os.listdir(audio_path_out + no_traffic_incident)))
    read_file = audio_path_out + no_traffic_incident + os.listdir((audio_path_out + no_traffic_incident))[audio_file - 1]
    audio = AudioSegment.from_wav(read_file)

    return audio, read_file


def overlay_audio():
    # TODO: Convert this to instead of reading, create a copy + crash when writing initial snipped audio file for performance
    check_dir = os.listdir(audio_path_out + no_traffic_incident)
    crash_audio_quantity = int(len(check_dir) / class_ratio) # How many traffic incidents to overlay

    for i in range(0, crash_audio_quantity):
        crash_audio, crash_filepath = get_crash_audio()
        traffic_audio, traffic_filepath = get_road_audio()

        traffic_filename = traffic_filepath.rsplit(r"\\", 1)[1].split(".")[0]
        crash_filename = crash_filepath.rsplit(r"\\", 1)[1].split(".")[0]

        overlaid_audio = traffic_audio.overlay(crash_audio)

        with open(audio_path_out + traffic_incident + traffic_filename + "&" + crash_filename + ".wav", "wb") as f:
            overlaid_audio.export(f, format="wav")


def main():

    # Road noise without crash slicer
    for filename in os.listdir(audio_path_in + road_noise):
        audio = AudioSegment.from_wav(audio_path_in + road_noise + filename)
        the_slicer(audio, audio_path_out + no_traffic_incident + filename.split('.')[0]) # TODO: Uncomment

    # Road noise with crash
    overlay_audio()


main()
