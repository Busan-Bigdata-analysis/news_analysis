from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import re

# 변수 관리
START_PAGE = 1
END_PAGE = 35
MOD_PATTERN = '[ㄱ-핳]{2}'

def getNewsFullText(result,st,ed):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('newsCrawer/chromedriver.exe',options=options)

    # 뉴스 번호 
    for i in range(st,ed+1):
        wd.get(f'https://finance.naver.com/item/sise_day.naver?code=005930&page={i}')
        # time.sleep(0.5) #팝업 표시후 크롤링이 안되서 브라우저가 닫히는 것을 방지
        
        try:
            html = wd.page_source
            soup = BeautifulSoup(html,'html.parser')
            # 변동한 날자
            # 주가의 상승 또는 하락
            # 주가의 상승폭 [2~6, 10~14] 번째 인덱스만 필요
            var_range = soup.select('tr')

            time.sleep(0.5)

            # 0 -> 2 , 7 -> 10
            for idx in range(15):
                if 1 < idx < 7 or 9 < idx < 15:
                    td = var_range[idx].select('td')
                    date = td[0].text
                    price = td[1].text
                    jud = re.search(MOD_PATTERN,str(td[2]))
                    ch_mod = jud.group() if jud else 'None' # 굳이 이렇게 쓸 필요가 있나 의문?
                    ch_range = int(td[2].text.strip().replace(',',''))
                    result.append([date,price,ch_mod,ch_range])
                    # 로그 확인용
                    # print([date,ch_mod,ch_range])

        except Exception as e:
            print(e)
            continue
    
def main():
    result = []
    getNewsFullText(result,START_PAGE,END_PAGE)

    columns = ['date','stock Price','change mod','change range']

    newsFulltext = pd.DataFrame(result,columns=columns)

    newsFulltext.to_csv('stockCrawer/data/stockPrice.csv', index=True, encoding='utf-8')
    print(len(result))


if __name__=='__main__':
    main()