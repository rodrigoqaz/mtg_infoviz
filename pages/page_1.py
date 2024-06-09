import streamlit as st
import pandas as pd
from src.scryfall import ScryfallHandler
from src.visualizations import vis_commander_by_released_date


scryfall_handler = ScryfallHandler()
df_commander_cards = scryfall_handler.commander_cards()

st.header("Visão Commander")
st.dataframe(df_commander_cards.head(10))
st.plotly_chart(
    vis_commander_by_released_date(df_commander_cards),
    use_container_width=True)

