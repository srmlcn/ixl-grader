import pandas as pd


class Report:
    def __init__(self):
        self._csv_path: str | None = None
        self._report: pd.DataFrame | None = None

    def _fix_csv(self) -> None:
        assert self._csv_path is not None, "CSV path must be set before fixing the CSV."

        raise NotImplementedError("CSV fixing not yet implemented.")

    def _load_report(self) -> pd.DataFrame:
        assert (
            self._csv_path is not None
        ), "CSV path must be set before loading the report."
        return pd.read_csv(self._csv_path)

    def import_report(self, csv_path: str) -> None:
        self._csv_path = csv_path
        self._report = self._load_report()
