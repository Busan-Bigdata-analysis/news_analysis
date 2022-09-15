from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import re

# 변수 관리
START_PAGE = 800000
END_PAGE = 800010
BREAK_OPTION = '찾으시는 페이지가 여기에 없는 것 같습니다.'
EMAIL_PATTERN = '[a-z][a-z0-9_]{4,}@(\w+)[.](\w+)'

def getNewsFullText(result):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('newsCrawer/chromedriver.exe',options=options)

    # 뉴스 번호 
    for i in range(START_PAGE,END_PAGE):
        wd.get(f'https://kr.investing.com/news/economy/article-{i}')
        # time.sleep(0.5) #팝업 표시후 크롤링이 안되서 브라우저가 닫히는 것을 방지
        
        try:
            html = wd.page_source
            soup = BeautifulSoup(html,'html.parser')
            fullText = soup.select('#leftColumn > div > p')

            patt = re.compile(EMAIL_PATTERN)
            # 기사가 삭제되어 페이지가 존재하지 않을때 나오는 메세지

            news = ''

            # 정규식을 사용해서 기사 아래에 오는 기자, 다른 뉴스 링크 등 데이터에 포함 되지 않게 처리
            for j in fullText:
                if re.search(pattern,j.text) or j.text == BREAK_OPTION:
                    break
                news += j.text + ' '

            # 정상적으로 기사를 획득했을 때 추가            
            if news:
                result.append(news)

        except Exception as e:
            print(e)
            continue
    
def main():
    result = []
    getNewsFullText(result)

    newsFulltext = pd.DataFrame(result,columns=['newsfulltext'])

    newsFulltext.to_csv('newsCrawer/data/newsData.csv', index=True, encoding='utf-8')
    print(len(result))


if __name__=='__main__':
    main()