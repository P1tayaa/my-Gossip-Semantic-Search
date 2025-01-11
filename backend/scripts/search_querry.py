import os
import json
import pandas as pd
from sentence_transformers import CrossEncoder
from typing import List, TypedDict

# Constants for model and data paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(SCRIPT_DIR, "../", os.getenv("DIR_DATA", "data/"))
QUERY_MAP_FILE = os.path.join(DATADIR, "query_map.json")
OLD_QUERIES_DIR = os.path.join(DATADIR, "old_queries/")
DATASET_FILE = os.getenv(
    "SENTENCE_TRANSFORMER_DATA_NAME", "articles_with_embeddings.csv"
)
CROSS_ENCODER_MODEL = os.getenv(
    "CROSS_ENCODER_MODEL", "cross-encoder/stsb-distilroberta-base"
)


class MatchDict(TypedDict):
    title: str
    link: str
    published: str
    summary: str
    source: str
    site: str
    similarity: float


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the dataset containing article information.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Dataset file not found: {file_path}")
        return pd.DataFrame()


def load_query_map() -> dict:
    """
    Load the query map from the JSON file.
    """
    if os.path.exists(QUERY_MAP_FILE):
        with open(QUERY_MAP_FILE, "r") as file:
            return json.load(file)
    return {}


def save_query_map(query_map: dict):
    """
    Save the query map to the JSON file.
    """
    with open(QUERY_MAP_FILE, "w") as file:
        json.dump(query_map, file, indent=4)


def load_cached_results(file_path: str) -> List[MatchDict]:
    """
    Load cached query results from a CSV file.
    """
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")


def save_results_to_cache(query: str, results: List[MatchDict]):
    """
    Save the query results to a CSV file and update the query map.
    """
    if not os.path.exists(OLD_QUERIES_DIR):
        os.makedirs(OLD_QUERIES_DIR)

    # Sanitize the query to create a valid filename
    sanitized_query = "".join(
        [c if c.isalnum() or c in (" ", "-", "_") else "_" for c in query]
    )
    file_name = f"{sanitized_query}.csv"
    file_path = os.path.join(OLD_QUERIES_DIR, file_name)

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)

    # Update and save the query map
    query_map = load_query_map()
    query_map[query] = file_name
    save_query_map(query_map)


def get_top_matches(query: str, top_k: int = 20) -> List[MatchDict]:
    """
    Rank all sentences in the dataset for the given query using a CrossEncoder.
    """
    # Load the query map
    query_map = load_query_map()

    # Check if the query has been processed before
    if query in query_map:
        cached_file = os.path.join(OLD_QUERIES_DIR, query_map[query])
        if os.path.exists(cached_file):
            print(f"Loading cached results for query: {query}")
            return load_cached_results(cached_file)
        else:
            print(f"Cached file not found for query: {query}. Recomputing results.")

    # Load the pretrained CrossEncoder model
    model = CrossEncoder(CROSS_ENCODER_MODEL)

    # Load the dataset
    dataset_df = load_dataset(os.path.join(DATADIR, DATASET_FILE))
    if dataset_df.empty:
        return []

    # Prepare the corpus and sentence combinations
    corpus = dataset_df["summary"].fillna("").tolist()
    sentence_combinations = [[query, sentence] for sentence in corpus]

    # Compute similarity scores
    scores = model.predict(sentence_combinations)

    # Add scores to the dataset
    dataset_df["similarity"] = scores

    # Get top `top_k` matches
    top_matches = dataset_df.nlargest(top_k, "similarity")[
        ["title", "link", "published", "summary", "source", "site", "similarity"]
    ]

    # Convert to a list of dictionaries for a clear structure
    results: List[MatchDict] = top_matches.to_dict(orient="records")

    # Save results to cache
    save_results_to_cache(query, results)

    return results


# Example usage
if __name__ == "__main__":
    query = "Sample search query"
    top_results = get_top_matches(query)
    for result in top_results:
        print(result)
