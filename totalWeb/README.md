# Build Web

## Connection model
* use VSCode
* [Run server](/totalWeb/run.py)
* [BART model connection](/totalWeb/ainize/__init__.py)
* web build
    + Flask
* 동작
    + main page 실행
    + BART 모델 호출
    + ~~BERT 모델 호출~~
    + 모듈 호출해서 실행
* 역할
    + 모델에 메세지 전달
    + 출력 메세지를 프론트에 전달
<br/><br/>

## Web design
* use VSCode
* [main HTML file](/totalWeb/templates/index.html)
* 동작
    + 비동기 웹
    + 요약 및 엔터 버튼 클릭시 동작
* 역할
    + 데이터를 받아서 화면에 출력
<br/><br/>

## Output stocks
* use VSCode
* [work module](/totalWeb/src/data/__init__.py)
* 동작
    + 엔터 버튼 입력시 동작
    + 입력 : Bert 모델로 얻은 숫자(테마 번호) -> 출력 : 테마주 리스트
    + 해당하는 테마주의 10% 전달
* Data set
    * [Theme Stocks](https://drive.google.com/file/d/1_-39p5uxK4oO8h9XVXymLXAu8n4Ceue1/view?usp=sharing)
* 역할
    + 획득한 테마 값을 매개로 테마주를 전달해주는 역할
<br/><br/>

## More TODO
* 요약된 정보 카카오톡으로 전송

## Problem
* [Bert 모델](/buildModel/BertModel.ipynb)과 Windows 환경의 호환성 문제
    + colab 환경(Linux)에서는 문제없이 동작
    + anaconda 환경(가상 환경)에서는 호환성 이슈가 있음
* Theme Stocks의 주기적인 업데이트가 필요
