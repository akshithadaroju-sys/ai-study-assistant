import streamlit as st
import re
from pypdf import PdfReader

from llm import generate_response
from translations import t

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="centered")

# ---------------- QUIZ TEXT PARSER HELPER ----------------
def parse_quiz_text(quiz_text):
    """
    Parses raw AI quiz text into a structured list of dictionaries.
    Each dictionary contains: question, options (list), and correct_answer.
    """
    # Split the text into individual question blocks using numbers followed by dots/parentheses
    blocks = re.split(r'\n(?=\d+[\\)\.])|\n\s*\n(?=\d+[\\)\.])', quiz_text.strip())
    
    structured_quiz = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Extract the question text (everything up to option A)
        question_match = re.search(r'^(\d+[\).\s]+.*?)(?=\b[A-D]\))', block, re.DOTALL | re.IGNORECASE)
        if not question_match:
            question_match = re.search(r'^(\d+[\).\s]+.*?)(?=\b[A-D][:\s])', block, re.DOTALL | re.IGNORECASE)
            
        # Extract options A, B, C, D
        options = re.findall(r'\b([A-D][\)\.:\s]+.*?)(?=\b[A-D][\)\.:\s]|Answer:|$)', block, re.DOTALL | re.IGNORECASE)
        
        # Extract correct answer
        answer_match = re.search(r'Answer:\s*([A-D])', block, re.IGNORECASE)
        
        if question_match and len(options) >= 4 and answer_match:
            structured_quiz.append({
                "question": question_match.group(1).strip(),
                "options": [opt.strip() for opt in options[:4]],
                "correct_answer": answer_match.group(1).upper()
            })
            
    return structured_quiz

# ---------------- SESSION STATE INITIALIZATION ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- LANGUAGE ----------------
st.sidebar.title("🌍 Language")

lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

lang_label = st.sidebar.selectbox("Choose language", list(lang_map.keys()))
lang = lang_map[lang_label]

# ---------------- STUDY MODE ----------------
st.sidebar.title("📚 Study Mode")
mode = st.sidebar.selectbox(
    "Select mode",
    ["Chat", "Summary", "Quiz", "Flashcards"]
)

