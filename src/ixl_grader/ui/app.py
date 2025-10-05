import streamlit as st

from ixl_grader.ui.components import (
    render_file_uploader,
    render_file_viewer,
    render_grade_button,
    render_grading_params,
    render_results_summary,
    render_footer,
)
from ixl_grader.ui.session import initialize_session_state
from ixl_grader.ui.session.file_upload import is_uploaded
from ixl_grader.ui.session.grade import is_graded


def render():
    """Render the main application"""

    st.set_page_config(
        page_title="IXL Assignment Grader", page_icon="📊"
    )

    st.title("📊 IXL Assignment Grader")
    st.markdown("Upload your IXL assignments CSV file and set grading parameters.")

    # Initialize session state
    initialize_session_state()

    # File upload section
    render_file_uploader()

    # Show file details and preview if file is uploaded
    if is_uploaded():
        st.markdown("---")
        render_file_viewer()

    # Grading parameters section (now includes student overrides)
    st.markdown("---")
    render_grading_params()

    # Grading button
    st.markdown("---")
    render_grade_button()

    if is_graded():
        st.markdown("---")
        render_results_summary()

    render_footer()
