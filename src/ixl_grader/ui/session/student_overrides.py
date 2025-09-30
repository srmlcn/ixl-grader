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
            
            # Import overrides - create report if needed
            report = get_report()
            if report is None:
                # Create a temporary report just for override management
                from ixl_grader.core.report import Report
                from ixl_grader.ui.session.report import set_report
                report = Report()
                set_report(report)
            
            report.import_student_overrides(csv_path=tmp_file.name)
                
    except Exception as e:
        st.error(f"❌ Error uploading student overrides file: {str(e)}")
        return
    
    # Store the uploaded overrides file in session state for UI feedback
    st.session_state.uploaded_overrides_file = uploaded_file
    

def is_overrides_uploaded() -> bool:
    """Check if a student overrides file has been uploaded in this session"""
    return getattr(st.session_state, 'uploaded_overrides_file', None) is not None


def get_uploaded_overrides_file():
    """Get the uploaded overrides file from session state"""
    return getattr(st.session_state, 'uploaded_overrides_file', None)


def has_student_overrides() -> bool:
    """Check if student overrides are loaded (from persistent storage or session)"""
    # Check if we have a report with overrides loaded
    from ixl_grader.ui.session.report import get_report
    report = get_report()
    if report is not None and report.has_student_overrides():
        return True
    
    # Also check persistent storage directly
    from ixl_grader.core.persistence import get_local_storage
    local_storage = get_local_storage()
    return local_storage.has_student_overrides()


def clear_student_overrides():
    """Clear all student overrides from persistent storage"""
    # Create a report if none exists to access the overrides manager
    from ixl_grader.ui.session.report import get_report, set_report
    report = get_report()
    if report is None:
        from ixl_grader.core.report import Report
        report = Report()
        set_report(report)
    
    if report is not None:
        report.get_student_overrides().clear_all_overrides()
    
    # Also clear from session state
    if hasattr(st.session_state, 'uploaded_overrides_file'):
        st.session_state.uploaded_overrides_file = None