import streamlit as st


def render():
    """Render the main application"""

    st.set_page_config(
        page_title="IXL Assignment Grader", page_icon="📊", layout="wide"
    )

    st.title("📊 IXL Assignment Grader")
    st.markdown("Upload your IXL assignments CSV file and set grading parameters.")

    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Upload new file section
        pass

    with col2:
        # Grading section
        pass
