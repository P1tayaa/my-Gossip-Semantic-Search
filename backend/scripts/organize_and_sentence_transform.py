import pandas as pd
from sentence_transformers import SentenceTransformer
import os
from . import get_data

SENTENCE_TRANFORMER_MODEL = os.getenv("SENTENCE_TRANFORMER_MODEL", "all-MiniLM-L6-v2")


FILENAME = os.getenv("SENTENCE_TRANSFORMER_DATA_NAME", "articles_with_embeddings.csv")


def load_dataset(filename=get_data.DATADIR + get_data.FILENAME):
    try:
        df = pd.read_csv(filename)
        print(f"Loaded dataset with {len(df)} articles.")
        return df
    except FileNotFoundError:
        print("Dataset file not found. Run the article fetching script first.")
        return None


def embed_articles(dataframe, model_name=SENTENCE_TRANFORMER_MODEL):
    model = SentenceTransformer(model_name)

    texts = dataframe["title"] + " " + dataframe["summary"].fillna("")

    embeddings = model.encode(texts.tolist(), show_progress_bar=True)

    dataframe["embedding"] = embeddings.tolist()
    return dataframe


def save_with_embeddings(dataframe, filename=get_data.DATADIR + FILENAME):
    dataframe.to_csv(filename, index=False)
    print(f"Dataset with embeddings saved to {filename}")


def check_required_file(filename=get_data.DATADIR + FILENAME) -> bool:
    if not os.path.exists(filename):
        return True
    return False


def main_call():
    get_data.create_dataset()

    df = load_dataset()

    if df is not None:
        df_with_embeddings = embed_articles(df)

        save_with_embeddings(df_with_embeddings)


if __name__ == "__main__":
    main_call()
