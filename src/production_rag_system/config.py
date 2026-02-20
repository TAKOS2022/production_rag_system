import os
from dataclasses import dataclass
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import PGVector

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    database_url: str  # e.g. postgresql+psycopg://rag:rag@localhost:5432/ragdb
    collection_name: str = "docs"
    k: int = 4
    score_threshold: float = 0.25  # ajuste selon ton cas (0-1)

def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    db_url = os.getenv("DATABASE_URL", "").strip()
    collection = os.getenv("PGVECTOR_COLLECTION", "docs").strip()

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY manquant dans .env")
    if not db_url:
        raise RuntimeError("DATABASE_URL manquant dans .env")

    return Settings(
        openai_api_key=api_key,
        database_url=db_url,
        collection_name=collection,
    )

def get_embeddings(settings: Settings) -> OpenAIEmbeddings:
    # Tu peux changer le modèle d'embedding ici plus tard
    return OpenAIEmbeddings(api_key=settings.openai_api_key)

def get_llm(settings: Settings) -> ChatOpenAI:
    # Tu peux changer le modèle ici plus tard
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.0")),
    )

def get_vectorstore(settings: Settings, embeddings: OpenAIEmbeddings) -> PGVector:
    return PGVector(
        connection_string=settings.database_url,
        collection_name=settings.collection_name,
        embedding_function=embeddings,
    )
