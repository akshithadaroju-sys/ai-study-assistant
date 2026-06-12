from llm import generate_response

def generate_flashcards(text, lang):
    prompt = f"""
Create 5 flashcards from this text.

Format:
Q: ...
A: ...

Text:
{text[:3000]}
"""
    return generate_response(prompt)