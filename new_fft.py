# -*- coding: utf-8 -*
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import glob
import sys


N = 5000            # サンプル数
dt = 0.001          # サンプリング間隔
t = np.arange(0, N*dt, dt) # 時間軸
freq = np.linspace(0, 1.0/dt, N) # 周波数軸

count = 0
mode = 0
plt.close('all')
print("正常か異常データのどちらですか？")
print("正常：1  異常：2")
mode = input(">>>  ")
if int(mode) == 1:
 os.chdir("test_fft")
 input_file_list = glob.glob('../normal_data/*.csv')
elif int(mode) == 2:
 os.chdir("test_fft")
 input_file_list = glob.glob('../abnormal_data/*.csv')
else:
 print("入力したモードがありません")
 sys.exit(1)
for filename in input_file_list:
 with open (filename, 'r') as input:
  x = np.loadtxt(filename,unpack=True, delimiter=",", skiprows = 1,usecols = (1,1))
  # グラフ表示

  datanum = len(x)                          #data number
  print(datanum)
  sampintv = 0.01                           #sampling interval[sec]
  funfreq = 1/(datanum * sampintv)          #fundamantal frequency
 
  anafreq = funfreq * np.arange(0, datanum) #analysis frequency
  res = np.fft.fft(x)                       #FFT results
  spec = abs(res)                           #FFT spectra
 
  #Graph output
  plt.xlim(1, 128)                          #data plot(128data)
  #plt.plot(x)
  #plt.show()
 
  plt.plot(anafreq, spec)                   #spectra 
  #plt.show()
 
  count = count + 1
  plt.savefig(str(count) + '.png')
  plt.close('all')







