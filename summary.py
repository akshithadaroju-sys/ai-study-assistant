from llm import generate_response

def summarize(text, lang):
    prompt = f"""
You are an expert teacher AI.

Summarize the following content in SIMPLE, CLEAR bullet points.

IMPORTANT RULES:
- Respond in language: {lang}
- Use short bullet points only
- Focus on key exam points
- Do NOT add unnecessary explanation
- Keep it easy to understand for students

Content:
{text[:3000]}
"""
    return generate_response(prompt)