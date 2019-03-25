from scipy.stats import kurtosis, skew, mode
from scipy.io.wavfile import read
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from librosa import feature as lb
import copy
import os
import csv
import re
import random
import geopip

# np.set_printoptions(threshold=np.inf)

audio_sub_dir = r"data/audio"

file_path = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], audio_sub_dir)
output_file = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], r"data")

# Output Folder Names (Can be changed for anything)
no_traffic_incident = r"No_Traffic_Incident"
traffic_incident = r"Traffic_Incident"


#Credit to StackOverflow user Constntinius for his answer on https://stackoverflow.com/questions/13497891/python-getting-around-division-by-zero
def safe_ln(x, min_val=0.000000000000000001): # Replace any zeros with very small value to avoid / 0
    return 10 * np.log10(x.clip(min=min_val))


# Credit to StackOverflow user Anil_M for his answer on https://stackoverflow.com/questions/43284049/spectrogram-of-a-wave-file
def amp_to_freq(audio_input):
    # Read file and get sampling freq [ usually 44100 Hz ]  and sound object
    sampling_frequency, sound_file = read(audio_input)

    # Check if wave file is 16bit or 32 bit. 24bit is not supported
    sound_fileDataType = sound_file.dtype

    # We can convert our sound array to floating point values ranging from -1 to 1 as follows
    sound_file = sound_file / (2.**15)

    # Check sample points and sound channel for duel channel(5060, 2) or  (5060, ) for mono channel

    sound_fileShape = sound_file.shape
    sample_points = float(sound_file.shape[0])

    # Get duration of sound file
    signal_duration = sound_file.shape[0] / sampling_frequency

    # If two channels, then select only one channel
    sound_file_single_channel = sound_file[:, 0]

    # Plotting the tone

    # We can represent sound by plotting the pressure values against time axis.
    # Create an array of sample point in one dimension
    time_array = np.arange(0, sample_points, 1)

    #
    time_array = time_array / sampling_frequency

    # Scale to milliSeconds
    time_array = time_array * 1000

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Plot the tone
    # plt.plot(time_array, sound_file_single_channel, color='G')
    # plt.xlabel('Time (ms)')
    # plt.ylabel('Amplitude')
    # plt.show()
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Plot frequency content
    # We can get frequency from amplitude and time using FFT , Fast Fourier Transform algorithm

    # Get length of sound_file object array
    sound_file_length = len(sound_file)

    # Take the Fourier transformation on given sample point
    # fft_array = fft(sound_file)
    fft_array = fft(sound_file_single_channel)

    number_unique_points = np.ceil((sound_file_length + 1) / 2.0)
    fft_array = fft_array[0:int(number_unique_points)]

    # FFT contains both magnitude and phase and given in complex numbers in real + imaginary parts (a + ib) format.
    # By taking absolute value , we get only real part
    fft_array = abs(fft_array)

    # Scale the fft array by length of sample points so that magnitude does not depend on
    # the length of the signal or on its sampling frequency
    fft_array = fft_array / float(sound_file_length)

    # FFT has both positive and negative information. Square to get positive only
    fft_array = fft_array ** 2

    # Multiply by two (research why?)
    # Odd NFFT excludes Nyquist point
    if sound_file_length % 2 > 0:  # We've got odd number of points in fft
       fft_array[1:len(fft_array)] = fft_array[1:len(fft_array)] * 2

    else:  # We've got even number of points in fft
        fft_array[1:len(fft_array) - 1] = fft_array[1:len(fft_array) - 1] * 2

    frequency_array = np.arange(0, number_unique_points, 1.0) * (sampling_frequency / sound_file_length)

    true_freq_array = safe_ln(fft_array)

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Plot the frequency
    # plt.plot(frequency_array/1000, true_freq_array, color='B')
    # plt.xlabel('Frequency (Khz)')
    # plt.ylabel('Power (dB)')
    # plt.show()
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Get List of element in frequency array
    # print frequency_array.dtype.type
    frequency_array_length = len(frequency_array)
    # print("frequency_array_length =", frequency_array_length)
    # np.savetxt("freqData.txt", frequency_array, fmt='%6.2f')

    # Print fft_array information
    # print("fft_array Length =", len(fft_array))
    # np.savetxt("fftData.txt", fft_array)

    return true_freq_array, frequency_array_length, sampling_frequency


