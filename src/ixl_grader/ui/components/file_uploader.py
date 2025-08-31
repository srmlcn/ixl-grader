import streamlit as st

from ixl_grader.ui.session.file_upload import get_uploaded_file, handle_file_upload


def render_file_uploader():
    """Render the file uploader component"""
    st.header("📁 Upload File")
    uploaded_file = st.file_uploader(
        "Choose your IXL assignments CSV file",
        type=["csv"],
        help="Upload the CSV file exported from IXL containing student assignments",
    )

    prev_uploaded_file = get_uploaded_file()
    if uploaded_file is not None and uploaded_file != prev_uploaded_file:
        handle_file_upload(uploaded_file=uploaded_file)
