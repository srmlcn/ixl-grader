import streamlit as st

from ixl_grader.ui.session.student_overrides import (
    handle_student_overrides_upload,
    get_uploaded_overrides_file,
    has_student_overrides,
)
from ixl_grader.ui.session.file_upload import is_uploaded
from ixl_grader.ui.session.report import get_report


def render_student_overrides_uploader():
    """Render the student overrides file uploader component"""

    if not is_uploaded():
        st.info("📋 Upload a report file first to manage student overrides")
        return

    st.header("🎯 Student Overrides")
    st.markdown(
        "Upload a CSV file with student-specific grade minimums and smart score thresholds for 504/IEP accommodations"
    )

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

    # Show status and sample format
    if has_student_overrides():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success("✅ Student overrides loaded (persisted locally)")
        with col2:
            if st.button(
                "🗑️ Clear All",
                help="Clear all persisted student overrides",
                key="clear_overrides",
            ):
                from ixl_grader.ui.session.student_overrides import (
                    clear_student_overrides,
                )

                clear_student_overrides()
                st.rerun()

        # Show preview of loaded overrides
        report = get_report()
        if report is not None:
            overrides_df = report.get_student_overrides().get_all_overrides()
            if len(overrides_df) > 0:
                st.subheader("📋 Loaded Overrides Preview")
                st.dataframe(overrides_df.head(), use_container_width=True)
                st.info(
                    f"💾 Total overrides persisted: {len(overrides_df)} (saved to local storage)"
                )
    else:
        # Check if we have persistent overrides but no report loaded
        from ixl_grader.core.persistence import get_local_storage

        local_storage = get_local_storage()
        if local_storage.has_student_overrides():
            st.info(
                "💾 Student overrides found in local storage - they will be loaded automatically when you upload a report"
            )

    # Show expected CSV format
    with st.expander("📄 Expected CSV Format"):
        st.markdown(
            """
        Your CSV file should contain these exact column headers:
        - **Student ID**: Student identifier (e.g., "12345" or "ID12345")
        - **Smart Score Threshold**: Custom threshold for this student (0-100, optional)
        - **Minimum Grade**: Minimum grade for this student (0-100, optional)
        
        Example:
        ```
        Student ID,Smart Score Threshold,Minimum Grade
        12345,70,60
        67890,,50
        11111,85,
        ```
        
        - Leave cells empty if no override is needed for that student/field
        - Student IDs will be automatically cleaned (removes "ID" prefix)
        - **🔄 Persistence**: All overrides are automatically saved to local storage 
          and will persist across browser sessions on this computer
        """
        )

    # Show persistence info
    st.markdown("---")
    st.markdown(
        "**💾 Local Storage**: Student overrides are automatically saved to your computer and will persist even after closing the browser tab."
    )


def render_individual_student_override():
    """Render form to add/edit individual student overrides"""

    if not is_uploaded():
        return

    st.subheader("✏️ Add/Edit Individual Override")

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
            report = get_report()
            if report is not None:
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
            else:
                st.error("No report loaded")
        elif submitted:
            st.error("Please enter a Student ID")
