import wave
import sys
import math
import numpy as np
import random
import cv2
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

output = np.zeros((800), dtype="float32")
RATE, data = wav.read("input2.wav")

threshold = 22100
final = np.int32(data[:]*.72)
k = np.where(final>threshold)
tmp = final-threshold
original = (tmp*14700)**0.5 + final
final[k]=original[k]
k = np.where(final<-threshold)
tmp = np.abs(final)-threshold
original = (tmp*14700)**0.5 + np.abs(final)
final[k]= -original[k]
final = np.nan_to_num(final) 
print(np.amax(final),np.amin(final))
final[np.where(final>32767)]=32767
final[np.where(final<-32767)]=-32767
final = np.int16(final)
wav.write("output2.wav", RATE, final)
