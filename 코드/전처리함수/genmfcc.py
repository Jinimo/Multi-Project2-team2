#!/usr/bin/env python
# coding: utf-8

# In[1]:


import librosa
import numpy as np
import pandas as pd
import noisereduce as nr


# In[2]:


def gen_mfcc(sig):
    
    # 상수 정의
    sample_rate=16000
    length = len(sig)/sample_rate   # 음악의 길이는 음파 길이(len(sig)) / sr
    n_fft=int(sample_rate*0.025)
    hop_length=int(sample_rate*0.01)
    r=length/9  # 분모를 조절하면 몇초동안 재생되는지 조절 가능

    # 진폭 정규화
    sig=(sig + sig.mean()) * 1/max(np.abs(sig))   

    # stft 분석을 하는 코드
    stft = librosa.stft(sig, n_fft=n_fft, hop_length=hop_length) 

    # 음원 데이터의 길이 정규화
    p_stft=librosa.phase_vocoder(stft, rate=r, hop_length=hop_length)

    mel_spec=librosa.feature.melspectrogram(S=p_stft, sr=sample_rate, n_mels=128, hop_length=hop_length)

    log_M=librosa.amplitude_to_db(mel_spec)

    # mfcc를 이용한 feature값 계산. n_mfcc는 추출하고자 하는 mfcc의 갯수
    mfcc = librosa.feature.mfcc(S=log_M, n_mfcc=30, sr=sample_rate)

    return mfcc


# In[ ]:




