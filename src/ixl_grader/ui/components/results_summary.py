import io
import os

import streamlit as st

from ixl_grader.ui.session.file_upload import get_uploaded_file
from ixl_grader.ui.session.report import get_report


def render_results_summary():
    """Render the results summary, statistics, and download button"""

    st.header("📊 Results Summary")
    st.markdown("View grading statistics and download the graded results.")

    report = get_report()
    graded_df = report.get_df()

    # Show summary statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", len(graded_df))

    with col2:
        graded_students = graded_df["Score"].notna().sum()
        st.metric("Graded Students", graded_students)

    with col3:
        if graded_students > 0:
            avg_score = graded_df["Score"].mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
        else:
            st.metric("Average Score", "N/A")

    with col4:
        if graded_students > 0:
            passing_students = (graded_df["Score"] >= 70).sum()
            pass_rate = (passing_students / graded_students) * 100
            st.metric("Pass Rate (≥70%)", f"{pass_rate:.1f}%")
        else:
            st.metric("Pass Rate", "N/A")

    # Show graded data preview (top 5, limited columns)
    st.subheader("📊 Graded Results Preview")
    preview_cols = ["Student ID", "Last name", "First name", "SmartScore", "Score"]
    preview_existing = [c for c in preview_cols if c in graded_df.columns]
    st.dataframe(graded_df[preview_existing].head(5), use_container_width=True)

    # Prepare CSV for download
    buffer = io.StringIO()
    report.export_report(buffer)

    uploaded_file = get_uploaded_file()
    file_name, extension = os.path.splitext(uploaded_file.name)
    download_file_name = f"{file_name}-Graded{extension}"

    # Download button
    st.download_button(
        label="📥 Download Graded Results",
        data=buffer.getvalue(),
        file_name=download_file_name,
        mime="text/csv",
        type="primary",
        use_container_width=True,
    )
