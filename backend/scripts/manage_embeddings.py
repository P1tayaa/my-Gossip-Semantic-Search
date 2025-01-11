import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import json


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR + "/../" + os.getenv("DIR_DATA", "data/")

EMBEDDINGS_DIR = DATA_DIR + "embeddings/"
QUERY_MAP_FILE = DATA_DIR + "query_map.json"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")


def load_query_map():
    """
    Load the query-to-embedding file map.
    """
    if os.path.exists(QUERY_MAP_FILE):
        with open(QUERY_MAP_FILE, "r") as f:
            query_map = json.load(f)
        print("Loaded query map.")
    else:
        query_map = {}
        print("Query map not found. Starting fresh.")
    return query_map


def save_query_map(query_map):
    """
    Save the query-to-embedding file map.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(QUERY_MAP_FILE, "w") as f:
        json.dump(query_map, f, indent=4)
    print(f"Query map saved to {QUERY_MAP_FILE}")


def get_embeddings_file_path(query):
    """
    Generate a consistent file path for storing embeddings for a given query.
    """
    sanitized_query = "".join(
        c if c.isalnum() or c in (" ", "_") else "_" for c in query
    )
    return os.path.join(EMBEDDINGS_DIR, f"{sanitized_query}.csv")


def generate_embeddings(query, model_name=SENTENCE_TRANSFORMER_MODEL):
    """
    Generate embeddings for a given query.
    """
    print(f"Generating embeddings for query: {query}")
    model = SentenceTransformer(model_name)

    # Example text list for embedding generation; replace this with actual data retrieval
    text_list = [f"Example sentence for query: {query}"]

    embeddings = model.encode(text_list, show_progress_bar=True)

    # Create a DataFrame to store the embeddings
    df = pd.DataFrame(
        {
            "query": [query] * len(text_list),
            "text": text_list,
            "embedding": embeddings.tolist(),
        }
    )

    return df


def manage_embeddings(query):
    """
    Check for existing embeddings or create new ones if not found.
    """
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    # Load or create query map
    query_map = load_query_map()

    # Check if embeddings for the query already exist
    if query in query_map:
        file_path = query_map[query]
        if os.path.exists(file_path):
            print(f"Found existing embeddings for query: {query}")
            return pd.read_csv(file_path)
        else:
            print(f"Embedding file {file_path} not found. Generating new embeddings.")

    # Generate new embeddings
    df_embeddings = generate_embeddings(query)

    # Save new embeddings to file
    file_path = get_embeddings_file_path(query)
    df_embeddings.to_csv(file_path, index=False)
    print(f"Embeddings saved to {file_path}")

    # Update and save query map
    query_map[query] = file_path
    save_query_map(query_map)

    return df_embeddings


if __name__ == "__main__":
    # Example query to test the script
    example_query = "example search query"
    df = manage_embeddings(example_query)
    print(f"Generated or loaded embeddings for query: {example_query}")
    print(df.head())
