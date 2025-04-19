import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams.update({'font.family' : 'AppleGothic'}) # 맥은 applegothic 써야함
plt.rcParams['axes.unicode_minus'] = False # -기호 사용시 깨짐 방지

path = '/Users/jawwoo/Bigdata/PData/'
raw_EMSNS = pd.read_excel(path + 'EMSNS.xlsx') # 배출통계량 원본 데이터
data = raw_EMSNS.copy()

# 연도와 오염물질 추출
years = data.columns[1:]
pollutants = data["Unnamed: 0"]

emissions_data = []
for index, pollutant in enumerate(pollutants):
    # 콤마를 제거하고 float으로 변환
    clean_data = data.iloc[index, 1:].replace(',', '', regex=True).astype(float)
    emissions_data.append(clean_data)

# 부드러운 색상의 커스텀 컬러맵 정의
custom_cmap = LinearSegmentedColormap.from_list(
    "enhanced_contrast",
    ['#ffb38a', '#8dd99b', '#7ab0d1']
)

# 컬러맵에서 색상 추출
colors = [custom_cmap(i/len(pollutants)) for i in range(len(pollutants))]

# 스택 막대 그래프 생성
plt.figure(figsize=(15, 10))
bottom = np.zeros(len(years))

for i, emissions in enumerate(emissions_data):
    plt.bar(years, emissions, bottom=bottom, label=pollutants[i], color=colors[i])
    bottom += emissions
plt.title("연도별 오염물질 누적 배출량 (2014-2022)", fontsize=16)
plt.xlabel("연도", fontsize=14)
plt.ylabel("배출량", fontsize=14)
plt.legend(fontsize=12)
plt.grid(axis='y')

# y축 값에 천 단위 구분 기호 추가
plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

plt.tight_layout()
plt.show()