# ---------------- PDF UPLOAD ----------------
st.sidebar.title("📄 Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload your notes", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        st.sidebar.success("📄 PDF loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Could not read PDF: {e}")

# ---------------- TITLE ----------------
st.title(t(lang, "title"))

# ---------------- CHAT HISTORY UI ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input(t(lang, "input"))

# Primary background text engine determination
source_text = pdf_text if pdf_text else user_input

# ======================================================
# 💬 CHAT MODE
# ======================================================
if mode == "Chat" and user_input:
    prompt = f"""
You are an AI Study Assistant.
Respond in language: {lang}

User: {user_input}
"""
    with st.spinner("Thinking..."):
        response = generate_response(prompt)
    
    if response and "ERROR" not in response:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ======================================================
# 🧠 SUMMARY MODE
# ======================================================
if mode == "Summary":
    if not source_text:
        st.info("💡 Please upload a PDF in the sidebar or type something in the chat input to summarize.")
    else:
        if st.button("✨ Generate Summary", use_container_width=True):
            with st.spinner("Processing context and generating bullet points..."):
                prompt = f"""
Summarize the content in simple bullet points.
Respond in language: {lang}

Content:
{source_text[:3000]}
"""
                st.session_state.summary_data = generate_response(prompt)

        if "summary_data" in st.session_state:
            st.subheader("🧠 Summary")
            st.write(st.session_state.summary_data)

# ======================================================
# ❓ QUIZ MODE
# ======================================================
if mode == "Quiz":
    if not source_text:
        st.info("💡 Please upload a PDF or interact with the chat bar to supply source material for a quiz.")
    else:
        if st.button("🎯 Generate New Quiz", use_container_width=True):
            with st.spinner("Building custom evaluation quiz..."):
                prompt = f"""
Create a 5-question multiple choice quiz based ONLY on the content provided.

RULES:
- Format each question with a number (e.g., 1., 2.)
- Provide exactly 4 options labeled exactly as: A) , B) , C) , D)
- Conclude each question block with the exact phrase: Answer: X (where X is A, B, C, or D)
- Respond in language: {lang}

Content:
{source_text[:3000]}
"""
                generated_quiz = generate_response(prompt)
                if "ERROR" not in generated_quiz:
                    st.session_state.quiz_data = generated_quiz

        # Only display if quiz data exists in state
        if st.session_state.quiz_data:
            parsed_questions = parse_quiz_text(st.session_state.quiz_data)
            
            if not parsed_questions:
                st.error("⚠️ The AI output format was unexpected. Please click 'Generate New Quiz' again.")
                with st.expander("Show raw output debug info"):
                    st.code(st.session_state.quiz_data)
            else:
                st.subheader("✍️ Take Your Quiz")
                user_answers = []
                
                # Loop through structured questions blocks and mount radios underneath them
                for idx, q_item in enumerate(parsed_questions):
                    st.markdown(f"### {q_item['question']}")
                    
                    user_ans_label = st.radio(
                        "Choose your answer:",
                        q_item["options"],
                        key=f"quiz_q_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    selected_letter = user_ans_label[0].upper() if user_ans_label else "A"
                    user_answers.append(selected_letter)
                    st.divider()

                if st.button("Submit Checked Answers", type="primary", use_container_width=True):
                    score = 0
                    results_output = []
                    
                    for i, q_item in enumerate(parsed_questions):
                        correct = q_item["correct_answer"]
                        chosen = user_answers[i]
                        
                        if chosen == correct:
                            score += 1
                            results_output.append(f"✅ **Question {i+1}**: Correct! You chose {chosen}.")
                        else:
                            results_output.append(f"❌ **Question {i+1}**: Incorrect. You chose {chosen}, but the correct answer was **{correct}**.")
                    
                    st.session_state.score += score
                    st.session_state.total_questions += len(parsed_questions)
                    
                    st.success(f"🎯 Quiz Checked! You scored {score}/{len(parsed_questions)} on this attempt.")
                    for res in results_output:
                        st.write(res)
                    
                    # Wipe the layout quiz session token so users don't resubmit stale radio groups
                    st.session_state.quiz_data = None
                    st.button("🔄 Click to Clear Completed Quiz & Update Progress Dashboard", use_container_width=True)

# ======================================================
# 🧾 FLASHCARDS MODE
# ======================================================
if mode == "Flashcards":
    if not source_text:
        st.info("💡 Supply data via PDF upload or text bar input to spin up customized memory flashcards.")
    else:
        if st.button("🎴 Generate Flashcards", use_container_width=True):
            with st.spinner("Assembling flashcards..."):
                prompt = f"""
Create 5 flashcards in Q&A format.
Respond in language: {lang}

Content:
{source_text[:3000]}
"""
                st.session_state.flashcard_data = generate_response(prompt)

        if "flashcard_data" in st.session_state:
            st.subheader("🧾 Flashcards")
            st.write(st.session_state.flashcard_data)

# ======================================================
# 📊 SIDEBAR PROGRESS TRACKER
# ======================================================
st.sidebar.divider()
st.sidebar.title("📊 Progress Tracker")

if st.session_state.total_questions > 0:
    accuracy = (st.session_state.score / st.session_state.total_questions) * 100
else:
    accuracy = 0.0

st.sidebar.metric("Cumulative Score", st.session_state.score)
st.sidebar.metric("Total Questions Attempted", st.session_state.total_questions)
st.sidebar.metric("Performance Accuracy", f"{accuracy:.2f}%")

if st.sidebar.button("Clear Dashboard Progress", use_container_width=True):
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.quiz_data = None
    if "summary_data" in st.session_state: 
        del st.session_state.summary_data
    if "flashcard_data" in st.session_state: 
        del st.session_state.flashcard_data
    st.rerun()