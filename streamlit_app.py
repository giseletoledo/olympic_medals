import streamlit as st
from src.data_loader import CSVDataLoader
from src.medal_analyzer import MedalAnalyzer
from src.constants import SortBy

def main():
    # Configuração da página
    st.set_page_config(page_title="Medalhas Olímpicas", layout="wide")
    
    # Título
    st.title("Análise de Medalhas Olímpicas")
    st.markdown("Top 10 países por medalhas")

    # Carrega e processa os dados
    loader = CSVDataLoader("data/olympics_medal_tally.csv")
    analyzer = MedalAnalyzer(loader.load_data())

    medal_colors = {
    "gold": "#FFD700",  # Amarelo ouro
    "silver": "#C0C0C0",  # Cinza prata
    "bronze": "#CD7F32"   # Marrom bronze
    }

    # Sidebar com filtros
    with st.sidebar:
        st.header("Filtros")
        sort_by = st.selectbox(
            "Ordenar por:",
            options=list(SortBy),
            format_func=lambda x: x.value.capitalize()
        )
        n_countries = st.slider("Número de países:", 5, 20, 10)

    # Dados processados
    sorted_data = analyzer.sort_countries(by=sort_by).head(n_countries)

    # Visualização

    chart_data = sorted_data.set_index("country")[["gold", "silver", "bronze"]]
    st.bar_chart(
    chart_data,
    color=[medal_colors["gold"], medal_colors["silver"], medal_colors["bronze"]]  # Cores personalizadas
    )

    st.subheader(f"Top {n_countries} países por medalhas")
    st.dataframe(sorted_data)

if __name__ == "__main__":
    main()