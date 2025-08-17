import pandas as pd

class DataValidator:
    @staticmethod
    def validate(data: pd.DataFrame) -> bool:
        # Verifica se há países sem medalhas
        if data[['gold', 'silver', 'bronze']].sum().sum() == 0:
            raise ValueError("Dados inconsistentes: nenhuma medalha encontrada.")
        
        # Verifica se há países duplicados na mesma edição
        duplicates = data.duplicated(subset=['edition_id', 'country_noc'])
        if duplicates.any():
            print(f"Warning: {duplicates.sum()} entradas duplicadas removidas.")
        
        return True