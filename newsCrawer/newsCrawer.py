from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver

def getNewsFullText(result):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('newsCrawer/chromedriver.exe',options=options)

    for i in range(800000,800010):
        wd.get(f'https://kr.investing.com/news/economy/article-{i}')
        time.sleep(0.5) #팝업 표시후 크롤링이 안되서 브라우저가 닫히는 것을 방지
        
        try:
            html = wd.page_source
            soup = BeautifulSoup(html,'html.parser')
            fullText = soup.select('#leftColumn > div > p')
            for j in fullText:
                print(j.text)
            

        except Exception as e:
            print(e)
            continue
    
        print('-'*50)

def main():
    result = []
    print('newsCrawer'+'>>'*10)
    getNewsFullText(result)


if __name__=='__main__':
    main()