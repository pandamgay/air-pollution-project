import pandas as pd
import  numpy as np
import seaborn as sns
import folium
import json


### 데이터 로드
path = '../통계량 데이터/'
m = 2
y = 2020
for i in range(1,21):
    data = pd.read_excel(path + f"{y}/{y}년 {m}월.xlsx")
    sigCd = pd.read_excel("./시군구단위 코드(법정동).xlsx")

    ### 결측치 확인
    # print(pd.isna(data).sum())

    ### 이상치 확인 - 이상치 없음
    # for i in ["SO2", "CO", "O3", "NO2", "PM10", "PM25"]:
    #     print(i, data[i].min())

    ### 결측치 처리
    dataCleaned = data.dropna(subset=['PM10', 'PM25'])
    # print(pd.isna(dataCleaned).sum())

    ### 지역별 평균값 계산
    regionAvg = dataCleaned.groupby("지역")[["PM10", "PM25"]].mean().reset_index()

    # 시군구코드 파생변수 생성
    regionAvg['시군구코드'] = None

    # 조건에 따라 매핑
    new_rows = []
    for idx, row in regionAvg.iterrows():
        region = row['지역']
        prefix = region[:2]
        suffix = region[3:]

        # 조건 1: 정확히 일치하는 경우
        match = sigCd[(sigCd['시도'] == prefix) & (sigCd['시군구'] == suffix)]
        if not match.empty:
            regionAvg.at[idx, '시군구코드'] = match.iloc[0]['시군구코드']
        else:
            # 조건 2: 시군구가 포함되는 경우
            partial_match = sigCd[(sigCd['시도'] == prefix) & (sigCd['시군구'].str.contains(suffix))]
            if not partial_match.empty:
                # 기존 행 삭제
                regionAvg.drop(idx, inplace=True)
                # 새로운 행 추가
                for _, match_row in partial_match.iterrows():
                    new_row = {
                        '지역': region,
                        'PM10': row['PM10'],
                        'PM25': row['PM25'],
                        '시군구코드': match_row['시군구코드']
                    }
                    new_rows.append(new_row)

    # 새로운 행 추가
    regionAvg = pd.concat([regionAvg, pd.DataFrame(new_rows)], ignore_index=True)

    print(regionAvg.to_string())

    # 지도 객체 생성 (대한민국 중심 좌표로)
    map = folium.Map(location=[36.5, 127.5], zoom_start=7)

    # geojson 파일 로드
    with open('./TL_SCCO_SIG.json', encoding='utf-8') as f:
        geo_str = json.load(f)

    # Choropleth 시각화
    folium.Choropleth(
        geo_data=geo_str,
        data=regionAvg,
        columns=["시군구코드", "PM10"],
        key_on="feature.properties.SIG_CD",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="지역별 PM10 평균 농도"
    ).add_to(map)

    map.save(f'region_pm10_avg_map-{str(y) + str(m).zfill(2)}.html')

    if m == 12:
        m = 1
        y += 1
    elif m == 3:
        m = 12
    else:
        m += 1
