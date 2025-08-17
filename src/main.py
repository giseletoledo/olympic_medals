from data_loader import CSVDataLoader
from medal_analyzer import MedalAnalyzer
from report_generator import CSVReportGenerator
from data_validator import DataValidator
from constants import SortBy

def main():
    # 1. Carrega e limpa os dados
    loader = CSVDataLoader("data/olympics_medal_tally.csv")
    data = loader.load_data()

    # 2. Valida os dados
    DataValidator.validate(data)

    # 3. Processa e gera relatório
    analyzer = MedalAnalyzer(data)
    sorted_data = analyzer.sort_countries(by=SortBy.GOLD)
    
    report_generator = CSVReportGenerator()
    report_generator.generate(sorted_data.head(10), "outputs/top_10_countries.csv")

if __name__ == "__main__":
    main()