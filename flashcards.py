from llm import generate_response

def generate_flashcards(text, lang):
    prompt = f"""
You are an expert teacher AI.

Create 5 high-quality flashcards from the given content.

IMPORTANT RULES:
- Respond in language: {lang}
- Each flashcard must be in this format:
Q: question
A: answer
- Keep answers short and clear
- Focus on important exam points

Content:
{text[:3000]}
"""
    return generate_response(prompt)