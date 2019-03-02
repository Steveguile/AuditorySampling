
import os
import AttributeGenerator
import copy

file_path = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\\"

audio_dict = {}
dict_list = []

for directory in os.listdir(file_path):
    for file_name in os.listdir(file_path + directory):

        class_attribute = "No"

        if "&" in file_name:
            class_attribute = "Yes"

        print(file_path + directory + r"\\" + file_name)

        frequency_array, frequency_array_length = AttributeGenerator.amp_to_freq(file_path + directory + r"\\" + file_name)
        AttributeGenerator.add_attributes(frequency_array, frequency_array_length, audio_dict)
        audio_dict["TrafficIncident"] = class_attribute
        dict_list.append(copy.deepcopy(audio_dict)) # Need deepcopy or would overwrite previous key value

print(audio_dict)