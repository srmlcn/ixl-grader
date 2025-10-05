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

    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # File upload section
        render_file_uploader()

        # Show file details and preview if file is uploaded
        if is_uploaded():
            render_file_viewer()

    with col2:
        # Grading parameters section (now includes student overrides)
        render_grading_params()

        # Removed extra informational sections for a cleaner UI
        render_grade_button()

        if is_graded():
            render_results_summary()

    render_footer()
