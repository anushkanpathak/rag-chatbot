
# def ask_question(question, retriever, model, chat_history=None):

#     # ✅ Safe chat history
#     if chat_history is None:
#         chat_history = []

#      # ✅ Make question context-aware
#     if chat_history:
#       last_q, last_a = chat_history[-1]

#     #   question = f"""
#     #   Previous Question: {last_q}
#     #   Previous Answer: {last_a}

#     #   Current Question: {question}

#     #   Rewrite the current question to be a standalone question.
#     # """
#     # ✅ Step 0: Rewrite question (only for retrieval, NOT final answer)
    
# # ✅ Step 0: Rewrite query (for better retrieval)
# query = question

# if chat_history:
#     last_q, last_a = chat_history[-1]

#     rewrite_prompt = f"""
# Convert the following into a clear standalone question.

# Previous Question: {last_q}
# Previous Answer: {last_a}

# Follow-up Question: {question}
# """

#     rewritten = model.generate_content(rewrite_prompt)

#     # ✅ Safe extraction
#     if hasattr(rewritten, "text"):
#         query = rewritten.text
#     else:
#         query = question


# # ✅ Use rewritten query for retrieval
# docs = retriever.invoke(query) if hasattr(retriever, "invoke") else retriever.get_relevant_documents(query)
# ```


#     rewritten = model.generate_content(rewrite_prompt)

#     query = rewritten.text if hasattr(rewritten, "text") else question

#     # ✅ Retriever compatibility
#     docs = retriever.invoke(question) if hasattr(retriever, "invoke") else retriever.get_relevant_documents(question)

#     if not docs:
#         return "No relevant information found in the repository."

#     # ✅ Deduplicate similar chunks
#     seen = set()
#     unique_docs = []

#     for doc in docs:
#         content = doc.page_content[:300]

#         if content not in seen:
#             seen.add(content)
#             unique_docs.append(doc)

#     # ✅ Build context
#     context = "\n\n".join(
#         f"FILE: {doc.metadata.get('source', 'unknown')}\n{doc.page_content[:800]}"
#         for doc in unique_docs
#     )

#     # ✅ Format chat history (last 3 only)
#     history_text = "\n\n".join(
#     f"User: {q}\nAssistant: {a}" for q, a in chat_history[-3:]
#    )

#     # ✅ YOUR ORIGINAL PROMPT (unchanged)
#     prompt = f"""

# You are an expert code assistant.

# Answer ONLY using the provided repository context.
# Conversation so far:
# {history_text}

# Format your answer like this:

# ### Summary (2-3 lines)
# Give a short, direct answer.

# ### Detailed Explanation
# Explain clearly using context.

# ### Code References
# Mention file names and include code snippets.
# - Mention file names
# - Include SHORT code snippets (max 10-15 lines)
# - Highlight important lines

# Avoid repeating similar explanations

# If answer is not present, say:
# "Answer not found in the repository."
# Do NOT repeat similar points. Avoid redundancy.
# Use conversation history to understand follow-up questions.
# ---------------------
# CONTEXT:
# {context}
# ---------------------

# QUESTION:
# {question}
# """

#     # ✅ Generate response safely
#     response = model.generate_content(prompt)

#     return response.text if hasattr(response, "text") else str(response)

def ask_question(question, retriever, model, chat_history=None):

    # ✅ Safe chat history
    if chat_history is None:
        chat_history = []

    # ✅ Step 0: Rewrite query (for better retrieval)
    query = question

    if chat_history:
        last_q, last_a = chat_history[-1]

        rewrite_prompt = f"""
Convert the following into a clear standalone question.

Previous Question: {last_q}
Previous Answer: {last_a}

Follow-up Question: {question}
"""

        rewritten = model.generate_content(rewrite_prompt)

        if hasattr(rewritten, "text"):
            query = rewritten.text
        else:
            query = question

    # ✅ Use rewritten query for retrieval
    docs = retriever.invoke(query) if hasattr(retriever, "invoke") else retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant information found in the repository."

    # ✅ Deduplicate similar chunks
    seen = set()
    unique_docs = []

    for doc in docs:
        content = doc.page_content[:300]

        if content not in seen:
            seen.add(content)
            unique_docs.append(doc)

    # ✅ Build context
    context = "\n\n".join(
        f"FILE: {doc.metadata.get('source', 'unknown')}\n{doc.page_content[:800]}"
        for doc in unique_docs
    )

    # ✅ Format chat history (last 3 only)
    history_text = "\n\n".join(
        f"User: {q}\nAssistant: {a}" for q, a in chat_history[-3:]
    )

    # ✅ YOUR ORIGINAL PROMPT
    prompt = f"""

You are an expert code assistant.

Answer ONLY using the provided repository context.
Conversation so far:
{history_text}

Format your answer like this:

### Summary (2-3 lines)
Give a short, direct answer.

### Detailed Explanation
Explain clearly using context.

### Code References
Mention file names and include code snippets.
- Mention file names
- Include SHORT code snippets (max 10-15 lines)
- Highlight important lines

Wrap all code snippets inside ```python ``` blocks
Always include at least one concrete code example if available.

Avoid repeating similar explanations
If partial information is available, still answer using best possible context.
If question is broad, infer related code concepts like routers, decorators, or request handling.

If answer is not present, say:
"Answer not found in the repository."
Do NOT repeat similar points. Avoid redundancy.
Use conversation history to understand follow-up questions.
---------------------
CONTEXT:
{context}
---------------------

QUESTION:
{question}
"""

    # ✅ Generate response safely
    response = model.generate_content(prompt)

    return response.text if hasattr(response, "text") else str(response)

