import re

def parse_quiz_text(quiz_text):
    """
    Parses raw AI quiz text into a structured list of dictionaries.
    Each dictionary contains: question, options (list), and correct_answer.
    """
    # Split the text into individual questions blocks (e.g., "1. What is...", "2. Machine...")
    # This splits by numbers followed by a dot or parenthesis
    blocks = re.split(r'\n(?=\d+[\\)\.])|\n\s*\n(?=\d+[\\)\.])', quiz_text.strip())
    
    # If the first block didn't catch the first question due to lack of a leading newline
    if blocks and not re.match(r'^\d+', blocks[0]):
        # Fallback split if needed, or just handle blocks
        pass

    structured_quiz = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Extract the question text (everything up to option A)
        question_match = re.search(r'^(\d+[\).\s]+.*?)(?=\b[A-D]\))', block, re.DOTALL | re.IGNORECASE)
        if not question_match:
            # Fallback if options are formatted like "A:" or just "A "
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