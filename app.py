import streamlit as st
from chatbot_logic import get_bot_response
from logger import get_public_ip, get_geolocation, log_threat
from datetime import datetime

# Page setup
st.set_page_config(page_title="Cybersecurity Chatbot", page_icon="🤖", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }
        .stButton > button {
            background-color: #00bcd4;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #00ffe7;'>🤖 Cybersecurity AI Chatbot</h2>", unsafe_allow_html=True)

# Chat session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input area
user_input = st.text_input("Ask about threats or security tips...", key="input")

if user_input:
    # Append user query
    st.session_state.chat.append(("You", user_input))

    # Run logic
    bot_reply, threat_flag, threat_terms = get_bot_response(user_input)

    # Log IP + geo + threats
    ip = get_public_ip()
    geo = get_geolocation(ip)
    log_threat(ip, geo, user_input, threat_flag, threat_terms)

    # Append bot response
    st.session_state.chat.append(("Bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.chat:
    if sender == "You":
        st.markdown(f"<div style='background-color:#00ffc3; padding:10px; border-radius:10px; text-align:right; margin-bottom:8px'><strong>{sender}:</strong> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:#3949ab; padding:10px; border-radius:10px; text-align:left; margin-bottom:8px; color:white'><strong>{sender}:</strong> {msg}</div>", unsafe_allow_html=True)

# Warning
st.markdown("<p style='text-align:center; font-size:12px; color: #f9a825;'>⚠ Your IP & location are logged for security threat analysis.</p>", unsafe_allow_html=True)