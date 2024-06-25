import streamlit as st
import pandas as pd
from src.scryfall import ScryfallHandler
from src.visualizations import vis_commander_by_released_date
from src.visualizations import vis_distribuition
from src.visualizations import vis_word_cloud
from src.visualizations import vis_colors_rank
from src.visualizations import vis_type_line
from src.visualizations import vis_rarity
from src.visualizations import vis_edhrec_rank
from src.visualizations import add_logo


scryfall_handler = ScryfallHandler()

add_logo()

@st.cache_data(experimental_allow_widgets = True, show_spinner = False)
def get_data():
    return scryfall_handler.commander_cards()

# def get_data_full():
#     return scryfall_handler.commander_cards()

df_commander_cards = get_data()

# df_base_full=get_data_full()



st.header("Visão Commander")
# st.dataframe(df_commander_cards.head(10))

st.plotly_chart(
    vis_commander_by_released_date(df_commander_cards),
    use_container_width=True)

st.plotly_chart(vis_distribuition(df_commander_cards))

fig_count, fig_avg_cmc = vis_type_line(df_commander_cards)
st.plotly_chart(fig_count)
st.plotly_chart(fig_avg_cmc)

fig_count, fig_avg_cmc = vis_rarity(df_commander_cards)
st.plotly_chart(fig_count)
st.plotly_chart(fig_avg_cmc)

st.plotly_chart(vis_colors_rank(df_commander_cards))

st.header("Nuvem de Palavras")
input_type = st.selectbox("Escolha nuvem de palavras que gostaria de exibir:",
                          ['Carta Texto', 'Palavras-chave'],
                          help="""Selecione o tipo de nuvem de palavras que
                          deseja visualizar.""")

if input_type == 'Palavras-chave':
    modulo = st.selectbox("Escolha como gostaria que as palavras-chave fossem"
                          " exibidas:",
                          ['Módulos Combinados', 'Módulos Separados'],
                          help="""Em alguns casos, há mais de uma palavra-chave
                          por módulo. Por isso, escolha se prefere que elas
                          sejam tratadas em conjunto, ou individualmente!""")

    # Exibi a nuvem de palavras apenas após a seleção do usuário
    if st.button("Exibir nuvem de palavras"):
        # Nuvem de palavras
        image_buffer = vis_word_cloud(df_commander_cards, 'Palavras-chave',
                                      modulo)
        st.image(image_buffer, use_column_width=True)

else:
    if st.button("Exibir nuvem de palavras"):
        image_buffer = vis_word_cloud(df_commander_cards, 'Carta Texto', None)
        st.image(image_buffer, use_column_width=True)

# st.header("Ranking EDHREC")
# image_buffer = vis_edhrec_rank(df_base_full)
# st.image(image_buffer, use_column_width=True)
