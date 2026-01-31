import streamlit as st
import google.generativeai as genai
import requests
import threading
import time
import os
import re

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8487111144:AAEfZUn0K2rShXnMrYD9PtadNcaxCdldgyw"
TELEGRAM_CHAT_ID = "8519715726"
SCOUT_INTERVAL_SECONDS = 3600 

# --- GEMINI SETUP ---
# Replit Secrets ထဲမှာ GEMINI_API_KEY ကို ထည့်ထားဖို့ လိုပါတယ်
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing GEMINI_API_KEY in Secrets!")

def clean_text(text):
    """စာသားထဲက မလိုလားအပ်တဲ့ Markdown အစုတ်အပဲ့တွေကို သန့်စင်ပေးတဲ့ function"""
    # ဒီနေရာမှာ ညီလေး မကြိုက်တဲ့ symbol တွေကို လိုသလို ဖျောက်လို့ရတယ်
    return text.replace("###", "").replace("***", "")

# --- CORE AI LOGIC ---
def generate_strategy(prompt):
    try:
        # Search Tool ကို နေရာမှန် ပြန်ထည့်ပေးထားတယ်
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash", # Flash က ပိုမြန်ပြီး Limit ပိုများတယ်
            tools=[{"google_search_retrieval": {}}] 
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- TELEGRAM UTILS ---
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# --- BACKGROUND THREADS ---
def scout_loop():
    while True:
        try:
            query = "Current high-growth business trends 2026. Provide a SWOT and ROI analysis."
            report = generate_strategy(query)
            send_telegram(f"🚀 *CEO SCOUT ALERT*\n\n{report[:3500]}")
        except: pass
        time.sleep(SCOUT_INTERVAL_SECONDS)

def telegram_bridge():
    last_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_id+1}"
            res = requests.get(url).json()
            for up in res.get("result", []):
                last_id = up["update_id"]
                msg = up["message"]["text"]
                ans = generate_strategy(f"Telegram Command: {msg}")
                send_telegram(f"🎯 *Strategy Response*\n\n{ans}")
        except: pass
        time.sleep(5)

if "init" not in st.session_state:
    threading.Thread(target=scout_loop, daemon=True).start()
    threading.Thread(target=telegram_bridge, daemon=True).start()
    st.session_state.init = True

# --- UI DESIGN ---
st.set_page_config(page_title="Nexus CEO Console", layout="wide")
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
      
