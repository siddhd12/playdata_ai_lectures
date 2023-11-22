import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from load_dataset import CustomDataset
from load_model import CustomModel
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    MarianTokenizer,
    MarianMTModel,
    MarianConfig,
)

import pandas as pd

class trans_load_model():
    def __init__(self,train_file_path,valid_file_path):
        self.train_df=pd.read_csv(train_file_path, encoding='utf-8')
        self.valid_df=pd.read_csv(valid_file_path, encoding='utf-8')
        self.model_name= "Helsinki-NLP/opus-mt-ko-en"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.train_dataset,self.valid_dataset=self.dataset()
        self.mymodel=self.model_make()
    
    def dataset(self):
        input_train = self.train_df['원문']
        target_train = self.train_df['번역문']

        input_valid = self.valid_df['원문']
        target_valid = self.valid_df['번역문']
        train_dataset = CustomDataset(input_train, target_train, self.tokenizer)
        valid_dataset = CustomDataset(input_valid, target_valid, self.tokenizer)
        return train_dataset,valid_dataset

    def model_make(self,decoder_layer=6):
        mymodel=CustomModel(self.model_name,decoder_layers=decoder_layer).return_model()
        for param in mymodel.get_encoder().parameters():
            param.requires_grad = False
        # total_params = sum(p.numel() for p in mymodel.parameters()) 파라미터 계산용,

        return mymodel
