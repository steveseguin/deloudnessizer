import wave
import sys
import math
import numpy as np
import random
import cv2
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

output = np.zeros((800), dtype="float32")
RATE, data = wav.read("input.wav")

data = np.float32(data)
good = data[:,0]

bad = data[:,1]*.72
dee = np.where(good==0)
good = np.delete(good,dee)
bad = np.delete(bad,dee)
gain = bad / good
gain = np.nan_to_num(gain)
gain = np.abs(gain)
good = np.int32(np.abs(good/50))
#20000
#0.3 drop for every 10000 over 20000
for i in range(40,800):
	j = np.where(good==(i))
	output[i]=np.mean(gain[j])
output = np.nan_to_num(output)
#plt.plot(final)	
plt.plot(output)

threshold = 22100
final = np.int32(data[:,1]*.72)
k = np.where(final>threshold)
tmp = final-threshold
original = (tmp*14700)**0.5 + final
final[k]=original[k]
k = np.where(final<-threshold)
tmp = np.abs(final)-threshold
original = (tmp*15000)**0.5 + np.abs(final)
final[k]= -original[k]
final = np.nan_to_num(final) 
print(np.amax(final),np.amin(final))
final[np.where(final>32767)]=32767
final[np.where(final<-32767)]=-32767
final = np.int16(final)
wav.write("output.wav", RATE, final)

plt.plot(output)
plt.show()