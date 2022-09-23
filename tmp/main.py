# -*- coding: utf-8 -*-
from predict import Predict
from bert import BERTClassifier
import os
from utils import init_logger
import argparse

'''

손 덜 댔음 주의. 09.21 22:10
이 부분에서 lucy_data는 희승씨가 줄 33개 category를 가지고 있는 데이터 셋의 이름을 정해서 그것으로 대체 할 것.

'''




def predict_func(pred_config):
  DATA_COL = 'contents'
  LABEL_COL = 'category'
  predict = Predict()
  print(pred_config.input_file)
  print(pred_config.model_dir)
  tok, model = predict.load_model_n_tokenizer(pred_config.model_dir)
  classfier = BERTClassifier(model)
  lucy_data = predict.preprocess_data(pred_config.input_file, DATA_COL)
  save_path = predict.category_encoding_n_save(lucy_data, './temp/', LABEL_COL)
  predict_set = predict.load_data(save_path, 1,2)
  result_set = predict.predict_n_save_result(model, predict_set, tok, lucy_data, DATA_COL, './output/')
  predict.get_accuracy(model, predict_set, tok)
  if os.path.isfile(save_path):
      os.remove(save_path)

def main():
  print("========================================Done")


'''
  parser.add_argument("--model_dir", default='./model/20210802/model.pt', type=str, help="Path to load model")
  parser.add_argument("--input_file", default='./data/predict_lucy.csv', type=str, help="Input file for prediction")

  경로 프론트가 적절하게 수정할 것.

'''


if __name__ == '__main__':
  init_logger()
  parser = argparse.ArgumentParser()
  parser.add_argument("--model_dir", default='./model/20210802/model.pt', type=str, help="Path to load model")
  parser.add_argument("--input_file", default='./data/predict_lucy.csv', type=str, help="Input file for prediction")
  pred_config = parser.parse_args()
  predict_func(pred_config)
  main()