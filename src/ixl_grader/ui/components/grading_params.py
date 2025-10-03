import streamlit as st

from ixl_grader.ui.session.grade import (
    get_smart_score_threshold,
    set_smart_score_threshold,
)
from ixl_grader.ui.session.student_overrides import (
    handle_student_overrides_upload,
    get_uploaded_overrides_file,
    has_student_overrides,
    clear_student_overrides,
)
from ixl_grader.ui.session.report import get_report


def render_grading_params():
    """Render the grading parameters section"""

    smart_score_threshold = get_smart_score_threshold()

    st.header("🎯 Grading Parameters")

    # Global threshold settings
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

    # Student overrides section (hidden behind a dropdown)
    st.markdown("---")
    render_student_overrides_section()


def render_student_overrides_section():
    """Render the student overrides section within grading parameters.
    - Hidden behind a dropdown (expander)
    - Upload flow via a single 'Upload' button that reveals the file picker only when clicked
    - Full description shown in a closable help panel triggered by a question-mark button
    """

    # Initialize UI state
    if "overrides_help_open" not in st.session_state:
        st.session_state["overrides_help_open"] = False
    if "show_overrides_uploader" not in st.session_state:
        st.session_state["show_overrides_uploader"] = False

    with st.expander("👥 Student Overrides (504/IEP Accommodations)", expanded=False):
        st.caption(
            "Optional: Upload CSV or add individual overrides for students with special accommodations"
        )

        # Row with Upload button (left) and Help button (right)
        col_upl, col_help = st.columns([1, 1])
        with col_upl:
            section = st.container(horizontal_alignment="left")
            with section:
                if st.button("📁 Upload", key="overrides_upload_btn"):
                    st.session_state["show_overrides_uploader"] = True
        with col_help:
            section = st.container(horizontal_alignment="right")
            with section:
                if st.button("❓ Info", key="overrides_help_btn"):
                    # Toggle the help panel open/closed
                    st.session_state["overrides_help_open"] = not st.session_state.get(
                        "overrides_help_open", False
                    )

        # Closable help panel (modal-style fallback)
        if st.session_state.get("overrides_help_open", False):
            with st.container(border=True):
                st.subheader("About Student Overrides CSV")
                st.markdown(
                    """
                    Use a CSV to set per-student accommodations. Your file should contain these exact column headers:
                    
                    - Student ID: Student identifier (e.g., "12345" or "ID12345")
                    - Smart Score Threshold: Custom SmartScore threshold for this student (0–100, optional)
                    - Minimum Grade: Minimum grade for this student (0–100, optional)
                    
                    Example:
                    ```csv
                    Student ID,Smart Score Threshold,Minimum Grade
                    12345,70,60
                    67890,,50
                    11111,85,
                    ```
                    Notes:
                    - Leave cells empty if no override is needed for that student/field
                    - Student IDs are automatically cleaned (removes the "ID" prefix)
                    - 🔄 Persistence: Overrides are saved to local storage and persist across browser sessions on this computer
                    """
                )

        # Reveal the file uploader only after clicking Upload
        if st.session_state.get("show_overrides_uploader", False):
            uploaded_overrides_file = st.file_uploader(
                "Choose student overrides CSV file",
                type=["csv"],
                help="CSV file with columns: Student ID, Smart Score Threshold, Minimum Grade",
                key="overrides_uploader",
            )

            prev_uploaded_overrides_file = get_uploaded_overrides_file()
            if (
                uploaded_overrides_file is not None
                and uploaded_overrides_file != prev_uploaded_overrides_file
            ):
                handle_student_overrides_upload(uploaded_file=uploaded_overrides_file)
                # Hide uploader after successful selection to keep UI clean
                st.session_state["show_overrides_uploader"] = False
                st.rerun()
            else:
                # Option to cancel/close the uploader without selecting a file
                if st.button("Cancel", key="cancel_overrides_upload"):
                    st.session_state["show_overrides_uploader"] = False
                    st.rerun()

        # Individual override editor inside the dropdown
        with st.expander("✏️ Add/Edit Individual Override", expanded=False):
            render_individual_override_form()

        # Show status and loaded overrides
        render_overrides_status()


def render_individual_override_form():
    """Render form to add/edit individual student overrides (simplified)"""

    with st.form("student_override_form"):
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            student_id = st.text_input("Student ID", help="Enter the student ID")

        with col2:
            custom_threshold = st.number_input(
                "Custom Smart Score Threshold (%)",
                min_value=0,
                max_value=100,
                value=None,
                help="Leave empty to use global threshold",
            )

        with col3:
            minimum_grade = st.number_input(
                "Minimum Grade (%)",
                min_value=0,
                max_value=100,
                value=None,
                help="Leave empty for no minimum grade override",
            )

        submitted = st.form_submit_button("Set Override")

        if submitted and student_id:
            # Create a report instance if none exists (for overrides management)
            from ixl_grader.core.report import Report

            report = get_report()
            if report is None:
                # Create a temporary report just for override management
                from ixl_grader.ui.session.report import set_report

                report = Report()
                set_report(report)

            # Convert None values appropriately
            threshold_val = custom_threshold if custom_threshold != 0 else None
            minimum_val = minimum_grade if minimum_grade != 0 else None

            report.set_student_override(
                student_id=student_id,
                smart_score_threshold=threshold_val,
                minimum_grade=minimum_val,
            )

            st.success(f"✅ Override set for student {student_id}")
            st.rerun()
        elif submitted:
            st.error("Please enter a Student ID")


def render_overrides_status():
    """Show status of loaded student overrides"""

    if has_student_overrides():
        # Status row with message (left) and clear button (right)
        # col_left, col_right = st.columns([1, 1])
        with st.container(horizontal=True):
            # with col_left:
            with st.container(width="stretch"):
                st.success("✅ Student overrides loaded")
            # with col_right:
            with st.container(horizontal_alignment="right"):
                if st.button(
                    "🗑️ Clear All",
                    help="Clear all persisted student overrides",
                    key="clear_overrides",
                ):
                    clear_student_overrides()
                    st.rerun()

        # Show preview of loaded overrides directly below the status, hidden behind a dropdown
        # Try to read from the current report; fall back to local storage if needed
        overrides_df = None
        report = get_report()
        if report is not None:
            overrides_df = report.get_student_overrides().get_all_overrides()
        else:
            from ixl_grader.core.persistence import get_local_storage

            _ls_df = get_local_storage().load_student_overrides()
            overrides_df = _ls_df if (_ls_df is not None and not _ls_df.empty) else None

        if overrides_df is not None and len(overrides_df) > 0:
            with st.expander("📋 View loaded overrides", expanded=False):
                st.dataframe(overrides_df, use_container_width=True)
                st.caption(
                    f"💾 Total overrides persisted: {len(overrides_df)} (saved to local storage)"
                )
    else:
        # Check if we have persistent overrides but no report loaded
        from ixl_grader.core.persistence import get_local_storage

        local_storage = get_local_storage()
        if local_storage.has_student_overrides():
            st.info(
                "💾 Student overrides found in local storage - they will be loaded automatically"
            )
        else:
            st.info(
                "ℹ️ No student overrides configured. This is optional - you can grade assignments without overrides."
            )
