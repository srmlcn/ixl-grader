import tempfile
import streamlit as st

from ixl_grader.ui.session.updater import session_updater
from ixl_grader.ui.session.report import get_report


@session_updater
def handle_student_overrides_upload(uploaded_file):
    """Handle student overrides file upload and update session state"""
    
    try:
        # Save the uploaded file to disk
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()
            
            # Import overrides into the current report
            report = get_report()
            if report is not None:
                report.import_student_overrides(csv_path=tmp_file.name)
                st.session_state.has_student_overrides = True
            else:
                st.error("Please upload a report file first")
                return
                
    except Exception as e:
        st.error(f"❌ Error uploading student overrides file: {str(e)}")
        st.session_state.has_student_overrides = False
        return
    
    # Store the uploaded overrides file in session state
    st.session_state.uploaded_overrides_file = uploaded_file
    

def is_overrides_uploaded() -> bool:
    """Check if a student overrides file has been uploaded"""
    return getattr(st.session_state, 'uploaded_overrides_file', None) is not None


def get_uploaded_overrides_file():
    """Get the uploaded overrides file from session state"""
    return getattr(st.session_state, 'uploaded_overrides_file', None)


def has_student_overrides() -> bool:
    """Check if student overrides are loaded"""
    return getattr(st.session_state, 'has_student_overrides', False)


@session_updater
def set_has_student_overrides(value: bool):
    """Set whether student overrides are loaded"""
    st.session_state.has_student_overrides = value