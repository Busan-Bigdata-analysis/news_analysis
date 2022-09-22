from flask import Flask,request,render_template,jsonify
from ainize import *
# 남이 만든 모듈을 내가 가져다 사용
# from model import predictMainStream

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/short', methods=['POST'])
def short():
    res = {
        'msg': decoding_summary_text(mySummary_text_ids(request.form['msg']))
    }
    return jsonify(res)

@app.route('/analisys')
def analisys():
    pass

if __name__=='__main__':
    app.run(debug=True)