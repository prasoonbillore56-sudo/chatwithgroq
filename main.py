import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def init_client() -> Groq | None:
    """Instantiate the Groq client if the API key is available."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Missing GROQ_API_KEY. Add it to your environment or .env file.")
        return None
    return Groq(api_key=api_key)


def main() -> None:
    st.set_page_config(page_title="Groq Chat UI", layout="centered", page_icon="💬")
    st.title("Groq Chat Playground")
    st.caption("Ask anything and get a response powered by openai/gpt-oss-20b.")

    prompt = st.text_area(
        "Your prompt",
        placeholder="Type your question or instructions here...",
        height=150,
    )

    col_run, col_clear = st.columns([1, 1], gap="large")
    run_clicked = col_run.button("Generate Response", type="primary", use_container_width=True)
    clear_clicked = col_clear.button("Clear", use_container_width=True)

    if clear_clicked:
        st.experimental_rerun()

    if not run_clicked:
        return

    if not prompt.strip():
        st.warning("Please enter a prompt before requesting a response.")
        return

    client = init_client()
    if client is None:
        return

    with st.spinner("Generating response..."):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-20b",
        )

    message = chat_completion.choices[0].message.content.strip()
    st.subheader("Response")
    st.write(message)


if _name_ == "_main_":
    main()
