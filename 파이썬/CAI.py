import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
path = '/Users/jawwoo/Bigdata/PData/'
raw_CAI = pd.read_excel(path + 'CAI.xlsx', sheet_name = 'Data') # 통합대기지수 원본 데이터
cai = raw_CAI.copy()
cai = cai.rename(columns = {'통합대기지수' : 'CAI'})
a = cai['CAI'].isna().sum() # 결측치 0
# print(a)
cai = cai.assign(HOW_EXPR = np.where(cai['CAI'] <= 50 , 'GOOD',     # 통합대기지수 구간별 표현방법
                                         np.where(cai['CAI'] <= 100 , 'NORMAL',
                                                  np.where(cai['CAI'] <= 250 , 'BAD','EXT_BAD'))))
# print(cai['HOW_EXPR'])
