import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1116"

html = requests.get(url).text

#print(html)


# bs4 lxml 파서 설치 안하고 html 로 파싱할때
# soup = BeautifulSoup(html, "html.parser")
# date = soup.find('p', {'class':'desc'}).text
# print(date)
soup = BeautifulSoup(html, "lxml")
date = soup.find('p', class_ = 'desc').text
lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")
print(lottoDate)

#lottoNumber = soup.find('div', class_ = 'num win').text  
#lottoNumber = soup.find('div', class_ = 'num win').find('p').text  # 숫자만 크롤링  
#lottoNumber = soup.find('div', class_ = 'num win').find('p').text.split('\n') # 줄바꿈 제거
lottoNumber = soup.find('div', class_ = 'num win').find('p').text.strip().split('\n')  # 앞 뒤 공백 제거. 로또당첨번호 5개를 리스트로 반환
lottoBonus = int(soup.find('div', class_ = 'num bonus').find('p').text.strip())  # 보너스번호 -> 정수로 반환
print(lottoNumber, lottoBonus)

# lottoNumberList = []
# for num in lottoNumber:
#     num = int(num)
#     lottoNumberList.append(num)

# 위의 for문을 lambda 식으로.
lottoNumberList = list(map(lambda num: int(num), lottoNumber))
print(lottoNumberList, lottoBonus)




