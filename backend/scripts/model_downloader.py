import os
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer

SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
CROSS_ENCODER_MODEL = os.getenv(
    "CROSS_ENCODER_MODEL", "cross-encoder/stsb-distilroberta-base"
)


def download_sentence_transformer(model_name=SENTENCE_TRANSFORMER_MODEL):
    print(f"Downloading SentenceTransformer model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"Downloaded SentenceTransformer model: {model_name}")


def download_cross_encoder(model_name=CROSS_ENCODER_MODEL):
    print(f"Downloading Cross Encoder model: {model_name}")
    AutoModel.from_pretrained(model_name)
    AutoTokenizer.from_pretrained(model_name)
    print(f"Downloaded Cross Encoder model: {model_name}")
