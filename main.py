import os
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


def get_client(api_key: Optional[str]) -> Groq:
    """
    Build a Groq client once Streamlit has validated that an API key exists.
    """
    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY. Set it in your .env file or environment."
        )
    return Groq(api_key=api_key)


def get_completion(client: Groq, prompt: str) -> str:
    """
    Send the user's prompt to Groq and return the model response text.
    """
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-120b",
    )
    return completion.choices[0].message.content


def main() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="Groq Chat Playground",
        layout="centered",
    )

    st.title("Groq Chat Playground")
    st.caption("Ask a question and view the response from `openai/gpt-oss-120b`.")

    with st.container():
        st.markdown("### Enter your query")
        user_prompt = st.text_area(
            "Prompt",
            placeholder="Type your query here...",
            height=200,
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            submit = st.button("Generate Response", type="primary")
        with col2:
            clear = st.button("Clear Input")

    if clear:
        st.experimental_rerun()

    if submit:
        if not user_prompt.strip():
            st.warning("Please enter a prompt before requesting a response.")
            return

        api_key = os.getenv("GROQ_API_KEY")
        try:
            client = get_client(api_key)
        except ValueError as exc:
            st.error(str(exc))
            return

        with st.spinner("Contacting Groq..."):
            try:
                response_text = get_completion(client, user_prompt.strip())
            except Exception as exc:  # pragma: no cover - network failure
                st.error(f"Request failed: {exc}")
                return

        st.markdown("### Response")
        st.write(response_text)


if __name__ == "__main__":
    main()