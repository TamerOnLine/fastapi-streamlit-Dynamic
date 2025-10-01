from __future__ import annotations
import streamlit as st

def render_blocks() -> None:
    st.header("Free-text Blocks")

    st.text_area(
        "Projects (each project as a block: first line = title, following lines = bullets, optional link line, then a blank line)",
        key="projects_text",
        height=200,
        placeholder="My App\n- bullet 1\n- bullet 2\nhttps://github.com/...\n\nProject 2\nDetails...",
    )
    st.text_area(
        "Education (blocks separated by a blank line)",
        key="education_text",
        height=160,
    )
    st.text_area(
        "Left sections (format: [Title] and lines starting with -)",
        key="sections_left_text",
        height=160,
    )
    st.text_area(
        "Right sections (format: [Title] and lines starting with -)",
        key="sections_right_text",
        height=160,
    )
