from langchain_community.llms import Ollama

# Load the model once
llm = Ollama(model="llama3")

def generate_response(prompt):
    """
    Sends prompt to LLM and returns response
    """
    return llm.invoke(prompt)