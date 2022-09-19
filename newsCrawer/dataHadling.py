import pandas as pd
import glob

# 변수 관리
DELTEXT = ['\n','"','\'','\xa0','사진=']
DROPTEXT = '코멘트를 추가합니다'

def textHandling(data):
    fulltext = data.newsfulltext

    for idx,text in enumerate(fulltext):
        if text == DROPTEXT:
            data.drop(index=idx, inplace=True)
        for item in DELTEXT:
            text = text.replace(item,'')
        fulltext[idx] = text

def main():
    directory = glob.glob('./data/newsData_*.csv')
    total = pd.DataFrame()
    for file_ in directory:
        data = pd.read_csv(file_,encoding='utf8',index_col=0)
        textHandling(data)
        total = total.append(data, ignore_index=True)

    total.to_csv('data/handlingData.csv', encoding='utf-8')

if __name__=='__main__':
    main()
