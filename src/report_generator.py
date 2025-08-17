import pandas as pd
from typing import Protocol

class ReportGenerator(Protocol):
    def generate(self, data: pd.DataFrame, output_path: str) -> None:
        ...

class CSVReportGenerator:
    def generate(self, data: pd.DataFrame, output_path: str) -> None:
        data.to_csv(output_path, index=False)