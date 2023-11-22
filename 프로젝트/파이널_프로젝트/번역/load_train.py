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
import torch
class CustomTrain():
    def __init__(self,model,model_path,epoch,train_dataset,valid_dataset):
        self.model=model
        self.epoch=epoch
        self.train_dataset = train_dataset
        self.valid_dataset = valid_dataset
        self.model_name='Helsinki-NLP/opus-mt-ko-en'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.best_accuracy = 0.0  # 초기 최고 정확도를 0.0으로 설정
        self.training_args = Seq2SeqTrainingArguments(
            output_dir=model_path,                  # The output directory
            overwrite_output_dir=True,              # overwrite the content of the output directory
            num_train_epochs=1,                     # number of training epochs
            per_device_train_batch_size=10,         # batch size for training
            per_device_eval_batch_size=10,          # batch size for evaluation
            eval_steps=len(self.valid_dataset),                          # Number of update steps between two evaluations.
            save_steps=len(self.valid_dataset),                         # after # steps model is saved
            logging_steps=len(self.valid_dataset),
            warmup_steps=300,                       # number of warmup steps for learning rate scheduler
            prediction_loss_only=True,
            evaluation_strategy="steps",
            save_total_limit=3
            )
        
    def epoch_train(self,model):
        trainer = Seq2SeqTrainer(
                model=model,
                args=self.training_args,
                train_dataset=self.train_dataset,
                eval_dataset=self.valid_dataset,
        )
        for epoc in range(self.epoch):  # epoc만큼 돌거임 
            trainer.train()
            
        
        

            # 정확한 토큰의 개수를 계산
            # 정확도 계산 
            # 값 나오면 저장 
            result = []

# if current_accuracy > best_accuracy:
#       best_accuracy = current_accuracy
#       trainer.save_model("/content/drive/MyDrive/hong/models/base_model_10000.pt")  # 모델 
# print(f'model1 정확도: {count/total}')