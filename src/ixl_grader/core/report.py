import math
from os import PathLike
from typing import TextIO, Optional

import pandas as pd

from .student_overrides import StudentOverrides


class Report:
    def __init__(self):
        self._csv_path: str | None = None
        self._report: pd.DataFrame | None = None
        self._student_overrides: StudentOverrides = StudentOverrides()

    def _fix_csv(self) -> None:
        assert self._csv_path is not None, "CSV path must be set before fixing the CSV."

        with open(self._csv_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Some CSVs from IXL have more columns than expected, likely due to commas in names
        lines = _fix_column_counts(lines)

        with open(self._csv_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

    def _load_report(self) -> pd.DataFrame:
        assert (
            self._csv_path is not None
        ), "CSV path must be set before loading the report."
        return pd.read_csv(self._csv_path)

    def _clean_report(self) -> None:
        assert self._report is not None, "Report must be loaded before cleaning."

        self._report = _clean_ids(self._report)

    def import_report(self, csv_path: str) -> None:
        self._csv_path = csv_path
        self._fix_csv()
        self._report = self._load_report()
        self._clean_report()

    def get_df(self) -> pd.DataFrame:
        assert (
            self._report is not None
        ), "Report must be loaded before accessing DataFrame."
        return self._report.copy()

    def grade(self, smart_score_threshold: int) -> None:
        assert self._report is not None, "Report must be loaded before grading."

        def assign_grade(row):
            smart_score = row["SmartScore"]
            student_id = row["Student ID"]
            
            if smart_score is None or pd.isna(smart_score):
                return math.nan

            # Get student-specific overrides
            override_threshold, minimum_grade = self._student_overrides.get_override(student_id)
            
            # Use override threshold if available, otherwise use global threshold
            threshold = override_threshold if override_threshold is not None else smart_score_threshold
            
            # Calculate grade based on threshold
            calculated_grade = float(
                round(
                    100
                    * min(smart_score, threshold)
                    / threshold
                )
            )
            
            # Apply minimum grade override if set and grade is lower
            if minimum_grade is not None and calculated_grade < minimum_grade:
                calculated_grade = minimum_grade
            
            return calculated_grade

        self._report["Score"] = self._report.apply(assign_grade, axis=1)

    def export_report(self, output: str | PathLike | TextIO) -> None:
        assert self._report is not None, "Report must be loaded before exporting."

        self._report.to_csv(output, index=False)
    
    def get_student_overrides(self) -> StudentOverrides:
        """Get the student overrides manager."""
        return self._student_overrides
    
    def import_student_overrides(self, csv_path: str) -> None:
        """Import student overrides from CSV file."""
        self._student_overrides.import_overrides(csv_path)
    
    def set_student_override(self, student_id: str, smart_score_threshold: Optional[float] = None, 
                           minimum_grade: Optional[float] = None) -> None:
        """Set override for a specific student."""
        self._student_overrides.set_override(student_id, smart_score_threshold, minimum_grade)
    
    def get_student_override(self, student_id: str) -> tuple[Optional[float], Optional[float]]:
        """Get override for a specific student.""" 
        return self._student_overrides.get_override(student_id)
    
    def has_student_overrides(self) -> bool:
        """Check if any student overrides are loaded."""
        return self._student_overrides.has_overrides()


def _fix_column_counts(lines: list[str]) -> list[str]:
    expected_column_count = lines[0].count(",") + 1

    # Naively fix lines with too many columns by merging a blank cell in the middle of the names
    for idx, line in enumerate(lines):
        # Skip the header
        if idx == 0:
            continue

        # From IXL, names come before other fields that could also be blank. We'll assume the first
        # blank cell in a row with too many columns is part of the name.
        column_count = line.count(",") + 1
        if column_count > expected_column_count:
            parts = line.split(",")
            first_blank_index = parts.index("")
            # Merge the blank cell with the previous cell (part of the name)
            parts[first_blank_index - 1] += " " + parts[first_blank_index]
            del parts[first_blank_index]
            lines[idx] = ",".join(parts)

    return lines


def _clean_ids(report: pd.DataFrame) -> pd.DataFrame:
    # Some Student IDs are incorrectly formatted as "ID0123456789" instead of "0123456789"
    report["Student ID"] = (
        report["Student ID"].astype(str).str.lstrip("ID").astype(str).str.strip()
    )

    return report
