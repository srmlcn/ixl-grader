import pandas as pd


class Report:
    def __init__(self):
        self._csv_path: str | None = None
        self._report: pd.DataFrame | None = None

    def _load_report(self) -> pd.DataFrame:
        assert (
            self._csv_path is not None
        ), "CSV path must be set before loading the report."
        return pd.read_csv(self._csv_path)
