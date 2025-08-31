import streamlit as st

from ixl_grader.core.report import Report
from ixl_grader.ui.session.updater import session_updater


def get_report() -> Report:
    """Get the current Report object from session state"""
    return st.session_state.report


@session_updater
def set_report(report: Report):
    """Set the Report object in session state"""
    st.session_state.report = report
