# 폴더 역할

## BART model
<!-- https://github.com/News-sentiment-analysis/news_analysis/blob/main/newsCrawer/newsCrawer.ipynb -->
* use colab
* [BART model](/buildModel/BartModel.ipynb)
* Data set
    + [total_data_set](https://drive.google.com/file/d/1iEM7ZGOZVRu5xVrCniZufAK7t5rOzxHu/view?usp=sharing)
    + 구성 
        - news | summary
* 역할
    + 문자열(기사)를 요약 하는 모델

## 역할 2
* use colab
* [BERT model](/buildModel/BertModel.ipynb)
* Data set
    + [total_data_set](https://drive.google.com/file/d/1iEM7ZGOZVRu5xVrCniZufAK7t5rOzxHu/view?usp=sharing)
    + 구성 
        - newsfulltext | theme
        - theme
            '''
               0: 'IT', 1: '가구', 2: '가전', 3: '건설', 4: '금', 5: '기계', 6: '담배', 7: '도로', 8: 무역', 9: '미디어', 10: '반도체', 11: '방송', 12: '보석', 13: '보험', 14: '부동산', 15: '생명', 16: '서비스', 17: '석유', 18: '소프트웨어', 19: '에너지', 20: '영화', 21: '운송', 22: '은행', 23: '의료', 24: '자동차', 25: '제약', 26: '철강', 27: '철도', 28: '컴퓨터', 29: '통신', 30: '투자', 31: '항공', 32: '화학'
            '''
* 역할
    + 기사의 카테고리를 분류하는 모델