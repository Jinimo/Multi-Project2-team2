### 비율 임의로 정하여 나누기 
# file_path: csv 파일 위치
# age_range: 0 --> 15세이상 65세미만 / 1 --> 15세 미만, 65세 이상 
# n: 원하는 배수 
# ** 참고) 아직 15세 미만, 65세 이상은 수정중 !!

import pandas as pd
import os

def cov_rate(file_path, age_range, n):  # ====> 결과: df_rate
  
  global df ,df_age, df_rate, df_new0, df_new1

  ## 파일 불러오기
  file_path = file_path
  while True:
    try:
        df  = pd.read_csv(file_path)
        break
    except ValueError:
        df  = pd.read_csv(file_path, encoding='cp949')
        break

  df.columns = ['uuid', 'cough_detected', 'SNR', 'gender', 'man',
        'respiratory_condition', 'fever_muscle_pain', 'COVID-19', 'healthy',
        'symptomatic', '15세미만', '15세이상65세미만', '65세이상']


  ## 나이대별로 나누기 
  # 15세이상 65세미만
  if age_range == 0: 
    df_age = df[df['15세이상65세미만'] == 1 ]
    range_n = df.groupby(['man', 'COVID-19'])['15세이상65세미만'].sum().min() # 음성의 최소 개수
  
  # 15세 미만, 65세 이상 
  elif age_range == 1: 
    df_age = df[(df['15세미만'] == 1) | (df['65세이상'] == 1) ]
    range_15 = df.groupby(['man', 'COVID-19'])['15세미만'].sum().min()
    range_65 = df.groupby(['man', 'COVID-19'])['65세이상'].sum().min()
    range_n = min(range_15, range_65) # 음성의 최소 개수

  df_age.reset_index(drop=True, inplace=True)

  ## 비율 맞춰서 나눈 후 병합  
  for i in range(2):
    for k in range(2):
      if k == 0: # 음성이면 
        df_gen_0 = df_age[(df_age['man'] == i) & (df_age['COVID-19'] == 1)].sample( n * range_n, replace=True)
      elif k == 1: # 양성이면 
        df_gen_1 = df_age[(df_age['man'] == i) & (df_age['COVID-19'] == k)][:range_n]
      
    globals()['df_new{}'.format(i)] = pd.concat([df_gen_0, df_gen_1])

  df_rate = pd.concat([df_new0, df_new1])
  df_rate.reset_index(drop=True, inplace=True)
  
  return df_rate