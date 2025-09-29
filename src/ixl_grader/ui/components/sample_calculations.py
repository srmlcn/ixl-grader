import pandas as pd
import streamlit as st

from ixl_grader.ui.session.grade import get_smart_score_threshold
from ixl_grader.ui.session.report import get_report
from ixl_grader.ui.session.student_overrides import has_student_overrides


def render_sample_calculations():
    """Render sample grade calculations"""

    report = get_report()
    smart_score_threshold = get_smart_score_threshold()

    st.subheader("📊 Processing")

    # Add a preview of what the grading will look like
    df_preview = report.get_df()
    if "SmartScore" in df_preview.columns:
        st.markdown("**Sample Grade Calculations:**")
        sample_scores = df_preview[["Student ID", "SmartScore"]].dropna(subset=["SmartScore"]).head(3)
        
        for idx, row in sample_scores.iterrows():
            student_id = row["Student ID"]
            score = row["SmartScore"]
            
            if pd.notna(score):
                # Get any overrides for this student
                override_threshold, minimum_grade = report.get_student_override(student_id)
                
                # Calculate grade using override logic
                threshold = override_threshold if override_threshold is not None else smart_score_threshold
                calculated_grade = min(100, (score / threshold) * 100)
                
                # Apply minimum grade override
                final_grade = calculated_grade
                if minimum_grade is not None and calculated_grade < minimum_grade:
                    final_grade = minimum_grade
                
                # Display calculation with override info
                override_info = ""
                if override_threshold is not None or minimum_grade is not None:
                    details = []
                    if override_threshold is not None:
                        details.append(f"threshold: {override_threshold}%")
                    if minimum_grade is not None:
                        details.append(f"min: {minimum_grade}%")
                    override_info = f" (override: {', '.join(details)})"
                
                if final_grade != calculated_grade:
                    st.text(f"Student {student_id}: SmartScore {score}% → {calculated_grade:.1f}% → {final_grade:.1f}%{override_info}")
                else:
                    st.text(f"Student {student_id}: SmartScore {score}% → {final_grade:.1f}%{override_info}")
        
        # Show override summary if any are loaded
        if has_student_overrides():
            overrides_df = report.get_student_overrides().get_all_overrides()
            if len(overrides_df) > 0:
                st.info(f"📋 {len(overrides_df)} student override(s) loaded")
