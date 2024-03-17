import json
from transformers import AutoTokenizer, AutoModel, Trainer, TrainingArguments
from datasets import IterableDataset

from huggingface_hub import login

login(token="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")

# Load your JSON dataset
with open("C:\\dev\\Abolify\\backend\\data\\ml_training_data.json", "r") as f:
    dataset = json.load(f)

def gen():
    for row in dataset:
        yield row

# Convert to Dataset object
formatted_dataset = IterableDataset.from_generator(gen)

# Load pre-trained Llama2 model and tokenizer
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name, token="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")

print("downloaded 1")
model = AutoModel.from_pretrained(model_name)
print("downloaded")

# Tokenize dataset
def tokenize_dataset(example):
    return tokenizer(example["question"], example["answer"], truncation=True)

print("after tokenize_dataset()")

tokenized_dataset = formatted_dataset.map(tokenize_dataset, batched=True)

print("tokenized_dataset")

# Define training arguments
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_dir="./logs",
)

print("training args")

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

print("TRAINING")

# Fine-tune the model
trainer.train()