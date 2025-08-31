import streamlit as st

from ixl_grader.ui.session.grade import (
    get_smart_score_threshold,
    set_smart_score_threshold,
)


def render_grading_params():
    """Render the grading parameters section"""

    smart_score_threshold = get_smart_score_threshold()

    st.header("🎯 Grading Parameters")

    subcol1, subcol2 = st.columns([1, 1])
    with subcol1:
        threshold = st.slider(
            "SmartScore Threshold (%)",
            min_value=0,
            max_value=100,
            value=smart_score_threshold,
            help="Students with SmartScore above this threshold will receive full points",
        )

        if threshold != smart_score_threshold:
            set_smart_score_threshold(threshold)

    with subcol2:
        st.metric("SmartScore Threshold", f"{threshold}%")
