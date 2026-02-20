import argparse
from typing import List, Tuple

from production_rag_system.config import get_settings, get_embeddings, get_llm, get_vectorstore

PROMPT_TEMPLATE = """Tu es un assistant qui répond uniquement à partir du CONTEXTE.
Si l'information n'est pas dans le contexte, dis: "Je ne sais pas d'après le document."

CONTEXTE:
{context}

QUESTION:
{question}

Réponse (en français, concise, précise):
"""

def format_context(docs) -> str:
    parts = []
    for d in docs:
        src = d.metadata.get("source", "document")
        page = d.metadata.get("page", None)
        prefix = f"[Source: {src}" + (f", page {page}]" if page is not None else "]")
        parts.append(prefix + "\n" + d.page_content)
    return "\n\n---\n\n".join(parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="Ta question")
    parser.add_argument("--k", type=int, default=None, help="Top-k passages (override)")
    args = parser.parse_args()

    settings = get_settings()
    embeddings = get_embeddings(settings)
    llm = get_llm(settings)
    vs = get_vectorstore(settings, embeddings)

    k = args.k if args.k is not None else settings.k

    # similarity_search_with_relevance_scores renvoie (doc, score)
    results: List[Tuple[object, float]] = vs.similarity_search_with_relevance_scores(args.q, k=k)

    # filtre optionnel par score
    filtered_docs = []
    sources = []
    for doc, score in results:
        if score >= settings.score_threshold:
            filtered_docs.append(doc)
            src = doc.metadata.get("source", "document")
            page = doc.metadata.get("page", None)
            sources.append((src, page, score))

    if not filtered_docs:
        print("⚠️ Aucun passage pertinent trouvé (essaie d'augmenter k ou baisser score_threshold).")
        return

    context = format_context(filtered_docs)
    prompt = PROMPT_TEMPLATE.format(context=context, question=args.q)

    answer = llm.invoke(prompt).content

    print("\n🧠 RÉPONSE:\n")
    print(answer)

    print("\n📚 SOURCES (top):")
    for src, page, score in sources:
        p = f"page {page}" if page is not None else "page ?"
        print(f"- {src} ({p}) score={score:.3f}")

if __name__ == "__main__":
    main()
