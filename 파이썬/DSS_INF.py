import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'font.family' : 'AppleGothic'}) # 맥은 applegothic 써야함
plt.rcParams['axes.unicode_minus'] = False # -기호 사용시 깨짐 방지
path = '/Users/jawwoo/Bigdata/PData/' # 경로
raw_DSS_INF = pd.read_excel(path + 'DSS_INF.xlsx') # 질병 원본 데이터
dss_inf = raw_DSS_INF.copy()
