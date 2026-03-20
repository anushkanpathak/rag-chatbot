from repo_loader import load_repo
from vector_store import build_vector_db
from llm_engine import load_llm
from rag_pipeline import ask_question


def main():

    repo_url = input("Enter GitHub repo URL: ")

    print("Loading repository...")
    documents = load_repo(repo_url)

    print("Building vector DB...")
    db = build_vector_db(documents)

    retriever = db.as_retriever(search_kwargs={"k": 5})

    model = load_llm()
    chat_history = []

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        answer = ask_question(question, retriever, model, chat_history)
        chat_history.append((question, answer))

        print("\nAnswer:\n", answer)
        


if __name__ == "__main__":
    main()