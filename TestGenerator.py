from pydub import AudioSegment

openfile = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Converted\Road_Noise\road_noise_1.wav"

audio = AudioSegment.from_wav(openfile)

print(len(audio))
new_audio = audio[200:len(audio) - 200]

with open(openfile, "wb") as f:
    new_audio.export(f, format="wav")