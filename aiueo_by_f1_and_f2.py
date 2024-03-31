import numpy as np
from wave_file import wave_write_16bit_mono

fs = 44100
duration = 1 # 母音一つあたりの音の継続期間（秒）
num_of_vowel = 5 # 音を出す母音の数
volume = 0.7 # 出力Volume

length_of_s = int(fs * duration) # 母音一つあたりのサンプル数
total_length_of_s = num_of_vowel*length_of_s

s = np.zeros(total_length_of_s)

f1 = [800, 300, 300, 500, 500]
f2 = [1200, 2300, 1200, 1900, 800]

# loop for a(0), i(1), u(2), e(3), o(4)
for i in range(5):
    for n in range(length_of_s):
        s[i*length_of_s + n] = 0.5 * np.sin(2 * np.pi * f1[i] * n / fs) + 0.5 * np.sin(2 * np.pi * f2[i] * n / fs)

s /= np.max(np.abs(s))
s *= volume

for n in range(int(fs * 0.01)):
    s[n] *= n / (fs * 0.01)
    s[total_length_of_s - n - 1] *= n / (fs * 0.01)

length_of_s_master = int(fs * (duration*num_of_vowel + 2)) # "+2"->最初と最後に1秒無音期間を入れるため
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1) # 無音期間が最初（と最後に）fsサンプル分だけ入る
for n in range(total_length_of_s):
    s_master[offset + n] += s[n]

wave_write_16bit_mono(fs, s_master.copy(), 'aiueo(output).wav')
