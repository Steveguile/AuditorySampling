from scipy.stats import kurtosis, kurtosistest
from scipy.io.wavfile import read
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt


# np.set_printoptions(threshold=np.inf)

test_file_1 = r"E:\Steve_Files\Work\University\Year 4\Project\My Project\Audio_Files\Audio_Files_Generated\No_Traffic_Incident\road_noise_1-8.wav"


sample_frequency, test_1 = read(test_file_1)

#Read file and get sampling freq [ usually 44100 Hz ]  and sound object
samplingFreq, mySound = read(test_file_1)

#Check if wave file is 16bit or 32 bit. 24bit is not supported
mySoundDataType = mySound.dtype

#We can convert our sound array to floating point values ranging from -1 to 1 as follows

mySound = mySound / (2.**15)

#Check sample points and sound channel for duel channel(5060, 2) or  (5060, ) for mono channel

mySoundShape = mySound.shape
samplePoints = float(mySound.shape[0])

#Get duration of sound file
signalDuration =  mySound.shape[0] / samplingFreq

#If two channels, then select only one channel
mySoundOneChannel = mySound[:,0]

#Plotting the tone

# We can represent sound by plotting the pressure values against time axis.
#Create an array of sample point in one dimension
timeArray = np.arange(0, samplePoints, 1)

#
timeArray = timeArray / samplingFreq

#Scale to milliSeconds
timeArray = timeArray * 1000

#Plot the tone
plt.plot(timeArray, mySoundOneChannel, color='G')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

#Plot frequency content
#We can get frquency from amplitude and time using FFT , Fast Fourier Transform algorithm

#Get length of mySound object array
mySoundLength = len(mySound)

#Take the Fourier transformation on given sample point
#fftArray = fft(mySound)
fftArray = fft(mySoundOneChannel)

numUniquePoints = np.ceil((mySoundLength + 1) / 2.0)
fftArray = fftArray[0:int(numUniquePoints)]

#FFT contains both magnitude and phase and given in complex numbers in real + imaginary parts (a + ib) format.
#By taking absolute value , we get only real part

fftArray = abs(fftArray)

#Scale the fft array by length of sample points so that magnitude does not depend on
#the length of the signal or on its sampling frequency

fftArray = fftArray / float(mySoundLength)

#FFT has both positive and negative information. Square to get positive only
fftArray = fftArray **2

#Multiply by two (research why?)
#Odd NFFT excludes Nyquist point
if mySoundLength % 2 > 0: #we've got odd number of points in fft
    fftArray[1:len(fftArray)] = fftArray[1:len(fftArray)] * 2

else: #We've got even number of points in fft
    fftArray[1:len(fftArray) -1] = fftArray[1:len(fftArray) -1] * 2

freqArray = np.arange(0, numUniquePoints, 1.0) * (samplingFreq / mySoundLength);

#Plot the frequency
plt.plot(freqArray/1000, 10 * np.log10 (fftArray), color='B')
plt.xlabel('Frequency (Khz)')
plt.ylabel('Power (dB)')
plt.show()

#Get List of element in frequency array
#print freqArray.dtype.type
freqArrayLength = len(freqArray)
print("freqArrayLength =", freqArrayLength)
np.savetxt("freqData.txt", freqArray, fmt='%6.2f')

#Print FFtarray information
print("fftArray Length =", len(fftArray))
np.savetxt("fftData.txt", fftArray)

#Print Kurtosis
mySoundKurtosis = kurtosis(freqArray, fisher=True, bias=True)
print(mySoundKurtosis)
