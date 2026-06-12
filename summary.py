from llm import generate_response

def summarize(text, lang):
    prompt = f"""
Summarize the following content in simple points:

{text[:3000]}
"""
    return generate_response(prompt)