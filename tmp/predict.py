import torch
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
from tqdm import tqdm, tqdm_notebook

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model


import pandas as pd
import os
import time

from bert import BERTDataset

class Predict():
    
  def __init__(self, device_type='cpu'):
    """
      Args:
          device_type : default는 "cpu", gpu로 돌리고자 할 때 "cuda:0"을 입력합니다.

    """
    self.device = torch.device(device_type) # cpu로 돌리도록 선언 기본값 / "cuda:0"
    self.max_len = 128 # seqeunce 최대 길이
  
  #model and tokenizer 로딩 
  def load_model_n_tokenizer(self, model_path):
    """
      tips: Pytorch Model과 Tokenizer를 반환합니다.
      Args:
          model_path : 모델이 저장된 path.
      Returns:
          tok : nlp.data.BERTSPTokenizer
          model : torch model
    """
    #BERT 모델, Vocabulary 불러오기 필수
    bertmodel, vocab = get_pytorch_kobert_model()
    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    print(model_path)

    #★★★현재경로가 model이 있는 폴더여야함★★★
    os.chdir('/content/drive/MyDrive/models/') # 실제 사용시 모델이 있는 폴더로 변경

    model1 = torch.load('33Cat_model.pt')  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
    model1.load_state_dict(torch.load('33Cat_model_state_dict.pt'))  # state_dict를 불러 온 후, 모델에 저장

    checkpoint = torch.load('33Cat_all.tar')   # dict 불러오기
    model1.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])

    

    return tok, model1


  '''
  이 부분 희승씨가 만들어주신 category dataset 불러오는 코드를 넣어주세요!

  주의, def calc_accuracy 부터 약간 바뀐 것 있음, def get_accuracy는 현국의 원본 코드에 없었음.

  '''
  # def load_data(self, save_path, data_colnum, label_colnum):
  #   """
  #     tips: 저장된 input dataset을 불러옵니다.
  #     Args:
  #         save_path : txt데이터의 path
  #         data_colnum : data의 컬럼번호
  #         label_colnum : label의 컬럼번호
  #     Returns:
  #         marking_set : dataframe
  #   """
  #   predict_set = nlp.data.TSVDataset(save_path, field_indices=[data_colnum,label_colnum], num_discard_samples=1)
  #   return predict_set
  
  #예측 
  def predict(self, predict_sentence):

    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
    
    model1.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(test_dataloader)):
        token_ids = token_ids.long().device(self.device)
        segment_ids = segment_ids.long().device(self.device)

        valid_length= valid_length
        label = label.long().device(self.device)

        out = model1(token_ids, valid_length, segment_ids)

