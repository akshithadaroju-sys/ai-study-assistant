import streamlit as st
from rag import extract_text
from llm import generate_response
from utils import load_translations, get_instruction

from summary import summarize
from flashcards import generate_flashcards
from quiz import generate_quiz

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Study Assistant", page_icon="📚")

# ---------------- LANGUAGE SELECTOR ----------------
language_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

selected_language = st.sidebar.selectbox(
    "🌐 Choose Language",
    list(language_map.keys()),
    index=0
)

lang = language_map[selected_language]
t = load_translations(lang)

# ---------------- UI ----------------
st.title("📚 " + t["title"])

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# ---------------- SIDEBAR ----------------
uploaded_file = st.sidebar.file_uploader(t["upload_pdf"], type="pdf")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- PDF PROCESSING ----------------
if uploaded_file:
    st.session_state.pdf_text = extract_text(uploaded_file)
    st.sidebar.success("PDF Loaded Successfully!")

# ---------------- FEATURE BUTTONS ----------------
st.sidebar.markdown("## ⚡ AI Tools")

if st.sidebar.button("🧾 Summarize PDF"):
    if st.session_state.pdf_text:
        result = summarize(st.session_state.pdf_text, lang)
        st.subheader("📄 Summary")
        st.write(result)
    else:
        st.warning("Upload a PDF first")

if st.sidebar.button("🃏 Generate Flashcards"):
    if st.session_state.pdf_text:
        result = generate_flashcards(st.session_state.pdf_text, lang)
        st.subheader("Flashcards")
        st.write(result)
    else:
        st.warning("Upload a PDF first")

if st.sidebar.button("📝 Generate Quiz"):
    if st.session_state.pdf_text:
        result = generate_quiz(st.session_state.pdf_text, lang)
        st.subheader("Quiz")
        st.write(result)
    else:
        st.warning("Upload a PDF first")

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- CHAT INPUT ----------------
user_question = st.chat_input(t["ask_question"])

if user_question:

    st.session_state.messages.append({"role": "user", "content": user_question})
    st.chat_message("user").write(user_question)

    context = st.session_state.pdf_text
    instruction = get_instruction(lang)

    if context and len(context.strip()) > 50:
        prompt = f"""
{instruction}

You are an Advanced AI Study Assistant.

Use the context below:

CONTEXT:
{context[:2500]}

QUESTION:
{user_question}

Answer clearly and simply.
"""
    else:
        prompt = f"""
{instruction}

Question:
{user_question}
"""

    try:
        response = generate_response(prompt)
    except Exception as e:
        response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)