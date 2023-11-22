import torch
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
from transformers import BartConfig
class model_file_load():
    '''
    데이터가 담긴 파일 경로를 parameter로 받아서 모델을 불러오고 모델의 predict도 함수로 설정함

    [parameter]
        file_path : 파일경로(str) - 모델(.pt) 
    '''
    def __init__(self,file_path,model_name,max_lengh=512):
        self.file_path=file_path # 파일 경로를 받아옴
        self.model_name = model_name # 모델의 pretrain 정보를 갖고옴 - tokenizer를 위해 필요
        if self.model_name=="Helsinki-NLP/opus-mt-ko-en":
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        elif self.model_name=='digit82/kobart-summarization':
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model=self.load_model()
        self.max_lengh=max_lengh
    def load_model(self):
        model = torch.load(self.file_path, map_location=torch.device('cpu'))  # GPU 사용하지 않도록 설정
        model.eval()
        return model
    
    def predict(self,text):
        if self.model_name=="Helsinki-NLP/opus-mt-ko-en":
            input_ids = self.tokenizer(text.replace('\n',''),return_tensors="pt")['input_ids']
            output = self.model.generate(input_ids,max_length=self.max_lengh)
            predcit_text=self.tokenizer.decode(output[0], skip_special_tokens=True)
        elif self.model_name=='digit82/kobart-summarization':
            input_ids = self.tokenizer(text.replace('\n',''),return_tensors="pt")['input_ids']
            output = self.model.generate(input_ids,max_length=68)
            predcit_text=self.tokenizer.decode(output[0], skip_special_tokens=True)
        return predcit_text
