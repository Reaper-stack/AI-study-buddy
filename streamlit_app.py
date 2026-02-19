import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load env variables (for local use)
load_dotenv()

# Get API key (Streamlit Cloud OR local)
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ API key not found. Add it in secrets or .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Page config
st.set_page_config(page_title="AI Study Buddy", page_icon="📚")

# Header
st.title("🎓 AI-Powered Study Buddy")
st.info("Developed by Arpan Singh")

# Sidebar
menu = ["Home", "Explain Concept", "Summarize Notes", "Quiz Generator"]
choice = st.sidebar.selectbox("Select Feature", menu)

# Groq Model (fast + free)
MODEL_ID = "llama-3.1-8b-instant"

# Function to generate response
def generate_response(prompt):
    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Home
if choice == "Home":
    st.subheader("Welcome to your Capstone Project!")
    st.write("This tool uses Groq + Llama 3 to help students understand complex topics.")
    st.markdown("""
    ### Features:
    - 💡 **Explain:** Simple analogies for hard topics.
    - 📝 **Summarize:** Long notes into bullet points.
    - 🧠 **Quiz:** Auto-generated MCQs.
    """)

# Explain Concept
elif choice == "Explain Concept":
    topic = st.text_input("Enter a complex topic:")
    if st.button("Simplify"):
        if topic.strip():
            with st.spinner("Thinking..."):
                prompt = f"Explain this like I'm 5 years old: {topic}"
                response = generate_response(prompt)
                st.success(response)
        else:
            st.warning("⚠️ Please enter a topic.")

# Summarize Notes
elif choice == "Summarize Notes":
    text = st.text_area("Paste your notes here:", height=200)
    if st.button("Summarize"):
        if text.strip():
            with st.spinner("Summarizing..."):
                prompt = f"Summarize this into key bullet points:\n{text}"
                response = generate_response(prompt)
                st.write(response)
        else:
            st.warning("⚠️ Please enter some text.")

# Quiz Generator
elif choice == "Quiz Generator":
    context = st.text_area("Paste content for the quiz:")
    if st.button("Generate 3 Questions"):
        if context.strip():
            with st.spinner("Generating quiz..."):
                prompt = f"""
Create exactly 3 multiple choice questions based on the text below.

Rules:
- Each question must be clearly separated.
- Each option must be on a new line.
- Leave one blank line between questions.

Format strictly like this:

Question 1:
<question text>

A. option
B. option
C. option
D. option

Question 2:
...

After all questions, write:

Answers:
1. <correct option>
2. <correct option>
3. <correct option>

Text:
{context}
"""
                response = generate_response(prompt)
                st.write(response)
        else:
            st.warning("⚠️ Please enter content.")
