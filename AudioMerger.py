import os
from pydub import AudioSegment
from random import *

audio_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Converted\\"
added_audio = r"\Added_Audio\\"
output_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\\"
traffic_incident = r"\Traffic_Incident\\"

audio_length = 100

def get_crash_audio():

    audio_file = randint(0, len(os.listdir(audio_path + added_audio)))
    read_file = audio_path + added_audio + os.listdir((audio_path + added_audio))[audio_file - 1]
    audio = AudioSegment.from_wav(read_file)

    if len(audio) > audio_length:
        random_start_point = randint(0, len(audio) - audio_length) # Always allow for audio length parameter
        audio_segment = audio[random_start_point : random_start_point + audio_length]
    else:
        audio_segment = audio

    # audio_segment.export(open(output_path + traffic_incident + "test.wav", "wb"), format="wav")

    return audio_segment

get_crash_audio()