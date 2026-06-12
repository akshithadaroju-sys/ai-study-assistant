import streamlit as st
from llm import generate_response
from rag import process_text, build_prompt

st.title("📚 AI Study Assistant (Cloud Version)")

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload your PDF / Notes", type=["pdf", "txt"])

context = ""

if uploaded_file:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    chunks = process_text(text)
    context = "\n".join(chunks[:5])

user_input = st.text_input("Ask your question")

if user_input:
    prompt = build_prompt(context, user_input)

    response = generate_response(prompt)

    st.session_state.messages.append((user_input, response))

for q, a in st.session_state.messages:
    st.write("🧑‍🎓 You:", q)
    st.write("🤖 AI:", a)