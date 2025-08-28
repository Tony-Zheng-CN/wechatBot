import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"   # 继续用镜像
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment"
)
print(classifier("今天天气好差"))