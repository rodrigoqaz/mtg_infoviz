import streamlit as st
import pandas as pd
from src.scryfall import ScryfallHandler
from src.visualizations import vis_commander_by_released_date


scryfall_handler = ScryfallHandler()

@st.cache_data(experimental_allow_widgets = True, show_spinner = False)
def get_data():
    return scryfall_handler.commander_cards()


df_commander_cards = get_data()
st.header("Visão Commander")
st.dataframe(df_commander_cards.head(10))
st.plotly_chart(
    vis_commander_by_released_date(df_commander_cards),
    use_container_width=True)

