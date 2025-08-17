from typing import List, Dict
import pandas as pd
from src.constants import SortBy

class MedalAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def aggregate_medals(self) -> pd.DataFrame:
        return self.data.groupby('country').agg({
            'gold': 'sum',
            'silver': 'sum',
            'bronze': 'sum',
            'total': 'sum'
        }).reset_index()

    def sort_countries(self, by: SortBy, ascending: bool = False) -> pd.DataFrame:
        return self.aggregate_medals().sort_values(by=by, ascending=ascending)