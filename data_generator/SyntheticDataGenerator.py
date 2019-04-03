
from pydub import AudioSegment
import os
from random import randint, uniform
import string
import random
import shutil
from math import floor, ceil

# File paths
audio_path_in = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], r"data\audio\Original_Files")
train_audio_path_out = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], r"data\audio\Train")
test_audio_path_out = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], r"data\audio\Test")

# Input Folder Names (Can be changed for anything)
road_noise = r"Road_Noise\\"
added_audio = r"Added_Audio\\"

# Output Folder Names (Can be changed for anything)
no_traffic_incident = r"No_Traffic_Incident\\"
traffic_incident = r"Traffic_Incident\\"

# PyDub does things in milliseconds
# ten_seconds = 10 * 1000
# first_10_seconds = audio[:10000]
# last_5_seconds = audio[-5000:]

# xxxxxxxxxxxxxxxxxxxxx Configure Parameters xxxxxxxxxxxxxxxxxxxxx
max_from_source = 500
audio_length = 3 * 1000 # 3 second audio
class_ratio = 1 # How many traffic accident clips vs non-traffic accident clips (1 = 1:1, 2 = 2:1, n = n:1)
min_crash_length = 2 * 1000 # 2 second crash length is minimum
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# Credit to StackOverflow user abhi krishnan for answer to question https://stackoverflow.com/questions/51434897/how-to-change-audio-playback-speed-using-pydub
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def the_slicer(path):
    for filename in os.listdir(os.path.join(audio_path_in, road_noise)):
        audio = AudioSegment.from_wav(os.path.join(audio_path_in, road_noise, filename))
        for i, chunk in enumerate(audio[::audio_length]):
            with open(os.path.join(path, no_traffic_incident , generate_reference(path) + ".wav"), "wb") as f:
                chunk.export(f, format="wav")

            if i == max_from_source - 1:  # Only really want x amount of instances from any single audio file
                break


def get_crash_audio(path):
    read_file = -1
    dir_size = len(os.listdir(os.path.join(audio_path_in, added_audio)))

    if path == test_audio_path_out:
        # 30% of road accident audio files to be used exclusively for holdout set
        read_file = randint(dir_size - floor((dir_size / 100) * 30), dir_size)
    elif path == train_audio_path_out:
        # 70 % left for training
        read_file = randint(0, ceil((dir_size / 100) * 70))

    crash_file = os.path.join(audio_path_in, added_audio, os.listdir(os.path.join(audio_path_in, added_audio))[read_file - 1])
    audio = AudioSegment.from_wav(crash_file) - randint(15, 25) # Always reduce as incidents are much louder than normal audio, 15-25db seems suitable

    # Do 1 of 3: 1 - Stretch audio, 3 - Reverse audio, else - Leave audio as is
    option = randint(1,4)
    if option == 1:
        audio = speed_change(audio, uniform(0.1, 1.1))
    elif option == 2:
        audio = audio.reverse()

    if len(audio) > audio_length:
        random_start_point = randint(0, len(audio) - audio_length) # Always allow for audio length parameter
        audio_segment = audio[random_start_point : random_start_point + randint(min_crash_length, audio_length)]
    else:
        audio_segment = audio

    return audio_segment


def get_road_audio(path):
    audio_file = randint(0, len(os.listdir(os.path.join(path, no_traffic_incident))))
    read_file = os.path.join(path, no_traffic_incident, os.listdir(os.path.join(path, no_traffic_incident))[audio_file - 1])
    audio = AudioSegment.from_wav(read_file)

    return audio


def overlay_audio(path):
    check_dir = os.listdir(os.path.join(path, no_traffic_incident))
    crash_audio_quantity = int(len(check_dir) / class_ratio) # How many traffic incidents to overlay

    for i in range(0, crash_audio_quantity):
        crash_audio = get_crash_audio(path)
        traffic_audio = get_road_audio(path)

        reference = generate_reference(path)
        overlaid_audio = traffic_audio.overlay(crash_audio)

        with open(os.path.join(path, traffic_incident, reference + ".wav"), "wb") as f:
            overlaid_audio.export(f, format="wav")


def generate_reference(path):
    reference_list = []

    # Current audio file reference names
    for filename in os.listdir(os.path.join(path, no_traffic_incident)):
        reference_list.append(filename.split('.')[0])
    for filename in os.listdir(os.path.join(path, traffic_incident)):
        reference_list.append(filename.split('.')[0])

    # Credit to StackOverflow user Ignacio Vazquez-Abrams for answer on https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while reference in reference_list:
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return reference


def refresh_dirs(path):
    # Refresh these directories
    shutil.rmtree(os.path.join(path, no_traffic_incident))
    os.mkdir(os.path.join(path, no_traffic_incident))
    shutil.rmtree(os.path.join(path, traffic_incident))
    os.mkdir(os.path.join(path, traffic_incident))


def main():

    if os.path.isdir(os.path.join(audio_path_in, road_noise)):
        refresh_dirs(train_audio_path_out)
        the_slicer(train_audio_path_out)
        overlay_audio(train_audio_path_out)

        refresh_dirs(test_audio_path_out)
        the_slicer(test_audio_path_out)
        overlay_audio(test_audio_path_out)
    else:
        print("This is not a valid input file")

main()
