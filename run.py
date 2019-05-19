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

## plot enable
plt.ion()
##################

#wf = wave.open('input.wav', 'rb')

###################
#audio = pyaudio.PyAudio()
###
#FORMAT = wf.getsampwidth()#pyaudio.paInt24
#CHANNELS = wf.getnchannels() # 2
#RATE = wf.getframerate()#44100
CHUNK = 4000

output = np.zeros((111,1000,2), dtype="uint32")
RATE, data = wav.read("input.wav")
j=0
while True:
	j += CHUNK
	print j
	#wavfile.read(somefile)
	#data = wf.readframes(CHUNK)
	#print len(data)
	#data = np.array(struct.unpack("%dh" % (len(data) / 2), data))

	good = data[j:j+CHUNK, 0]
	bad = data[j:j+CHUNK, 1]
	
	
	fft_data_original = np.abs(np.fft.fft(good,222))[0:111]
	fft_data_processed = np.abs(np.fft.fft(bad,222))[0:111]
	
	gain =   fft_data_processed / fft_data_original
	gain *= 255
	gain[np.where(gain>999)]=999
	#gain = gain.astype("uint8")
	fft_data_original/=2560
	fft_data_original[np.where(fft_data_original>65500)]=65500
	print np.amax(gain),np.amax(fft_data_original),np.amax(fft_data_processed)/256/100
	#fft_data_original[np.where(fft_data_original>255)]=255
	for i in range(111):  # gain x frequency 
		output[i,gain[i],0]+=fft_data_original[i]
		output[i,gain[i],1]+=1
		
	
	final = output[:,:,0]/output[:,:,1]
	final = final.astype("uint8")
	cv2.imshow("test",final)
	cv2.waitKey(1)
	#plt.clf()
	#plt.semilogx(range(np.shape(g1)[0]), g1)
	#plt.semilogx(range(np.shape(g1)[0]), (g2))
	#plt.semilogx(range(np.shape(gain)[0]), (gain*500000))
	#plt.axis([101, np.shape(g1)[0], 0, 18000000])
	#plt.pause(0.1)
	