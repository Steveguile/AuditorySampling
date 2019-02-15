from pydub import AudioSegment
import os

directory_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\\"
video_path = r"Audio_Files_Original\\"
audio_path = r"Audio_Files_Converted\\"

# 2 Directories for Added_Audio and Road_Noise, this is here to batch convert them to wav
for directory_name in os.listdir(directory_path + video_path):
    for filename in os.listdir(directory_path + video_path + directory_name):
        audio = AudioSegment.from_file(directory_path + video_path + directory_name + r'\\' + filename)
        filename = filename.split('.')[0]
        audio.export(directory_path + audio_path + directory_name + r'\\' + filename + '.wav', format="wav")

