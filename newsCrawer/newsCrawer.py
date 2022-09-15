from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import re

# 변수 관리
START_PAGE = 633128
END_PAGE = 833128
BREAK_OPTION = '찾으시는 페이지가 여기에 없는 것 같습니다.'
EMAIL_PATTERN = '[a-z][a-z0-9_]{4,}@(\w+)[.](\w+)'
DATE_PATTERN = '(\d{4})년 (\d{1,2})월 (\d{1,2})일'

def getNewsFullText(result,st,ed):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('newsCrawer/chromedriver.exe',options=options)

    # 뉴스 번호 
    for i in range(st,ed):
        wd.get(f'https://kr.investing.com/news/economy/article-{i}')
        # time.sleep(0.5) #팝업 표시후 크롤링이 안되서 브라우저가 닫히는 것을 방지
        
        try:
            html = wd.page_source
            soup = BeautifulSoup(html,'html.parser')
            fullText = soup.select('#leftColumn > div > p')
            date = soup.select_one('#leftColumn > div > span')

            time.sleep(0.5)
            # 뉴스 일자를 획득
            news = ''

            # 정규식을 사용해서 기사 아래에 오는 기자, 다른 뉴스 링크 등 데이터에 포함 되지 않게 처리
            for j in fullText:
                if re.search(EMAIL_PATTERN,j.text) or j.text == BREAK_OPTION:
                    break
                news += j.text + ' '

            # 정상적으로 기사를 획득했을 때 추가            
            if news:
                date = (re.search(DATE_PATTERN,date.text))
                result.append([date.group(),news])

        except Exception as e:
            print(e)
            continue
    
def main():
    result = []
    for i in range(100):
        getNewsFullText(result,START_PAGE+i*1000,END_PAGE+i*1000)

        columns = ['date','newsfulltext']

        newsFulltext = pd.DataFrame(result,columns=columns)

        newsFulltext.to_csv('newsCrawer/data/newsData.csv', index=True, encoding='utf-8')
        print(len(result))


if __name__=='__main__':
    main()