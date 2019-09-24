# -*- coding: utf-8 -*
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import glob
import sys

count = 0
mode = 0
plt.close('all')
print("正常、異常、ちょっと異常データのどちらですか？")
print("正常：1  異常：2  ちょっと異常：3")
mode = input(">>>  ")
if int(mode) == 1:
 os.chdir("normal_fft")
 input_file_list = glob.glob('../normal_data/*.csv')
elif int(mode) == 2:
 os.chdir("abnormal_fft")
 input_file_list = glob.glob('../abnormal_data/*.csv')
elif int(mode) == 3:
 os.chdir("abnormal2_fft")
 input_file_list = glob.glob('../abnormal2_data/*.csv')
else:
 print("入力したモードがありません")
 sys.exit(1)
for filename in input_file_list:
 with open (filename, 'r') as input:
  (time, data) = np.loadtxt(filename,unpack=True, delimiter=",", skiprows = 1,usecols = (1,1))

  fs = 10000.0 # サンプリング周波数
  f,t,Sxx = signal.spectrogram(data, fs, nperseg=512)
  print(filename)
  plt.figure()
  plt.pcolormesh(t,f,Sxx,vmax=1e-6)
  plt.xlim([0,2.1])
  plt.xlabel(u"Time [sec]")
  plt.ylabel(u"Freq [Hz]")
  plt.colorbar()
  #plt.show()
  count = count + 1
  plt.savefig(str(count) + '.png')
  plt.close('all')
