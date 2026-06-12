import json
import os

# ---------------- LOAD TRANSLATIONS ----------------
def load_translations(lang):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "translations", f"{lang}.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- AI LANGUAGE CONTROL ----------------
def get_instruction(lang):
    return {
        "en": "Answer ONLY in English.",
        "hi": "Answer ONLY in Hindi.",
        "te": "Answer ONLY in Telugu."
    }.get(lang, "Answer ONLY in English.")