import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.suwon.ac.kr/index.html?menuno=727"
html_doc = requests.get(url).text
soup = BeautifulSoup(html_doc, 'html.parser')

schedule = soup.find('div', class_ = 'contents_table')
schedule = schedule.tbody.find_all('tr')

start_date = []; end_date = []; content = []
for i in schedule:
    for j in i:
        if 'subject' in j.get('class', []):
            content.append(j.get_text())
        else:
            try:
                start_date_str, end_date_str = j.get_text().split('~')
                start = start_date_str.split('(')[0].strip()
                end = end_date_str.split('(')[0].strip()
            except:
                start = j.get_text().split('(')[0]
                end = j.get_text().split('(')[0]
            start_date.append(start); end_date.append(end)

start_date = pd.to_datetime(start_date, format = '%Y-%m-%d')
end_date = pd.to_datetime(end_date, format = '%Y-%m-%d')

학사일정 = pd.DataFrame({'content' : content, 'start_date' : start_date, 'end_date' : end_date})
학사일정