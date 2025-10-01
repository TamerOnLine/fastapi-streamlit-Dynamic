from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import streamlit as st

from api_client import get_api_base, post_generate_form

def _request_reset():
    st.session_state["_reset_requested"] = True

def render_generate_actions(outputs_dir: Path) -> None:
    st.header("Generate & Download")

    colg1, colg2, colg3 = st.columns(3)

    with colg1:
        if st.button("Generate PDF", type="primary"):
            try:
                data = {
                    "name": st.session_state.name,
                    "location": st.session_state.location,
                    "phone": st.session_state.phone,
                    "email": st.session_state.email,
                    "github": st.session_state.github,
                    "linkedin": st.session_state.linkedin,
                    "birthdate": st.session_state.birthdate,
                    "projects_text": st.session_state.projects_text,
                    "education_text": st.session_state.education_text,
                    "sections_left_text": st.session_state.sections_left_text,
                    "sections_right_text": st.session_state.sections_right_text,
                    "skills_text": st.session_state.skills_text,
                    "languages_text": st.session_state.languages_text,
                    "rtl_mode": "true" if st.session_state.rtl_mode else "false",
                }

                photo_tuple: Optional[Tuple[bytes, str, str]] = None
                if st.session_state.photo_bytes:
                    photo_tuple = (
                        st.session_state.photo_bytes,
                        st.session_state.photo_mime or "image/png",
                        st.session_state.photo_name or "photo.png",
                    )

                pdf_bytes = post_generate_form(
                    api_base=(st.session_state.api_base or get_api_base()),
                    data=data,
                    photo_tuple=photo_tuple,
                )
                st.session_state.pdf_bytes = pdf_bytes
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                st.session_state.pdf_name = f"resume-{ts}.pdf"
                st.success("PDF generated.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    with colg2:
        st.button("Clear form", on_click=_request_reset)

    with colg3:
        if st.session_state.pdf_bytes:
            out_path = outputs_dir / st.session_state.pdf_name
            try:
                out_path.write_bytes(st.session_state.pdf_bytes)
            except Exception:
                pass
            st.download_button(
                "Download PDF",
                data=st.session_state.pdf_bytes,
                file_name=st.session_state.pdf_name,
                mime="application/pdf",
            )
        else:
            st.caption("The download button appears after generating a PDF.")
