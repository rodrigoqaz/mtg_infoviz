import streamlit as st
from src.visualizations import add_logo

add_logo()

st.sidebar.radio('drops sub-menu', options=['add drops', 'view drops'])
st.sidebar.checkbox('special')