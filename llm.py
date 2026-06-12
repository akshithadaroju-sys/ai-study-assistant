import os
from google import genai
from google.genai.errors import ServerError

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except ServerError as e:
        # Catch 503 errors and return a clean fallback string
        print(f"Google API Server Error: {e}")
        return "ERROR_503_OVERLOAD"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "ERROR_GENERIC"