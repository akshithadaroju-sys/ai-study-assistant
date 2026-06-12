import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI study assistant that explains concepts simply."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]