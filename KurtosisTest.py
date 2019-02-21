from scipy.stats import kurtosis, skew
from scipy.io.wavfile import read
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt


# np.set_printoptions(threshold=np.inf)

test_file_1 = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\No_Traffic_Incident\road_noise_1-587.wav"
test_file_2 = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\No_Traffic_Incident\road_noise_1-655.wav"


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
    # We can get frquency from amplitude and time using FFT , Fast Fourier Transform algorithm

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
    fft_array = fft_array **2

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
    print("frequency_array_length =", frequency_array_length)
    np.savetxt("freqData.txt", frequency_array, fmt='%6.2f')

    # Print fft_array information
    print("fft_array Length =", len(fft_array))
    np.savetxt("fftData.txt", fft_array)

    add_mean_freq(true_freq_array, frequency_array_length)
    add_std_freq(true_freq_array)
    add_median_freq(true_freq_array)
    add_quartile_freq(true_freq_array, frequency_array_length)
    add_skewness(true_freq_array)
    add_kurtosis(true_freq_array)


def add_mean_freq(frequency_array, frequency_array_length):
    mean_freq = sum(frequency_array) / frequency_array_length
    print(mean_freq)


def add_std_freq(frequency_array):
    std_freq = np.std(frequency_array)
    print(std_freq)


def add_median_freq(frequency_array):
    # Median sorts list
    median_freq = np.median(frequency_array)
    print(median_freq)


def add_quartile_freq(frequency_array, frequency_array_length):
    q1 = int(frequency_array_length * 0.25)
    q3 = int(frequency_array_length * 0.75) + 1  # Int rounds down

    q1_freq = np.median(frequency_array[0:q1])
    q2_freq = np.median(frequency_array[q3:frequency_array_length])
    iqr_freq = np.median(frequency_array[q1 + 1: q3 - 1])

    print(q1_freq, " ", iqr_freq, " ", q2_freq)


def add_skewness(frequency_array):
    sound_file_skewness = skew(frequency_array)
    print(sound_file_skewness)


def add_kurtosis(frequency_array):
    sound_file_kurtosis = kurtosis(frequency_array, fisher=True, bias=True)
    print(sound_file_kurtosis)


def main():

    amp_to_freq(test_file_1)
    amp_to_freq(test_file_2)


main()

