from app.rag.pdf_loader import load_pdfs
from app.rag.chunker import chunk_text
from app.rag.retriever import add_documents

PDF_FOLDER = "app/rag/docs"

pdf_texts = load_pdfs(PDF_FOLDER)


all_chunks = []

for text in pdf_texts:
    chunks = chunk_text(text)
    all_chunks.extend(chunks)

if not all_chunks:
    print("NO CHUNKS FOUND — STOPPING")
    exit()
print("TOTAL CHUNKS:", len(all_chunks))

add_documents(all_chunks)

print("PDFs loaded into vector DB")
