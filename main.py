import streamlit as st
import google.generativeai as genai

# --- API SETUP ---
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    # ညီလေးတွေ့လာတဲ့ version ပြဿနာ မတက်အောင် config ကို အရှင်းဆုံးလုပ်ထားတယ်
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing API Key in Secrets!")

# --- AI MODEL ---
# ညီလေး ရှာတွေ့တဲ့ gemini-2.0-flash က လက်ရှိမှာ စမ်းသပ်ဆဲမို့လို့
# အသေချာဆုံးဖြစ်တဲ့ 'gemini-1.5-flash' ကိုပဲ models/ မပါဘဲ သုံးပါမယ်
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("💼 Nexus CEO Agent")

if prompt := st.chat_input("Direct me, Boss..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # AI ကို အဖြေတောင်းမယ်
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI Connection Error: {str(e)}")
