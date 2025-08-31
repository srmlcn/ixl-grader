import streamlit as st

from ixl_grader.ui.session.updater import session_updater


def is_graded() -> bool:
    """Check if assignments have been graded"""
    return st.session_state.is_graded


@session_updater
def set_is_graded(value: bool):
    """Set the graded status of assignments"""
    st.session_state.is_graded = value


def is_gradable() -> bool:
    """Check if the uploaded file is gradable"""
    return st.session_state.is_gradable


@session_updater
def set_is_gradable(value: bool):
    """Set the gradable status of the uploaded file"""
    st.session_state.is_gradable = value


def get_smart_score_threshold() -> int:
    """Get the current SmartScore threshold"""
    return st.session_state.smart_score_threshold


@session_updater
def set_smart_score_threshold(value: int):
    """Set the SmartScore threshold"""
    st.session_state.smart_score_threshold = value
