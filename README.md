# 📚 AI Study Assistant

## Application Preview
An AI-powered Study Assistant built using Streamlit and the Google Gemini API.

## Features
* 📄 PDF Upload & Analysis (using PyPDF)
* 💬 AI Chat Assistant 
* 🧠 PDF Summarization (Bullet Points)
* 🎴 Flashcard Generation
* ❓ Dynamic Quiz Generation & Interactive Scoring System
* 🌍 English, Hindi, and Telugu Language Support
* ☁️ Cloud AI Orchestration using Google GenAI SDK

## Tech Stack
* **Frontend/UI:** Streamlit
* **LLM Engine:** Google Gemini (`gemini-2.5-flash`)
* **PDF Parser:** PyPDF
* **Deployment Platform:** Streamlit Community Cloud

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
# project structure
ai-study-assistant/
│
├── app.py           # Main Streamlit Application UI & Logic
├── llm.py           # Google GenAI SDK Client Initialization
├── translations.py  # Multilingual String Dictionary Map
└── requirements.txt # Cloud Application Dependencies
