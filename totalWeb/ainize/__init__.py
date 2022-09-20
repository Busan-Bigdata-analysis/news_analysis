from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
#  Load Model and Tokenize
tokenizer = PreTrainedTokenizerFast.from_pretrained("./ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("./ainize/kobart-news")

def mySummary_text_ids(input_text): 
    # Encode Input Text
    # input_text = "지난해 인텔을 제치고 세계 반도체 시장 매출 1위로 올라선 삼성전자[005930]가 올해 2분기 점유율을 더 늘린 것으로 나타났다. 18일 시장조사기관 옴디아에 따르면 올해 2분기 전 세계 반도체 시장 규모는 1천581억1천300만달러(약 220조원) 수준으로 집계됐다. 삼성전자의 2분기 반도체 매출은 203억달러(약 28조5천억원)로, 견조한 서버 수요와 시스템반도체 사업 성장에 힘입어 분기 기준 역대 최대치였다. 삼성전자의 시장 점유율은 1분기 12.5%에서 0.3%포인트(p) 늘어난 12.8%를 기록했다. 반면 인텔은 경기침체에 따른 PC 수요 둔화와 공급망 차질 등의 영향으로 올해 2분기에 '어닝쇼크'를 기록했다. 인텔의 2분기 매출은 1분기보다 16.6% 감소한 148억6천500만달러(약 20조6천억원)였고, 4억5천400만달러(약 6천억원)의 적자까지 발생했다. 인텔의 시장 점유율은 올해 1분기 11.1%에서 2분기 9.4%로 하락했다. 이에 따라 1위 삼성전자와 2위 인텔 간 점유율 격차는 1분기 1.4%p에서 2분기 3.4%p로 벌어졌다. 삼성과 인텔은 반도체 매출 1위 자리를 놓고 서로 엎치락뒤치락하는 라이벌 관계다. '반도체 공룡' 인텔은 세계 반도체 시장에서 명실상부 1위 자리를 지켜오다가 2017년 처음으로 삼성전자에 추월당했다. 2018년에도 삼성이 1위였다. 이후 인텔은 2019년에 삼성전자를 다시 추월해 2020년까지 2년 연속 1위를 차지했고, 지난해에는 삼성전자가 메모리반도체 호황에 힘입어 재역전에 성공했다. 올해 들어 메모리 반도체 업황이 나빠졌긴 했지만, 업계에서는 삼성전자가 올해도 무난하게 세계 반도체 1위 자리를 지킬 것이라는 전망이 나온다. 한편 SK하이닉스는 올해 2분기 6.8%의 시장 점유율로 삼성전자, 인텔에 이어 세계 3위를 기록했다. SK하이닉스의 점유율은 1분기보다 0.6%p 높아졌다. 퀄컴은 5.9%의 점유율로 4위, 마이크론은 5.2%의 점유율로 5위였고 그다음은 브로드컴(4.2%), AMD(4.1%), 엔비디아(3.6%), 미디어텍(3.3%), 텍사스인스트루먼트(3.0%) 등의 순이었다. 세계 반도체 매출 10위권 기업 중 국내 기업인 삼성전자와 SK하이닉스, 대만 미디어텍을 제외한 나머지 7개는 모두 미국 기업이었다."
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    # Generate Summary Text Ids
    summary_text_ids = model.generate(
        input_ids=input_ids,
        bos_token_id=model.config.bos_token_id,
        eos_token_id=model.config.eos_token_id,
        length_penalty=2.0,
        max_length=142,
        min_length=56,
        num_beams=4,
    )
    return summary_text_ids

def decoding_summary_text(summary_text_ids):
    return tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)