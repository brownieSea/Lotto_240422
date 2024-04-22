# ORM 기술. 파이썬에서 만든 객체를 DB에 매핑하는 기술.
# 즉, 파이썬에서 db에 데이터를 넣을 때 사용.

import pandas as pd
from sqlalchemy import create_engine
import pymysql

data = {'학번': range(2000, 2013), '성적': [70,60,100,90,50,75,85,99,78,63, 100, 90, 100]}
df = pd.DataFrame(data=data, columns=['학번','성적'])
print(df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")  # mysql+pymysql://관리자id:비빌번호@주소:port/스키마?캐릭터셋
engine.connect()  # 실제 db와 연결

df.to_sql(name="test_tbl", con=engine, if_exists='replace', index=False) # name = 테이블명, con=커넥션, if_exists = 테이블이 있으면 추가된 자료만 더 추가해라.
