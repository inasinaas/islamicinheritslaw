import streamlit as st
from google import genai
from docx import Document

# Initialize Gemini client with secrets
try:
    F6PJf6z1DDrE = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # Fallback for local testing
    F6PJf6z1DDrE = genai.Client(api_key="AIzaSyBnmvzruiBZrCA8aBSA8s55TtiZCr59Gfk")

# Read knowledge base from docx
@st.cache_resource
def load_knowledge_base():
    document = Document("Islamic Law of Inheritance.docx")
    kb = ""
    for para in document.paragraphs:
        kb += para.text + "\n"
    return kb

kb = load_knowledge_base()

# System prompt
prompt = f"""You are MISHKATH HELP executive. Your job is to provide answers to the customers. You should answer them in polite.
If there is any question out of the KB say you did not have that info. Only refer the KB and provide the response.
Knowledge Base:
{kb}"""

# UI CODE - EDIT BELOW THIS LINE ============================================

st.title("MISHKATH HELP")
st.caption("Islamic Inheritance Law Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat session
if "chat" not in st.session_state:
    try:
        st.session_state.chat = F6PJf6z1DDrE.chats.create(
            model="gemini-1.5-flash",  # Changed to stable model
            config={"system_instruction": prompt}
        )
    except Exception as e:
        st.error(f"Error initializing chat: {e}")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                bot_response = response.text
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"Error: {e}")

# UI CODE - EDIT ABOVE THIS LINE ============================================