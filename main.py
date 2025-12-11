import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ...existing code...
# Streamlit UI + Groq client integration

st.set_page_config(page_title="Groq Chat UI", layout="wide")
st.title("Groq Chat - Streamlit Frontend")
st.markdown("Enter a query below and click Send. Responses and history are displayed on the right.")

# Ensure API key is available
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error("GROQ_API_KEY not found in environment. Please set it in your .env file.")
    st.stop()

# Initialize client once
client = Groq(api_key=API_KEY)

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []  # list of (user_prompt, assistant_reply)

# Layout: left column for input, right column for response & history
left_col, right_col = st.columns([1, 2])

with left_col:
    with st.form("query_form", clear_on_submit=False):
        query = st.text_area("Enter your query", height=160, placeholder="Ask a question for Groq model...")
        model = st.selectbox("Model", options=["openai/gpt-oss-120b"], help="Select model (default available option).")
        submitted = st.form_submit_button("Send")
        clear_history = st.form_submit_button("Clear history")

    if clear_history:
        st.session_state.history = []
        st.success("History cleared.")

# Handle submission
if submitted and query:
    with st.spinner("Sending request to Groq..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model=model,
            )
            reply = chat_completion.choices[0].message.content
        except Exception as e:
            reply = None
            st.error(f"Request failed: {e}")

    if reply is not None:
        # store and show result
        st.session_state.history.insert(0, (query, reply))

# Right column: show latest response and expandable history
with right_col:
    st.subheader("Latest response")
    if st.session_state.history:
        user_q, bot_reply = st.session_state.history[0]
        st.markdown("*You:*")
        st.write(user_q)
        st.markdown("*Groq:*")
        st.text_area("Response", value=bot_reply, height=200, key="latest_response", disabled=True)
    else:
        st.info("No responses yet. Submit a query from the left.")

    st.markdown("---")
    st.subheader("Conversation history")
    if st.session_state.history:
        for i, (u, b) in enumerate(st.session_state.history):
            with st.expander(f"Turn {len(st.session_state.history)-i}: {u[:60]}...", expanded=(i == 0)):
                st.markdown("*You:*")
                st.write(u)
                st.markdown("*Groq:*")
                st.write(b)
    else:
        st.write("History is empty.")

# Helpful note for Windows users
st.caption("Running locally on Windows: in the project folder run streamlit run main.py.")

# ...existing code...
