import streamlit as st
import google.generativeai as genai

# --- API SETUP ---
# Streamlit Secrets ထဲက Key ကို ယူမယ်
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing API Key in Streamlit Secrets!")

# --- AI LOGIC ---
def generate_strategy(prompt):
    try:
        # ဒီနေရာမှာ 'gemini-1.5-flash' လို့ပဲ ရေးပေးရမှာပါ (models/ မပါဘဲ စမ်းကြည့်ပါ)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Error တက်ရင် ဘာလို့တက်လဲဆိုတာ သေချာပြအောင် လုပ်ထားတယ်
        return f"AI Error: {str(e)}"

# --- SIMPLE UI ---
st.title("💼 Nexus CEO Agent")

if prompt := st.chat_input("Direct me, Boss..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = generate_strategy(prompt)
        st.markdown(response)
        
