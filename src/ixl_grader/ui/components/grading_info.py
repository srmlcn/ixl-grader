import streamlit as st

from ixl_grader.ui.session.grade import get_smart_score_threshold


def render_grading_info():
    """Render grading information section"""

    smart_score_threshold = get_smart_score_threshold()

    st.markdown("### 📚 Grading Information")
    st.markdown(
        f"""
    **Current Settings:**
    - SmartScore Threshold: **{smart_score_threshold}%**
    - Grading Scale: Linear (0-{smart_score_threshold}% SmartScore → 0-100% Grade)
    
    **How Grading Works:**
    - Students who achieve the threshold get 100%
    - Students below threshold get proportional scores
    - Missing scores are marked as incomplete
    """
    )
