
from pydub import AudioSegment
import os
from random import randint
import string
import random

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

def the_slicer():
    for filename in os.listdir(audio_path_in + road_noise):
        audio = AudioSegment.from_wav(audio_path_in + road_noise + filename)
        for i, chunk in enumerate(audio[::audio_length]):
            with open(audio_path_out + no_traffic_incident + generate_reference() + ".wav" , "wb") as f:
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
    return audio_segment


# TODO: Make it so original road audio is never used twice, can be solved by TODO under "Road noise with crash"
def get_road_audio():
    audio_file = randint(0, len(os.listdir(audio_path_out + no_traffic_incident)))
    read_file = audio_path_out + no_traffic_incident + os.listdir((audio_path_out + no_traffic_incident))[audio_file - 1]
    audio = AudioSegment.from_wav(read_file)

    return audio


def overlay_audio():
    # TODO: Convert this to instead of reading, create a copy + crash when writing initial snipped audio file for performance
    check_dir = os.listdir(audio_path_out + no_traffic_incident)
    crash_audio_quantity = int(len(check_dir) / class_ratio) # How many traffic incidents to overlay

    for i in range(0, crash_audio_quantity):
        crash_audio = get_crash_audio()
        traffic_audio = get_road_audio()

        reference = generate_reference()
        overlaid_audio = traffic_audio.overlay(crash_audio)

        with open(audio_path_out + traffic_incident + reference + ".wav", "wb") as f:
            overlaid_audio.export(f, format="wav")


def generate_reference():
    reference_list = []

    # Current audio file reference names
    for filename in os.listdir(audio_path_out + no_traffic_incident):
        reference_list.append(filename.split('.')[0])
    for filename in os.listdir(audio_path_out + traffic_incident):
        reference_list.append(filename.split('.')[0])

    # Credit to StackOverflow user Ignacio Vazquez-Abrams for answer on https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while reference in reference_list:
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return reference


def main():

    the_slicer()

    # Road noise with crash
    overlay_audio()

    generate_reference()


main()
