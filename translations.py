translations = {
    "en": {
        "title": "📚 AI Study Assistant",
        "input": "Ask your question..."
    },
    "hi": {
        "title": "📚 एआई स्टडी असिस्टेंट",
        "input": "अपना प्रश्न पूछें..."
    },
    "te": {
        "title": "📚 AI స్టడీ అసిస్టెంట్",
        "input": "మీ ప్రశ్న అడగండి..."
    }
}

def t(lang, key):
    return translations.get(lang, translations["en"]).get(key, key)