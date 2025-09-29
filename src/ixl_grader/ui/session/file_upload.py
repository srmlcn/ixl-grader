import tempfile

import streamlit as st

from ixl_grader.core.report import Report
from ixl_grader.ui.session.updater import session_updater


@session_updater
def handle_file_upload(uploaded_file):
    """Handle file upload and update session state"""

    try:
        # Save the uploaded file to disk
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()

            report = Report()
            report.import_report(csv_path=tmp_file.name)
            st.session_state.report = report
            st.session_state.is_gradable = True

    except Exception as e:
        st.error(f"❌ Error uploading file: {str(e)}")
        st.session_state.report = None

    # Store the uploaded file in session state
    st.session_state.uploaded_file = uploaded_file

    # Reset graded status when a new file is uploaded
    st.session_state.is_graded = False
    
    # Reset student overrides when a new report is uploaded
    st.session_state.uploaded_overrides_file = None
    st.session_state.has_student_overrides = False


def is_uploaded() -> bool:
    """Check if a file has been uploaded"""
    return st.session_state.uploaded_file is not None


def get_uploaded_file():
    """Get the uploaded file from session state"""
    return st.session_state.uploaded_file
