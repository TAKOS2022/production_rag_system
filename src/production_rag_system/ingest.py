import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector

from production_rag_system.config import get_settings, get_embeddings

def ingest_pdf(pdf_path: str, reset: bool = False) -> None:
    settings = get_settings()
    embeddings = get_embeddings(settings)

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()  # documents avec metadata (source, page, etc.)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(__import__("os").getenv("CHUNK_SIZE", "900")),
        chunk_overlap=int(__import__("os").getenv("CHUNK_OVERLAP", "150")),
    )
    chunks = splitter.split_documents(docs)

    # reset = drop la collection avant d'ingérer
    if reset:
        PGVector(
            connection_string=settings.database_url,
            collection_name=settings.collection_name,
            embedding_function=embeddings,
            pre_delete_collection=True,
        )
        # La ligne ci-dessus efface la collection si elle existe

    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        connection_string=settings.database_url,
        collection_name=settings.collection_name,
    )

    print(f"✅ Ingestion OK: {len(docs)} pages/documents -> {len(chunks)} chunks")
    print(f"📦 Collection: {settings.collection_name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Chemin du PDF (ex: data/docs/mon_doc.pdf)")
    parser.add_argument("--reset", action="store_true", help="Efface la collection avant ingestion")
    args = parser.parse_args()

    ingest_pdf(args.path, reset=args.reset)

if __name__ == "__main__":
    main()