# np.argmax(logits) 출력

        test_eval=[]
        for i in out:
            logits=i
            logits = logits.detach().gpu().numpy()
            test_eval.append(np.argmax(logits))
        print(test_eval[0])

  #얼마나 타겟의 값을 잘 맞추었는지 평가하는 함수, 현국이 작성한 코드 원본에는 self 없었음.
  def calc_accuracy(self, X,Y):
    max_vals, max_indices = torch.max(X, 1)
    train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
    return train_acc

  #정확도 평가하는 함수
  def get_accuracy(self, model, predict_set, tok):
    """
      tips: predict_set에 대한 정확도를 평가합니다.
      Args:
          predict_set : 예측할 데이터 셋
          tok : tokenizer
          model : Pytorch Model
    """
    predict_set = BERTDataset(predict_set, 0, 1, tok, self.max_len, True, False)
    predict_input = torch.utils.data.DataLoader(predict_set, batch_size=1, num_workers=9)
    
    model.eval() # 평가 모드로 변경
      
    test_acc = 0.0
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(predict_input)):
        token_ids = token_ids.long().to(self.device)
        segment_ids = segment_ids.long().to(self.device)
        valid_length= valid_length
        label = label.long().to(self.device)
        out = model(token_ids, valid_length, segment_ids)
        test_acc += self.calc_accuracy(out, label)
    print("test accuracy : {}".format(test_acc / (batch_id+1)))




  # #전처리 안된 데이터 전처리
  # def preprocess_data(self, data_path, data_colname):
  #   """
  #     tips: csv 데이터를 받아 지정된 column의 내용을 preprocess 합니다.
  #     Args:
  #         data_path : csv데이터의 path
  #         data_colname : 지정할 column명
  #     Returns:
  #         lucy_data : DataFrame
  #   """
  #   lucy_data = pd.read_csv(data_path)

  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\(.*\)|\s-\s.*"," " ,regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\[.*\]|\s-\s.*"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\<.*\>|\s-\s.*"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("무단전재 및 재배포 금지"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("무단 전재 및 재배포 금지"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("©"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("ⓒ"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("저작권자"," ",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace(".* 기자", " ", regex=True) #기자 이름에서 오는 유사도 차단
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("사진 = .*", " ", regex=True) #사진 첨부 문구 삭제
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("사진=.*", " ", regex=True) #사진 첨부 문구 삭제
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace('\"', "",regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)", " ", regex=True) #이메일 주소에서 오는 유사도 차단
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\n"," ")
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\r"," ")
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("\t"," ")
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace( "\’" , "", regex=True)
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]"," ")
  #   lucy_data[data_colname] = lucy_data[data_colname].str.replace("[ ]{2,}"," ",regex=True)
    
  #   return lucy_data

  #라벨을 정수로 인코딩
  # def category_encoding_n_save(self, lucy_data, save_directory, label_colname):
  #   """
  #     tips: 텍스트로 된 라벨을 model에 지정된 정수 label로 인코딩 및 model의 input data를 파일로 저장합니다.
  #     Args:
  #         lucy_data : dataframe 형식의 데이터
  #         save_directory : 저장할 디렉토리(파일명은 제외)
  #         label_colname : 라벨의 컬럼명
  #     Returns:
  #         save_path : string
  #   """
  #   lucy_data[label_colname+'_val'] = lucy_data[label_colname] # string 형 컬럼 생성

  #   label_dict = {'0': 'IT/과학',
  #     '1': '경제',
  #     '2': '문화',
  #     '3': '미용/건강',
  #     '4': '사회',
  #     '5': '생활',
  #     '6': '스포츠',
  #     '7': '연예',
  #     '8': '정치'}

  #   for key, value in label_dict.items():
  #     print(value)
  #     lucy_data[label_colname] = lucy_data[label_colname].str.replace(value, key)

  #   now = int(round(time.time() * 1000))
  #   filename = 'sample_' + str(now) + '.txt'
  #   save_path = os.path.join(save_directory, filename)
  #   lucy_data.to_csv(save_path , sep = '\t' , index = False)
  #   print("===============Data encoding success! please check this directory : ", save_path)
  #   return save_path

  #dataset 불러오기

  # def predict_n_save_result(self, model, predict_set, tok, marking_set, marking_set_data_colname, save_directory, encoding_type='euc-kr'):
  #   """
  #     tips: 저장된 input dataset을 불러옵니다.
  #     Args:
  #         predict_set : 예측할 데이터 셋
  #         tok : tokenizer
  #         marking_set : 기록할 데이터 셋 (dataframe)
  #         marking_set_data_colname : 기록할 데이터 셋의 data 컬럼 이름
  #         save_directory : 저장할 디렉토리
  #         encoding_type : csv의 default는 euc-kr / 영문은 utf-8-sig 
  #     Returns:
  #         predict_set : nlp.data.TSVDataset
  #   """
  #   predict_set = BERTDataset(predict_set, 0, 1, tok, self.max_len, True, False)
  #   predict_input = torch.utils.data.DataLoader(predict_set, batch_size=1, num_workers=9)
    
  #   #컬럼 초기화
  #   marking_set['predict'] = -1
  #   marking_set['predict_tag'] = 'a'

  #   for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(predict_input)):
  #     token_ids = token_ids.long().to(self.device)
  #     segment_ids = segment_ids.long().to(self.device)
  #     valid_length= valid_length
  #     out = model(token_ids, valid_length, segment_ids)
  #     out_val = torch.argmax(out).cpu().numpy() # tensor > numpy로 변환
  #     out_tag = ''
  #     # print(marking_set[marking_set_data_colname][batch_id][1:50],'...') # 50자까지만 미리 출력 (빼도됨)
      
  #     if(out_val == 0):
  #       # print('IT/과학')
  #       out_tag = 'IT/과학'
  #     elif(out_val == 1):
  #       # print('경제')
  #       out_tag = '경제'
  #     elif(out_val == 2):
  #       # print('문화')
  #       out_tag = '문화'
  #     elif(out_val == 3):
  #       # print('미용/건강')
  #       out_tag = '미용/건강'
  #     elif(out_val == 4):
  #       # print('사회')
  #       out_tag = '사회'
  #     elif(out_val == 5):
  #       # print('생활')
  #       out_tag = '생활'
  #     elif(out_val == 6):
  #       # print('스포츠')
  #       out_tag = '스포츠'
  #     elif(out_val == 7):
  #       # print('연예')
  #       out_tag = '연예'
  #     elif(out_val == 8):
  #       # print('정치')
  #       out_tag = '정치'

  #     marking_set['predict'][batch_id] = out_val
  #     marking_set['predict_tag'][batch_id] = out_tag

  #   now = int(round(time.time() * 1000))
  #   filename = 'news_predict_' + str(now) + '.csv'
  #   save_path = os.path.join(save_directory, filename)
  #   marking_set.to_csv(save_path, encoding=encoding_type) #한글이면 euc-kr, utf-8-sig 
  #   print("===============Thank you for waiting. Predicting your dataset Finally Finish! Please Check this directory : ", save_path)
    
    # return marking_set

