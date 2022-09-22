from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

tokenizer = PreTrainedTokenizerFast.from_pretrained("./ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("./ainize/kobart-news")

def mySummary_text_ids(input_text): 
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    
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

    