import streamlit as st

from ixl_grader.ui.session.file_upload import is_uploaded
from ixl_grader.ui.session.grade import (
    get_smart_score_threshold,
    is_gradable,
    is_graded,
    set_is_graded,
)
from ixl_grader.ui.session.report import get_report


def render_grade_button() -> None:
    st.header("🚀 Grade Assignments")
    st.markdown("Review your settings and click the button to grade all assignments.")
    
    button_placeholder = st.empty()

    if is_uploaded() and is_gradable() and not is_graded():
        with button_placeholder.container():
            should_grade = st.button(
                "🚀 Grade Assignments",
                type="primary",
                use_container_width=True,
                key="grade_button",
            )

            if should_grade:
                report = get_report()
                smart_score_threshold = get_smart_score_threshold()

                report.grade(smart_score_threshold=smart_score_threshold)

                set_is_graded(True)

    elif is_uploaded() and is_graded():
        with button_placeholder.container():
            st.info(
                "✅ Assignments have been graded! Upload a new file to grade more assignments."
            )
