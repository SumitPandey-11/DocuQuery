# DocuQuery: Local Document Q&A System

DocuQuery is a privacy-first, local RAG (Retrieval-Augmented Generation) system that allows users to upload PDF documents and ask questions about their content. The system ensures that all processing happens locally, with no data leaving your machine.

## 🚀 Features
- **PDF Upload**: Easily upload any PDF document.
- **Local LLM**: Powered by **Ollama** (llama3) for high-quality responses.
- **Vector Search**: Uses **FAISS** and **Sentence Transformers** for efficient document retrieval.
- **Privacy First**: No external APIs or internet connection required (once models are downloaded).
- **Premium UI**: Modern, glassmorphic design for a superior user experience.

## 🛠️ Tech Stack
- **Backend**: Django
- **LLM Engine**: Ollama (llama3)
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **PDF Processing**: PyMuPDF (fitz)

## 📋 Prerequisites
1. **Python 3.9+**
2. **Ollama**: [Download and Install Ollama](https://ollama.com/)
3. **Llama3 Model**: Run the following command in your terminal:
   ```bash
   ollama run llama3
   ```

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd docqa
   ```

2. **Install dependencies**:
   ```bash
   pip install django faiss-cpu sentence-transformers pymupdf ollama
   ```

3. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

5. **Open the app**:
   Visit `http://127.0.0.1:8000` in your browser.

## 🧠 How it Works
1. **Extraction**: The system uses PyMuPDF to extract text from the uploaded PDF.
2. **Chunking**: Text is split into manageable chunks with overlapping context.
3. **Embedding**: Each chunk is converted into a vector embedding using Sentence Transformers.
4. **Retrieval**: When a question is asked, the system finds the most relevant chunks using FAISS similarity search.
5. **Generation**: The relevant context + the question are sent to the local Llama3 model via Ollama to generate a precise answer.

## 📝 Note
Ensure Ollama is running in the background before asking questions. The first time you run it, it might take a few seconds to load the embedding model and the LLM.
