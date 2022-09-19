from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import re

# 변수관리
KOR_PATTERN = '[^ㄱ-핳 0-9,.]'
BLANK = '(\s+)'
NEWS_THEME = ['IT','가구','가전','건설','금','기계','서비스','통신','운송','담배','도로','무역','미디어','반도체','방송','보석','보험','부동산','생명','석유','소프트웨어','에너지','영화','은행','의료','자동차','제약','철도','철강','컴퓨터','투자','항공','화학']
SKIP_PATTERN = '(오디오래빗+)'

def getFulltext(text):
    text = re.sub(KOR_PATTERN,'',text)
    text = re.sub(BLANK,' ',text)
    return text

def getNews(theme):
    fulltextList = []

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('chromedriver.exe',options=options)

    idx = 1

    while True:
        wd.get(f'https://www.hankyung.com/tag/{theme}?page={idx}')

        html = wd.page_source
        soup = BeautifulSoup(html,'html.parser')
        news = soup.select('.news_list_wrap .news-tit')

        print(f'현제 테마 : {theme}, 현제 페이지 : {idx}')
        
        if news or idx<11:
            for item in news:
                link = item.find(href=True)['href']
                wd.get(link)

                html = wd.page_source
                soup = BeautifulSoup(html,'html.parser')
                if re.search(SKIP_PATTERN,soup.select_one('title').text):
                    continue

                if soup.select_one('.article-body'):
                    data = soup.select_one('.article-body').text

                    fulltextList.append(getFulltext(data))
                    time.sleep(0.5)
            idx += 1
        else:
            break  
    return fulltextList

def main():
    for item in NEWS_THEME:
        newslist = getNews(item)
    
        columns = ['newsfulltext']

        news = pd.DataFrame(newslist,columns=columns)
        news['theme'] = item
        news.to_csv(f'data/{item}.csv', index=True, encoding='utf-8')

if __name__=='__main__':
    main()
    