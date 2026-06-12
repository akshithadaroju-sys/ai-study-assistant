from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)
    return chunks


def build_prompt(context, question):
    return f"""
Use the following study material:

{context}

Question: {question}
"""