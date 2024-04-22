# 로또 당성 번호 월별 분석

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter  # 내장모듈
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

dbconn = pymysql.connect(host='localhost', user='root', password='12345', db='lottodb')

sql = "SELECT * FROM lotto_tbl"

cur = dbconn.cursor()
cur.execute(sql)
dbResult = cur.fetchall()

lotto_df = pd.DataFrame(data=dbResult, columns=['회차', '추첨일', '번호1', '번호2', '번호3', '번호4','번호5','번호6', '보너스번호'])

lotto_df['추첨일'] = pd.to_datetime(lotto_df['추첨일'])  # 판다스에서 사용하는 날짜 형식으로 반환

#추첨일에서 월(month)만 추출하여 새로운 필드로 데이터 프레임에 추가
lotto_df['추첨월'] = lotto_df['추첨일'].dt.month


# lotto_month_01 = lotto_df[lotto_df['추첨월'] == 1]  # 1월에 추첨됐던 당첨 번호들.
#
# print(lotto_month_01)
#
# month01_list = list(lotto_month_01['번호1']) \
#                 + list(lotto_month_01['번호2']) \
#                 + list(lotto_month_01['번호3']) \
#                 + list(lotto_month_01['번호4']) \
#                 + list(lotto_month_01['번호5']) \
#                 + list(lotto_month_01['번호6']) \
#                 + list(lotto_month_01['보너스번호'])
#
# print(Counter(month01_list))
# n_lotto_data = Counter(month01_list)
# data = pd.Series(n_lotto_data)
# data = data.sort_index()
# data.plot(figsize=(12, 8), kind='barh', grid=True, title='1월 로또 번호 빈도수')
# plt.show()

for month in range(1,13): # 1월~12월까지 반복
    lotto_month_df = lotto_df[lotto_df['추첨월'] == month]
    month_lottoList = list(lotto_month_df['번호1']) \
                      + list(lotto_month_df['번호2']) \
                      + list(lotto_month_df['번호3']) \
                      + list(lotto_month_df['번호4']) \
                      + list(lotto_month_df['번호5']) \
                      + list(lotto_month_df['번호6']) \
                      + list(lotto_month_df['보너스번호'])

    month_freq = Counter(month_lottoList)  #  월별 출현 숫자의 빈도수
    data = pd.Series(month_freq)
    sorted_data = data.sort_values(ascending=False)  # 빈도수의 내림차순으로 정렬
    top10_data = sorted_data.head(10) # 빈수도가 높은 순으로 10개만 추출
    plt.subplot(4,3, month)
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.5)
    top10_data.plot(figsize=(10,20), kind='barh', grid=True, title="월별 최다 출현 로또 번호 top 10")
    plt.title(f"{month}월 최다 출현 번호")
    plt.xlabel("빈도수")
    plt.ylabel("로또번호")

plt.show()
cur.close()
dbconn.close()