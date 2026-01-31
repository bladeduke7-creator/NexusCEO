import streamlit as st
import google.generativeai as genai

# --- API SETUP ---
# Streamlit Secrets ထဲက Key ကို အတိအကျ ယူမယ်
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    # ဤနေရာတွင် version သတ်မှတ်ချက်ကို ရှင်းလင်းထားပါသည်
    genai.configure(api_key=API_KEY)
else:
    st.error("Secrets ထဲမှာ Key မရှိသေးပါဘူး!")

# --- UI DESIGN ---
st.set_page_config(page_title="Nexus CEO Agent", layout="centered")
st.title("💼 Nexus CEO Agent")

# Model ကို ရိုးရိုးရှင်းရှင်းပဲ ခေါ်ပါမယ်
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Direct me, Boss..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI ကို အဖြေတောင်းမယ်
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
