import pyaudio
import wave
import struct
import audioop
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
import scipy.io.wavfile as wav

def scale_linear_bycolumn(rawpoints, high=255.0):
    maxs = np.amax(rawpoints)
    return high - ((high * (maxs - rawpoints)) / maxs)

def smooth(x,window_len=11,window='hanning'):
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

plt.ion()

CHUNK = 2205 # This should allow for 20HZ to be the baseline
length = 44100-CHUNK

RATE, data = wav.read("input.wav")
output = np.zeros((int(CHUNK/2),length),dtype="uint32")
histo = np.zeros((int(CHUNK/2),255),dtype="uint8")
data = data[0:length+CHUNK,0].astype("float32")

for j in range(0, length): # each position
	output[0:int(CHUNK/2),j] = np.abs(np.fft.fft(data[j:j+CHUNK]))[0:int(CHUNK/2)]/(CHUNK)
output = output/(np.amax(output)/255.0)
	
for j in range(int(CHUNK/2)):
	histo[j,:] = np.uint8(scale_linear_bycolumn(np.histogram(output[j,:],bins=255, range=(0,255), density=False)[0]))

cv2.imshow("test",histo[0:400,:])
print("done")
cv2.waitKey(0)