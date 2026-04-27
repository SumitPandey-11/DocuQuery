from django.shortcuts import render
from .models import Document
from .utils import (
    extract_text,
    chunk_text,
    create_vector_store,
    search_relevant_chunks,
    generate_answer
)
import os


def upload_and_ask(request):
    answer = ""
    error = ""
    file_name = ""
    chunks_used = []

    if request.method == "POST":
        file = request.FILES.get("file")
        question = request.POST.get("question")

        # ✅ STEP 1: Handle file upload
        if file:
            if not file.name.endswith(".pdf"):
                error = "Only PDF files are allowed!"
                return render(request, "qa/index.html", {"error": error})

            doc = Document.objects.create(file=file)
            pdf_path = doc.file.path

            # Save path in session (IMPORTANT)
            request.session["pdf_path"] = pdf_path
            file_name = file.name

        # ✅ STEP 2: Get stored PDF
        pdf_path = request.session.get("pdf_path")

        if not pdf_path:
            error = "Please upload a PDF first."
            return render(request, "qa/index.html", {"error": error})

        file_name = os.path.basename(pdf_path)

        # ✅ STEP 3: Process only if question exists
        if question:
            try:
                # Extract + chunk
                text = extract_text(pdf_path)
                chunks = chunk_text(text)

                # Create vector DB
                index, chunks = create_vector_store(chunks)

                # Search relevant chunks
                relevant = search_relevant_chunks(question, index, chunks)

                # Build context (LIMIT IMPORTANT)
                context = " ".join(relevant)
                context = context[:2500]

                # Generate answer
                answer = generate_answer(question, context)
                chunks_used = relevant

            except Exception as e:
                error = f"Error: {str(e)}"

    return render(request, "qa/index.html", {
        "answer": answer,
        "error": error,
        "file_name": file_name,
        "chunks_used": chunks_used
    })