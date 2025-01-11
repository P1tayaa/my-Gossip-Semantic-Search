# Gossip Semantic Search

This project is a semantic search application designed as part of an assignment for **LinkUp**. The application uses sentence-transformer model to provide meaningful search results based on user queries.

---

## Features

- **Sentence Transformer**: Embeds input queries and data for efficient similarity searches.
- **Cross Encoder**: Reranks results for improved precision using transformer models.
- **REST API**: Exposes endpoints for querying and fetching results.

---

## Technologies Used

- **Python**: Core backend language.
- **Flask**: Lightweight framework for creating the REST API.
- **Docker**: Containerization for easy deployment and consistent environments.
- **Transformers**: Hugging Face library for loading NLP models.
- **Sentence Transformers**: Framework for building semantic search applications.

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- Internet connection (for downloading models)
- Nvidia graphics card

### Clone the Repository

```bash
git clone <repository_url>
cd gossip-semantic-search
```

### To run with Docker

```bash
sudo docker compose up --build
```

### To run it on local machine (tested on my linux)

```bash
python backend/app.py
```
