from app.rag.chroma_store import collection
from app.rag.embed import embed_text
import uuid


def add_documents(docs):
    ids = [str(uuid.uuid4()) for _ in docs]

    collection.add(
        documents=docs,
        embeddings=[embed_text(doc) for doc in docs],
        ids=ids
    )


def retrieve(query):
    results = collection.query(
        query_embeddings=[embed_text(query)],
        n_results=3
    )

    print("ChromaDB query results:", results)

    return results["documents"][0]