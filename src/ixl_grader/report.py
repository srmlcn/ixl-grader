import pandas as pd


class Report:
    def __init__(self):
        self._csv_path: str | None = None
        self._report: pd.DataFrame | None = None
