import streamlit as st


def initialize_session_state():
    """Initialize session state variables"""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "report" not in st.session_state:
        st.session_state.report = None
    if "is_gradable" not in st.session_state:
        st.session_state.is_gradable = False
    if "smart_score_threshold" not in st.session_state:
        st.session_state.smart_score_threshold = 80
    if "is_graded" not in st.session_state:
        st.session_state.is_graded = False
    if "uploaded_overrides_file" not in st.session_state:
        st.session_state.uploaded_overrides_file = None
    # Note: has_student_overrides removed as overrides are now persistent
