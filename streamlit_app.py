import streamlit as st
from groq import Groq

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Study Buddy", page_icon="📚")

# ---------------- API SETUP ----------------
# Safely get API key from Streamlit secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ GROQ API key not found. Please add it in Streamlit Secrets.")
    st.stop()

# ---------------- HEADER ----------------
st.title("🎓 AI-Powered Study Buddy")
st.info("Developed by Arpan Singh")

# ---------------- SIDEBAR ----------------
menu = ["Home", "Explain Concept", "Summarize Notes", "Quiz Generator"]
choice = st.sidebar.selectbox("Select Feature", menu)

# ---------------- MODEL ----------------
MODEL_ID = "llama-3.1-8b-instant"

# ---------------- FUNCTION ----------------
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

# ---------------- HOME ----------------
if choice == "Home":
    st.subheader("Welcome to your Capstone Project!")
    st.write("This tool uses Groq + Llama 3 to help students understand complex topics.")

    st.markdown("""
    ### Features:
    - 💡 **Explain:** Simple analogies for hard topics  
    - 📝 **Summarize:** Long notes into bullet points  
    - 🧠 **Quiz:** Auto-generated MCQs  
    """)

# ---------------- EXPLAIN ----------------
elif choice == "Explain Concept":
    topic = st.text_input("Enter a complex topic:")

    if st.button("Simplify"):
        if topic.strip():
            prompt = f"Explain this like I'm 5 years old: {topic}"
            response = generate_response(prompt)
            st.success(response)
        else:
            st.warning("⚠️ Please enter a topic")

# ---------------- SUMMARIZE ----------------
elif choice == "Summarize Notes":
    text = st.text_area("Paste your notes here:", height=200)

    if st.button("Summarize"):
        if text.strip():
            prompt = f"Summarize this into key bullet points:\n{text}"
            response = generate_response(prompt)
            st.write(response)
        else:
            st.warning("⚠️ Please paste some notes")

# ---------------- QUIZ ----------------
elif choice == "Quiz Generator":
    context = st.text_area("Paste content for the quiz:")

    if st.button("Generate 3 Questions"):
        if context.strip():
            prompt = f"""
Create exactly 3 multiple choice questions based on the text below.

Rules:
- Each question must be clearly separated.
- Each option must be on a new line.
- Leave one blank line between questions.

Format:

Question 1:
<question>

A. option
B. option
C. option
D. option

Question 2:
...

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
            st.warning("⚠️ Please enter content")