def add_mean_freq(frequency_array, frequency_array_length, audio_dict):
    mean_freq = sum(frequency_array) / frequency_array_length
    # print("Mean Frequency: ", mean_freq)
    audio_dict["MeanFreq"] = mean_freq


def add_median_freq(frequency_array, audio_dict):
    # Median sorts list
    median_freq = np.median(frequency_array)
    # print("Median Frequency: ", median_freq)
    audio_dict["MedFreq"] = median_freq


def add_mode_freq(frequency_array, audio_dict):
    # Round down otherwise there will rarely be a mode
    mode_freq = mode(frequency_array.astype(int))
    # print("Mode Frequency :", int(mode_freq[0]))
    audio_dict["ModeFreq"] = int(mode_freq[0])


def add_std_freq(frequency_array, audio_dict):
    std_freq = np.std(frequency_array)
    # print("Standard Deviation Frequency: ", std_freq)
    audio_dict["SDF"] = std_freq


def add_quartile_freq(frequency_array, frequency_array_length, audio_dict):
    q1 = int(frequency_array_length * 0.25)
    q3 = int(frequency_array_length * 0.75) + 1  # Int rounds down

    q1_freq = np.median(frequency_array[0:q1])
    audio_dict["Q1"] = q1_freq
    iqr_freq = np.median(frequency_array[q1 + 1: q3 - 1])
    audio_dict["IQR"] = iqr_freq
    q3_freq = np.median(frequency_array[q3:frequency_array_length])
    audio_dict["Q3"] = q3_freq
    # print("Q1 Frequency: ", q1_freq, "\nIQR Frequency: ", iqr_freq, "\nQ3 Frequency: ", q3_freq)


def add_skewness(frequency_array, audio_dict):
    sound_file_skewness = skew(frequency_array)
    # print("Skewness: ", sound_file_skewness)
    audio_dict["Skewness"] = sound_file_skewness


def add_kurtosis(frequency_array, audio_dict):
    sound_file_kurtosis = kurtosis(frequency_array, fisher=True, bias=True)
    # print("Kurtosis: ", sound_file_kurtosis)
    audio_dict["Kurtosis"] = sound_file_kurtosis


def add_spectral_flatness(frequency_array, audio_dict):
    flatness = lb.spectral_flatness(frequency_array, power=1)  # 1 is power spectrum
    for i, band_flatness in enumerate(flatness.tolist()[0]):#
        # print("SpFlt%s" % (i + 1), band_flatness)
        audio_dict["SpFlt%s" % (i + 1)] = band_flatness


def add_spectral_centroid(frequency_array, audio_dict, sample_rate):
    centroid = lb.spectral_centroid(frequency_array, sample_rate)
    for i, band_centroid in enumerate(centroid.tolist()[0]):
        # print("Spectral Centroid: ", centroid)
        audio_dict["SpCen%s" % (i + 1)] = band_centroid


# I think average rows as https://librosa.github.io/librosa/generated/librosa.feature.spectral_contrast.html states
# "each row of spectral contrast values corresponds to a given octave-based frequency"
def add_spectral_contrast(frequency_array, audio_dict):
    contrast = lb.spectral_contrast(frequency_array)
    for i, row in enumerate(contrast.tolist()):
        audio_dict["SpCon%s" % (i + 1)] = sum(row) / len(row)


