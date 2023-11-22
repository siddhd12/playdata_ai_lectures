import torch.nn as nn
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
class CustomModel(nn.Module):
    def __init__(self, model_name, decoder_layers=None, lm_head=None, dropout=None):
        super(CustomModel, self).__init__()

        # 디코더 레이어 개수 정의
        config = MarianConfig.from_pretrained(model_name)
        config.decoder_layers = decoder_layers

        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, config=config)

        if lm_head:
            self.model.lm_head = lm_head

        if dropout:
            self.model.dropout = dropout

        # encoder freezing
        for param in self.model.get_encoder().parameters():
            param.requires_grad = False

    def return_model(self):
        return self.model