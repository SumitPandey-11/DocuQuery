import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama
import os
import pickle
import re

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=600, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def create_vector_store(chunks):
    embeddings = embedding_model.encode(chunks, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index, chunks

def search_relevant_chunks(query, index, chunks, k=6):
    query_vec = embedding_model.encode([query], normalize_embeddings=True)
    distances, indices = index.search(np.array(query_vec).astype('float32'), k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]

def save_index(index, chunks, file_id):
    faiss.write_index(index, f"{file_id}.index")
    with open(f"{file_id}.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_index(file_id):
    index_path = f"{file_id}.index"
    chunk_path = f"{file_id}.pkl"

    if os.path.exists(index_path) and os.path.exists(chunk_path):
        index = faiss.read_index(index_path)
        with open(chunk_path, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks

    return None, None

def clean_output(text):
    text = re.sub(r'(?i)according to.*?:?', '', text)
    text = re.sub(r'\s+', ' ', text)

    lines = text.split('. ')
    bullets = []

    for line in lines:
        line = line.strip()
        if len(line) > 5:
            bullets.append(f"• {line}")

    return "\n".join(bullets[:10])

def generate_answer(query, context):
    context = context[:2500]

    system_prompt = """
You are a strict document-based AI assistant.

Rules:
- Use ONLY the given context
- Do NOT guess
- If not found → say "Not found in document"
- Answer in exactly 8 to 10 bullet points
- Each point must be a complete, informative sentence
- No long paragraphs
"""

    user_prompt = f"""
CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ]
        )

        output = response['message']['content']
        return clean_output(output)

    except Exception as e:
        return f"Error: {str(e)}"