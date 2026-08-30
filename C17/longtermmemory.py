import uuid
from langchain_openrouter import ChatOpenRouter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

llm = ChatOpenRouter(model="gpt-4o-mini")

episodic_memory = Chroma(
        collection_name="episodic_memory", 
        embedding_function=embeddings, 
        persist_directory="./memory",
        collection_metadata=
            {"hnsw:space": "cosine"}
        )

semantic_memory = Chroma(
    collection_name="semantic_memory", 
        embedding_function=embeddings, 
        persist_directory="./memory",
        collection_metadata=
            {"hnsw:space": "cosine"}
        )


THRESHOLD = 0.2
CONSOLIDATE_AFTER = 5 # after 5 raw conversations, it consolidates and distills episodic memory and updates semantic memory after 5 interactions with the user

def add_to_episodic_memory(user, text):
    episodic_memory.add_documents(
        [Document(page_content=text, metadata={"user": user, "id": str(uuid.uuid4())})]
    )

def add_facts(user, facts):
    if facts:
        episodic_memory
        semantic_memory.add_documents(
            [Document(page_content=f, metadata={"user": user}) for f in facts]
        )

def search(store, user, query, k=4):
   # semilarity search with scroe, filtered by 
   # user and threshold
   hits = store.similarity_search_with_score(
       query,
       k=k,
       filter={"user": user}
   )
   return [doc.page_content for doc, score in hits if score >= THRESHOLD]

def consolidate(user):
    # pull all raw episotes for this user
    got = episodic_memory.get(
        where={"user": user}
    )

    ids, docs = got["ids"], got["documents"]
    if len(ids) < CONSOLIDATE_AFTER:
        return
    # proceed with consolidation logic here
    joined = "\n".join(docs)

    resp = llm.invoke(
        f"Extract durable, general facts about the user from those exchanges. One fact per line, no numbering. Skip anything trivial or one-off").content

    facts = [line.strip("-. ").strip() for line in resp.splitlines() if line.strip()]

    add_facts(user, facts)
    # Optionally, remove the consolidated episodic memories
    episodic_memory.delete(ids=ids)
    print(f"[Consolidated {len(ids)} episodic -> {len(facts)} facts]")


def answer(user, query):
    # All knwon facts for this user
    # direct lookup by id - always available

    facts = semantic_memory.get(
        where={"user": user}
    )["documents"]

    # Topically relevant past exchanges (similarity search)

    recent = search(episodic_memory, user, query)

    context = ""
    if facts:
        context += "Known facts about the user:\n" + "\n".join(f"- {f}" for f in facts) + "\n\n"
    if recent:
        context += "Relevant past exchanges:\n" + "\n".join(f"- {r}" for r in recent) + "\n\n"


    reply = llm.invoke(
        f"{context}The user's id is '{user}'. The known facts above are about "
        f"this user — treat 'me', 'I', and 'my' as referring to them.\n\n"
        f"User says: {query}\n\nRespond helpfully using any relevant memory above."
    ).content

    add_to_episodic_memory(user, f"User says: {query}\nAssistant replies: {reply}")
    consolidate(user)
    return reply

def main():
    user = input("User id: ").strip() or "default"
    print("Chat (blank line to quit). Memory persists across runs.\n")
    while True:
        q = input("> ").strip()
        if not q:
            break
        print(answer(user, q), "\n")


if __name__ == "__main__":
    main()