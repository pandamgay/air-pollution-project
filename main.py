import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from DSS_INF import dss_inf
from EMSNS import clean_data
from CAI import cai
# print(dss_inf)
# print(clean_data)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#
# # 2. 데이터 전처리
df_melted = dss_inf.melt(id_vars="구분", var_name="년도", value_name="인원수")
df_melted["년도"] = df_melted["년도"].str.replace("년", "").astype(int)

dust_dict = {
    2014: 13426.0, 2015: 15934.0, 2016: 17236.0, 2017: 16415.0,
    2018: 15723.0, 2019: 13518.0, 2020: 11945.0, 2021: 10975.0, 2022: 11042.0
}
df_dust = pd.DataFrame(list(dust_dict.items()), columns=["년도", "미세먼지"])

# 3. 데이터 병합
df_merged = pd.merge(df_melted, df_dust, on="년도")

# 4. 상관계수 계산
correlation_results = df_merged.groupby("구분", group_keys=False).apply(
    lambda x: x["인원수"].corr(x["미세먼지"])
).reset_index(name="상관계수")

# 5. 유의미한 상관관계 필터링
significant = correlation_results[correlation_results["상관계수"].abs() >= 0.7]
selected_departments = significant["구분"].tolist()

# 6. 그래프 스타일 설정
sns.set(style="whitegrid")
plt.rcParams["font.family"] = "AppleGothic"  # Mac 기준 폰트 설정 (Windows는 'Malgun Gothic')
plt.rcParams["axes.unicode_minus"] = False

# 7. 그래프 + 표를 함께 출력
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})

# 7-1. 선그래프
for dept in selected_departments:
    dept_data = df_merged[df_merged["구분"] == dept]
    ax1.plot(dept_data["년도"], dept_data["인원수"], label=dept, linewidth=2)

ax1.set_title("미세먼지와 유의미한 진료과목 인원수 변화", fontsize=16)
ax1.set_xlabel("년도", fontsize=12)
ax1.set_ylabel("인원수", fontsize=12)
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)

# 7-2. 상관계수 표
table_data = significant.sort_values("상관계수", ascending=False).round(3)
ax2.axis("off")
table = ax2.table(
    cellText=table_data.values,
    colLabels=table_data.columns,
    cellLoc="center",
    loc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)

# 8. 이미지 저장
plt.tight_layout()
plt.savefig("유의미한_진료과목_미세먼지_그래프_및_상관계수.png", dpi=300)
plt.show()

