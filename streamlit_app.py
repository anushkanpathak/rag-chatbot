import streamlit as st
from repo_loader import load_repo
from vector_store import build_vector_db 
from llm_engine import load_llm
from rag_pipeline import ask_question

st.set_page_config(page_title="GitHub RAG Chatbot", layout="wide")

st.title("💬 GitHub Repo Chatbot")

# 🔥 Session state (important)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "model" not in st.session_state:
    st.session_state.model = None

# 🔗 Repo input
repo_url = st.text_input("Enter GitHub Repo URL")
if st.button("Load Repository"):
    if not repo_url:
        st.warning("Please enter repo URL")
        st.stop()

    with st.spinner("Loading repo..."):
        docs = load_repo(repo_url)
        db = build_vector_db(docs)
        st.session_state.retriever = db.as_retriever(search_kwargs={"k": 3})
        st.session_state.model = load_llm()
    st.success("Repo loaded successfully!")

# 💬 Ask question
# question = st.text_input("Ask your question")
# if st.button("Ask") and st.session_state.retriever and question:

#     with st.spinner("Thinking..."):
#         answer = ask_question(
#             question,
#             st.session_state.retriever,
#             st.session_state.model,
#             st.session_state.chat_history
#         )

#     # 🔥 Save chat
#     if not st.session_state.chat_history or st.session_state.chat_history[-1][0] != question:
#      st.session_state.chat_history.append((question, answer))
with st.form("chat_form", clear_on_submit=True):

    question = st.text_input("Ask your question")

    submitted = st.form_submit_button("Ask")

    if submitted and st.session_state.retriever and question:

        with st.spinner("Thinking..."):
            answer = ask_question(
                question,
                st.session_state.retriever,
                st.session_state.model,
                st.session_state.chat_history
            )

        st.session_state.chat_history.append((question, answer))


# 🧾 Show chat history
st.markdown("## 💬 Chat History")

for q, a in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {q}")
    st.markdown("**🤖 Bot:**")
    st.markdown(a)
    st.markdown("---")