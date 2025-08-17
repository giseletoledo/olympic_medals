import streamlit as st
from src.data_loader import CSVDataLoader
from src.medal_analyzer import MedalAnalyzer
from enum import Enum


class MedalType(Enum):
    TODAS = "total"
    OURO = "gold"
    PRATA = "silver"
    BRONZE = "bronze"


def get_filtered_data(df, medal_type: MedalType, n_countries: int):
    """Filtra, ordena e retorna os dados prontos para exibição."""
    # Remove países sem medalhas (se não for 'todas')
    if medal_type != MedalType.TODAS:
        df = df[df[medal_type.value] > 0]

    # Ordena sempre do maior para o menor
    sorted_df = df.sort_values(by=medal_type.value, ascending=False)

    # Seleciona apenas os top N países
    return sorted_df.head(n_countries)


def render_sidebar():
    """Renderiza todos os filtros na sidebar."""
    with st.sidebar:
        st.header("Filtros")

        medal_type = st.selectbox(
            "Mostrar medalhas:",
            options=list(MedalType),
            format_func=lambda x: x.name.replace("_", " ").title()
        )

        n_countries = st.slider("Número de países:", 5, 20, 10)

    return medal_type, n_countries


def render_charts(df, medal_type: MedalType, n_countries: int):
    """Renderiza os gráficos principais."""
    st.markdown(f"### Top {n_countries} países por medalhas de {medal_type.name.lower()}")

    if medal_type == MedalType.TODAS:
        st.bar_chart(
            df.set_index("country")[["gold", "silver", "bronze"]],
            color=["#FFD700", "#C0C0C0", "#CD7F32"]
        )
    else:
        st.bar_chart(
            df.set_index("country")[[medal_type.value]],
            color="#FFD700" if medal_type == MedalType.OURO else 
                  "#C0C0C0" if medal_type == MedalType.PRATA else "#CD7F32"
        )


def render_table(df):
    """Renderiza a tabela formatada."""
    st.dataframe(
        df.rename(columns={
            "country": "País",
            "gold": "Ouro",
            "silver": "Prata",
            "bronze": "Bronze",
            "total": "Total"
        }),
        column_config={
            "País": st.column_config.TextColumn("País"),
            "Ouro": st.column_config.NumberColumn("Ouro", format="%d"),
            "Prata": st.column_config.NumberColumn("Prata", format="%d"),
            "Bronze": st.column_config.NumberColumn("Bronze", format="%d"),
            "Total": st.column_config.NumberColumn("Total", format="%d")
        },
        hide_index=True,
        use_container_width=True
    )


def main():
    st.set_page_config(page_title="Análise de Medalhas Olímpicas", layout="wide")
    st.title("Análise de Medalhas Olímpicas")

    try:
        # Carrega dados
        loader = CSVDataLoader("data/olympics_medal_tally.csv")
        analyzer = MedalAnalyzer(loader.load_data())
        df = analyzer.aggregate_medals()

        # Sidebar (filtros)
        medal_type, n_countries = render_sidebar()

        # Processa dados
        filtered_df = get_filtered_data(df, medal_type, n_countries)

        # Renderiza visualizações
        render_charts(filtered_df, medal_type, n_countries)
        render_table(filtered_df)

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()