def add_attributes(frequency_array, frequency_array_length, audio_dict, reference, sample_rate):

    audio_dict["reference"] = reference

    add_mean_freq(frequency_array, frequency_array_length, audio_dict)
    add_median_freq(frequency_array, audio_dict)
    add_mode_freq(frequency_array, audio_dict)
    add_std_freq(frequency_array, audio_dict)
    add_quartile_freq(frequency_array, frequency_array_length, audio_dict)
    add_skewness(frequency_array, audio_dict)
    add_kurtosis(frequency_array, audio_dict)
    add_spectral_flatness(frequency_array, audio_dict)
    add_spectral_centroid(frequency_array, audio_dict, sample_rate)
    add_spectral_contrast(frequency_array, audio_dict) # This may need changing

def modify_sp_attributes(dict_list, dict_keys):

    # TODO:  highest and lowest flatness and centroids as there's so many
    # Credit to StackOverflow user Sven Marnach for answer on https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
    SpFlt = [s for s in dict_keys if "SpFlt" in s]
    SpCen = [s for s in dict_keys if "SpCen" in s]

    max_val = 0
    min_val = 50000000 # Will never be larger than this
    output_list = []

    for audio_dict in dict_list:
        for flatness in SpFlt:
            if audio_dict[flatness] > max_val:
                max_val = audio_dict[flatness]
            elif audio_dict[flatness] < min_val:
                min_val = audio_dict[flatness]

            audio_dict["MaxSpFlt"] = max_val
            audio_dict["MinSpFlt"] = min_val

            del audio_dict[flatness] # Remove key

        max_val = 0
        min_val = 50000000

        for centroid in SpCen:
            if audio_dict[centroid] > max_val:
                max_val = audio_dict[centroid]
            elif audio_dict[centroid] < min_val:
                min_val = audio_dict[centroid]

            audio_dict["MaxSpCen"] = max_val
            audio_dict["MinSpCen"] = min_val

            del audio_dict[centroid] # Remove key

        max_val = 0
        min_val = 50000000

        # Sometimes get added SpFlt and SpCen for some reason, can't figure out why as all should have same bands so just remove
        extra_keys = [key for key in audio_dict if "SpFlt" in key or "SpCen" in key]
        for key in extra_keys:
            if bool(re.search(r'\d', key)):
                del audio_dict[key]

        # Put label on end of dict
        target_val = audio_dict["TrafficIncident"]
        audio_dict.pop("TrafficIncident")
        audio_dict["TrafficIncident"] = target_val

        output_list.append(copy.deepcopy(audio_dict))

    return output_list


# Get a coordinate somewhere in UK borders
def coord_data():
    # UK borders exist somewhere between -8.5 to 2.2 (latitude) and 49.5 to 60 (longitude)
    Lat = random.uniform(49.5, 60)
    Long = random.uniform(-8.5, 2.2)
    coord = geopip.search(lat=Lat, lng=Long)

    # Fancied doing some recursion, not optimal over while loop though
    if coord is None:
        return coord_data()
    elif coord["FIPS"] == 'UK':
        return Lat, Long
    else:
        return coord_data()


def main():

    audio_dict = {}
    dict_list = []

    for directory in os.listdir(file_path):
        for file_name in os.listdir(os.path.join(file_path, directory)):

            class_attribute = "No"

            if directory == "Traffic_Incident": # TODO This is bad, don't do this
                class_attribute = "Yes"

            frequency_array, frequency_array_length, sample_rate = amp_to_freq(os.path.join(file_path, directory) + r"\\" + file_name)
            add_attributes(frequency_array, frequency_array_length, audio_dict, file_name.split('.')[0], sample_rate)
            audio_dict["TrafficIncident"] = class_attribute
            dict_list.append(copy.deepcopy(audio_dict))  # Need deepcopy or would overwrite previous key value

            # NEED TO DEFAULT DICT KEY VALUE TO "?" after each loop for unknown values for shorter audio clips
            audio_dict = {x: "?" for x in audio_dict}


    dict_keys = dict_list[0].keys()
    output_list = modify_sp_attributes(dict_list, dict_keys)

    with open(os.path.join(output_file, "traffic_audio.csv"), "w", newline='') as f:
        dict_writer = csv.DictWriter(f, dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_list)


main()

