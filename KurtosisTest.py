from scipy.stats import kurtosis, skew, mode
from scipy.io.wavfile import read
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from librosa import feature as lb
import copy

# np.set_printoptions(threshold=np.inf)

test_file_1 = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\No_Traffic_Incident\road_noise_1-587.wav"
test_file_2 = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\No_Traffic_Incident\road_noise_1-655.wav"


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

    # Plot the tone
    plt.plot(time_array, sound_file_single_channel, color='G')
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.show()

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

    true_freq_array = 10 * np.log10(fft_array)

    # Plot the frequency
    plt.plot(frequency_array/1000, true_freq_array, color='B')
    plt.xlabel('Frequency (Khz)')
    plt.ylabel('Power (dB)')
    plt.show()

    # Get List of element in frequency array
    # print frequency_array.dtype.type
    frequency_array_length = len(frequency_array)
    # print("frequency_array_length =", frequency_array_length)
    # np.savetxt("freqData.txt", frequency_array, fmt='%6.2f')

    # Print fft_array information
    # print("fft_array Length =", len(fft_array))
    # np.savetxt("fftData.txt", fft_array)

    return true_freq_array, frequency_array_length



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


def add_spectral_centroid(frequency_array, audio_dict):
    centroid = lb.spectral_centroid(frequency_array)
    for i, band_centroid in enumerate(centroid.tolist()[0]):
        # print("Spectral Centroid: ", centroid)
        audio_dict["SpCen%s" % (i + 1)] = band_centroid


# I think average rows as https://librosa.github.io/librosa/generated/librosa.feature.spectral_contrast.html states
# "each row of spectral contrast values corresponds to a given octave-based frequency"
def add_spectral_contrast(frequency_array, audio_dict):
    contrast = lb.spectral_contrast(frequency_array)

    for i, row in enumerate(contrast.tolist()):
        audio_dict["SpCon%s" % (i + 1)] = sum(row) / len(row)


def add_attributes(frequency_array, frequency_array_length, audio_dict):

    add_mean_freq(frequency_array, frequency_array_length, audio_dict)
    add_median_freq(frequency_array, audio_dict)
    add_mode_freq(frequency_array, audio_dict)
    add_std_freq(frequency_array, audio_dict)
    add_quartile_freq(frequency_array, frequency_array_length, audio_dict)
    add_skewness(frequency_array, audio_dict)
    add_kurtosis(frequency_array, audio_dict)
    add_spectral_flatness(frequency_array, audio_dict)
    add_spectral_centroid(frequency_array, audio_dict)
    add_spectral_contrast(frequency_array, audio_dict) # This may need changing

def main():

    audio_dict = {}
    dict_list = []
    frequency_array, frequency_array_length = amp_to_freq(test_file_1)
    add_attributes(frequency_array, frequency_array_length, audio_dict)
    dict_list.append(copy.deepcopy(audio_dict)) # Need deepcopy or would overwrite previous key value
    frequency_array, frequency_array_length = amp_to_freq(test_file_2)
    add_attributes(frequency_array, frequency_array_length, audio_dict)
    dict_list.append(copy.deepcopy(audio_dict))

    # Print rows for easy checking
    for audio_dict in dict_list:
        print(audio_dict)


    #NEED TO DEFAULT DICT KEY VALUE TO "?" after each loop for unknown values for shorter audio clips
    audio_dict = {x: "?" for x in audio_dict}
    print(audio_dict)

main()

