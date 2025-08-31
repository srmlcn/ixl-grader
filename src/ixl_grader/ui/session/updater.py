import streamlit as st


def session_updater(func):
    """Decorator to update session state after function execution"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        st.rerun()
        return result

    return wrapper
