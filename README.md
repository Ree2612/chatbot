🛡️ Cybersecurity-Aware Chatbot

A Streamlit-powered AI chatbot that detects cybersecurity-related queries, identifies threats in real-time, logs user geolocation + IP, and provides intelligent responses using Cohere’s AI API + spaCy NLP.
Includes an admin dashboard with threat visualizations and a Leaflet-based map of logged attacks

🚀 Features
🧠 Smart AI Chatbot using Cohere’s Command-R model

🕵️‍♀️ Threat keyword detection (e.g., phishing, malware, XSS)

🌐 IP address & geolocation tracking

🗂️ Admin panel with live log table, threat frequency graph & map

🔊 Optional ping sound for bot replies

💬 Polished modern cyber-themed UI

📁 Project Structure
![struct](https://github.com/user-attachments/assets/4106bf0a-ac2c-400a-9ba9-7e25226b6bc6)

🌍 API & Model Integration
Cohere Command-R: Handles general questions

spaCy: Detects greetings and threat keywords

ip-api.com: Retrieves IP geolocation

folium: Map plotting in admin panel
