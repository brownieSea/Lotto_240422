# 로또 당첨 번호별 당첨 빈도수

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter  # 내장모듈


dbconn = pymysql.connect(host='localhost', user='root', password='12345', db='lottodb')

sql = "SELECT * FROM lotto_tbl"

cur = dbconn.cursor()
cur.execute(sql)
dbResult = cur.fetchall()

lotto_df = pd.DataFrame(data=dbResult, columns=['회차', '추첨일', '번호1', '번호2', '번호3',
                                                   '번호4','번호5','번호6', '보너스번호'])

lotto_num_df = pd.DataFrame(lotto_df.iloc[0:, 2:])  # 모든행, 2열부터 마지막열까지 (당첨번호 + 보너스번호만 추출)

# 모든 로또 번호를 하나의 리스트에 반환하기
lotto_num_list = list(lotto_num_df['번호1']) \
                 + list(lotto_num_df['번호2']) \
                 + list(lotto_num_df['번호3']) \
                 + list(lotto_num_df['번호4']) \
                 + list(lotto_num_df['번호5']) \
                 + list(lotto_num_df['번호6']) \
                 + list(lotto_num_df['보너스번호'])
print(len(lotto_num_list))

# 각 수의 빈도수
# for i in range(1, 46):
#     count = 0
#     for num in lotto_num_list:
#         if num == i:
#             count = count + 1
#     print(f"{i}의 빈도수 : {count}")


# 빈도수 계산 모듈 collections 라이브러리의 Counter - 딕셔너리로 반환. value 기준 내림차순.
n_lotto_data = Counter(lotto_num_list)
# print(n_lotto_data)

data = pd.Series(n_lotto_data)
data = data.sort_index()
data.plot(figsize=(12, 8), kind='barh', grid=True, title='lotto KOR DATA')
plt.show()

cur.close()
dbconn.close()