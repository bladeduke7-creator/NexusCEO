import streamlit as st
import google.generativeai as genai

# Streamlit Secrets ထဲက Key ကို အတိအကျ ယူမယ်
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets ထဲမှာ Key မရှိသေးပါဘူး!")
    st.stop()

# Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("💼 Nexus CEO Agent")

if prompt := st.chat_input("Direct me, Boss..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # AI ကို စကားပြောခိုင်းမယ်
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"AI Connection Error: {str(e)}")
