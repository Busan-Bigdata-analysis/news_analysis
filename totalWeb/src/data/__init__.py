import pandas as pd

# 환경변수
TAG_NAME = {0: 'IT', 1: '가구', 2: '가전', 3: '건설', 4: '금', 5: '기계', 6: '담배', 7: '도로', 8: '무역', 9: '미디어', 10: '반도체', 11: '방송', 12: '보석', 13: '보험', 14: '부동산', 15: '생명', 16: '서비스', 17: '석유', 18: '소프트웨어', 19: '에너지', 20: '영화', 21: '운송', 22: '은행', 23: '의료', 24: '자동차', 25: '제약', 26: '철강', 27: '철도', 28: '컴퓨터', 29: '통신', 30: '투자', 31: '항공', 32: '화학'}

# 카테고리를 통해서 테마 기업을 추출 하는 함수
def getName(category):
    '''
        category : 태그(테마) 번호를 입력 해주면 됨
        0: 'IT', 1: '가구', 2: '가전', 3: '건설', 4: '금', 5: '기계', 
        6: '담배', 7: '도로', 8: '무역', 9: '미디어', 10: '반도체', 
        11: '방송', 12: '보석', 13: '보험', 14: '부동산', 15: '생명', 
        16: '서비스', 17: '석유', 18: '소프트웨어', 19: '에너지', 20: '영화', 
        21: '운송', 22: '은행', 23: '의료', 24: '자동차', 25: '제약', 
        26: '철강', 27: '철도', 28: '컴퓨터', 29: '통신', 30: '투자', 
        31: '항공', 32: '화학'
    '''
    category = TAG_NAME[category]
    data = pd.read_csv('../totalWeb/src/data/stockName.csv',encoding='utf-8',index_col=0)
    data = data[data.tags==category].sample(frac=0.1)
    if len(data.Names):
        names = '| '
        for name in data.Names:
            names += name + ' | '
        return names
    else:
        return None


def main():
    result = getName(0)
    print(result)

if __name__=='__main__':
    main()