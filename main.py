import streamlit as st
import google.generativeai as genai

# Secrets ထဲက Key ကို ယူမယ်
API_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

st.title("💼 Nexus CEO Agent")

# Model နာမည်ကို models/ မပါဘဲ ရေးပါ
model = genai.GenerativeModel("gemini-1.5-flash")

if prompt := st.chat_input("Direct me, Boss..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
        
