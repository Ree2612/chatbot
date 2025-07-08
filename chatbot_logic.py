import spacy
import cohere
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Cybersecurity threat definitions
cyber_knowledge = {
    "phishing": "Phishing is a type of social engineering attack used to steal user data.",
    "malware": "Malware is malicious software designed to damage or gain unauthorized access.",
    "ransomware": "Ransomware locks your files and demands payment for access.",
    "sql injection": "SQL Injection exploits vulnerable input fields to run unauthorized SQL commands.",
    "xss": "XSS (Cross-Site Scripting) allows attackers to inject client-side scripts.",
    "hacking": "Hacking is the act of gaining unauthorized access to systems by exploiting vulnerabilities."
}

def detect_threat(user_input):
    lower = user_input.lower()
    return [term for term in cyber_knowledge if term in lower]

def get_bot_response(user_input):
    user_input = user_input.strip()
    doc = nlp(user_input.lower())

    # Rule-based quick replies
    if any(token.lemma_ in ["hi", "hello", "hey", "hii", "namaste"] for token in doc):
        return "👋 Hello! How can I help you with cybersecurity?", False, []

    if "name" in user_input.lower():
        return "🤖 I'm your Cybersecurity-Aware Assistant.", False, []

    if "thank" in user_input.lower():
        return "You're welcome! Stay safe online 🛡️", False, []

    if any(token.lemma_ in ["bye", "goodbye", "see", "later"] for token in doc):
        return "👋 Goodbye! Stay cyber-safe!", False, []

    if any(phrase in user_input.lower() for phrase in ["how are you", "what are you doing"]):
        return "I'm doing great, thanks for asking!", False, []

    # Detect cybersecurity keywords
    threats_found = detect_threat(user_input)
    if threats_found:
        response = "\n\n".join(f"{term.capitalize()}: {cyber_knowledge[term]}" for term in threats_found)
        return response, True, threats_found

    if len(user_input.split()) <= 2:
        return "🤔 Could you elaborate? Try asking about malware, phishing, etc.", False, []

    # Fallback: Use Cohere API
    try:
        response = co.chat(message=user_input, model="command-r")
        return f"🤖 {response.text.strip()}", False, []
    except Exception as e:
        return f"❌ Error using Cohere: {str(e)}", False, []
