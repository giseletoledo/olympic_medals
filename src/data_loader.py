import pandas as pd
from typing import Protocol

class DataLoader(Protocol):
    def load_data(self) -> pd.DataFrame:
        ...

class CSVDataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.file_path)
        return self._clean_data(data)

    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove nulos, duplicatas e corrige formatos."""
        # Remove linhas com valores nulos em colunas críticas
        data = data.dropna(subset=['country', 'gold', 'silver', 'bronze'])
        
        # Preenche nulos em 'total' se as medalhas existirem
        data['total'] = data['total'].fillna(
            data['gold'] + data['silver'] + data['bronze']
        )
        
        # Remove duplicatas (se houver)
        data = data.drop_duplicates(subset=['edition_id', 'country_noc'])
        
        # Converte medalhas para inteiros (caso estejam como float)
        medal_columns = ['gold', 'silver', 'bronze', 'total']
        data[medal_columns] = data[medal_columns].astype(int)
        
        return data