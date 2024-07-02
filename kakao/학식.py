import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

detail = [762, 1793]
식단 = {0: [], 1: [], 2: [], 3: [], 4: []}
for i in range(2):
    url = "https://www.suwon.ac.kr/index.html?menuno=" + str(detail[i])
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    lunch = soup.find('table', class_ = 'txtc bdr w768')
    lunch = lunch.tbody.tr

    cells = lunch.find_all('td')

    for idx, cell in enumerate(cells[2:]):
        식단[idx].append(cell.text)

df = pd.DataFrame(식단)
df.rename(columns={0: '월', 1: '화', 2: '수', 3: '목', 4: '금'}, inplace = True)
df.insert(0, '식당', ['종합강의동', '아마랜스홀'])

today = ''
tommorow = ''
def get_today():
    global today, tommorow
    now = datetime.datetime.now()
    t = ['월', '화', '수', '목', '금', '토', '일']
    r = datetime.datetime.today().weekday() % 7
    day = str(now.year) + '년 ' + str(now.month) + '월 ' + str(now.day) + '일 ' + t[r] + '요일'
    today = t[r]
    tommorow = t[r+1]
    return {'오늘' : today, '내일' : tommorow}

오늘 = get_today()['오늘']
내일 = get_today()['내일']

df['오늘'] = df[오늘]
df['내일'] = df[내일]
df.to_csv('학식_ver2.csv', index = False)

