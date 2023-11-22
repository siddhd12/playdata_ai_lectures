
import torch
from torch.utils.data import Dataset
from transformers import MarianTokenizer, MarianMTModel, MarianConfig, MarianModel
class CustomDataset(Dataset):
    def __init__(self, source_df, target_df, max_length=429):
        self.source_sentences = source_df.reset_index().drop('index', axis=1).values.tolist()
        self.target_sentences = target_df.reset_index().drop('index', axis=1).values.tolist()
        model_name = "Helsinki-NLP/opus-mt-ko-en"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.max_length = max_length

    def __len__(self):
        return len(self.source_sentences)

    def __getitem__(self, idx):
        source_text = self.source_sentences[idx][0]
        target_text = self.target_sentences[idx][0]

        # 토큰화 및 패딩
        source_tokens = self.tokenizer(source_text, add_special_tokens=True, max_length=self.max_length, padding="max_length", truncation=True)
        target_tokens = self.tokenizer(target_text, add_special_tokens=True, max_length=self.max_length, padding="max_length", truncation=True)

        # 아래 부분을 수정하여 input_ids를 반환하도록 재정의
        return {'input_ids': torch.tensor(source_tokens['input_ids'], dtype=torch.long),
                'attention_mask': torch.tensor(source_tokens['attention_mask'], dtype=torch.long),
                'decoder_input_ids': torch.tensor(target_tokens['input_ids'], dtype=torch.long)}