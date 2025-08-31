import pandas as pd
import streamlit as st

from ixl_grader.ui.session.grade import get_smart_score_threshold
from ixl_grader.ui.session.report import get_report


def render_sample_calculations():
    """Render sample grade calculations"""

    report = get_report()
    smart_score_threshold = get_smart_score_threshold()

    st.subheader("📊 Processing")

    # Add a preview of what the grading will look like
    df_preview = report.get_df()
    if "SmartScore" in df_preview.columns:
        st.markdown("**Sample Grade Calculations:**")
        sample_scores = df_preview["SmartScore"].dropna().head(3)
        for idx, score in sample_scores.items():
            if pd.notna(score):
                calculated_grade = min(100, (score / smart_score_threshold) * 100)
                st.text(f"SmartScore {score}% → Grade {calculated_grade:.1f}%")
