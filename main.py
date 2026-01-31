import streamlit as st
import google.generativeai as genai
import requests
import threading
import time
import os

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8487111144:AAEfZUn0K2rShXnMrYD9PtadNcaxCdldgyw"
TELEGRAM_CHAT_ID = "8519715726"

# --- API SETUP ---
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing API Key in Streamlit Secrets!")

# --- AI LOGIC ---
def generate_strategy(prompt):
    try:
        # ဒီနေရာမှာ 'models/gemini-1.5-flash' လို့ အသေသပ်ဆုံး ပြင်ထားပါတယ်
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- UI ---
st.title("💼 Nexus CEO Command Bridge")
if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Direct me, Boss..."):
    st.session_state.history.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    
    resp = generate_strategy(p)
    with st.chat_message("assistant"): st.markdown(resp)
    st.session_state.history.append({"role": "assistant", "content": resp})
    
