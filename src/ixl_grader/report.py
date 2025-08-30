import pandas as pd


class Report:
    def __init__(self):
        self._csv_path: str | None = None
        self._report: pd.DataFrame | None = None

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
