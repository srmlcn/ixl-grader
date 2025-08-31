import streamlit as st

from ixl_grader.ui.session.report import get_report


def render_file_viewer():
    """Render file details and data preview"""

    # Show file details
    st.success("✅ File uploaded")

    report = get_report()
    if report is None:
        st.error("Error: No report found in session state.")

    # Preview the data
    df_preview = report.get_df()

    st.subheader("📋 Data Preview")
    st.dataframe(df_preview.head(), use_container_width=True)
    st.info(
        f"Dataset contains {len(df_preview)} rows and {len(df_preview.columns)} columns"
    )
