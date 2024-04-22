import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql

def get_lottoNumber(count):  # 함수가 호출될 때 회차 번호를 받는다
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"
    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")
    date = soup.find('p', class_ = 'desc').text
    lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")

    lottoNumber = soup.find('div', class_ = 'num win').find('p').text.strip().split('\n')  # 앞 뒤 공백 제거. 로또당첨번호 5개를 리스트로 반환
    bonusNum = int(soup.find('div', class_ = 'num bonus').find('p').text.strip())  # 보너스번호 -> 정수로 반환

    lottoNumberList = list(map(lambda num: int(num), lottoNumber))

    # 날짜, 로또번호, 보너스 번호를 딕셔너리 성태로 return
    lottoDic = {"lottoDate" : lottoDate, "lottoNumber" : lottoNumberList, "bonusNumber" : bonusNum}
    return lottoDic

def get_recent_lottoCount():  # 최신 로또 회차 크롤링 함수
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    recent_count = int(soup.find('strong', {'id':'lottoDrwNo'}).text.strip())
    return recent_count + 1

lottoDf_list = []

for count in range(1, get_recent_lottoCount()):
    lottoResult = get_lottoNumber(count)
    lottoDf_list.append({
        'count' : count, # 로또 추첨 회차
        'lottoDate' : lottoResult['lottoDate'], # 로또 추첨일
        'lotteNum1' : lottoResult['lottoNumber'][0], # 로또 당첨 번호 1번째
        'lotteNum2' : lottoResult['lottoNumber'][1],  # 로또 당첨 번호 1번째
        'lotteNum3' : lottoResult['lottoNumber'][2],  # 로또 당첨 번호 1번째
        'lotteNum4' : lottoResult['lottoNumber'][3],  # 로또 당첨 번호 1번째
        'lotteNum5' : lottoResult['lottoNumber'][4],  # 로또 당첨 번호 1번째
        'lotteNum6' : lottoResult['lottoNumber'][5],  # 로또 당첨 번호 1번째
        'bonusNum' : lottoResult['bonusNumber']  # 로또 보너스 번호
    })
    print(f"{count}회차 처리중...")

# 가져온 로또 당첨번호를 dataframe 형태로 변환
lottoDf = pd.DataFrame(data=lottoDf_list, columns=['count', 'lottoDate', 'lotteNum1', 'lotteNum2', 'lotteNum3',
                                                   'lotteNum4','lotteNum5','lotteNum6', 'bonusNum'])

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")  # mysql+pymysql://관리자id:비빌번호@주소:port/스키마?캐릭터셋
engine.connect()  # 실제 db와 연결
lottoDf.to_sql(name="lotto_tbl", con=engine, if_exists='replace', index=False) # name = 테이블명, con=커넥션, if_exists = 테이블이 있으면 추가된 자료만 더 추가해라.

