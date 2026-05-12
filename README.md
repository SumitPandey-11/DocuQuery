# DocuQuery

A local RAG system for asking questions about PDF documents. Everything runs on your machine — no API keys, no cloud, no data leaving your computer.

Built this because I wanted to be able to query my own documents without feeding them to some third-party service.

## What it does

Upload a PDF, ask questions about it, get answers. That's it.

Under the hood it extracts text from your PDF, splits it into chunks, embeds them with Sentence Transformers, stores the vectors in FAISS, and when you ask something it pulls the relevant chunks and feeds them to a local Llama3 model via Ollama.

## Stack

- Django (backend)
- Ollama + llama3 (local LLM)
- FAISS (vector search)
- Sentence Transformers — `all-MiniLM-L6-v2` (embeddings)
- PyMuPDF (PDF text extraction)

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running

Pull the model before you start:
```bash
ollama run llama3
```

## Setup

```bash
git clone <repository-url>
cd docqa

pip install django faiss-cpu sentence-transformers pymupdf ollama

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

Then open `http://127.0.0.1:8000`.

## A couple of things to know

Make sure Ollama is running in the background before you try to ask anything. First run is a bit slow — the embedding model and LLM both need a moment to load.

If you're running this for the first time, the `ollama run llama3` step will download the model which is a few GBs, so give it some time.
