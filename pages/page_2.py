import streamlit as st
from src.visualizations import add_logo

add_logo()

css='''
<style>
[data-testid="stFileUploaderDropzone"] div div::before {content:"Arraste seu arquivo txt"}
[data-testid="stFileUploaderDropzone"] div div span{display:none;}
[data-testid="stFileUploaderDropzone"] div div::after {font-size: .8em; content:"Limite de 200MB por arquivo"}
[data-testid="stFileUploaderDropzone"] div div small{display:none;}
[data-testid="stFileUploaderDropzone"] button {visibility:hidden;}
[data-testid="stFileUploaderDropzone"] button::after {visibility: visible; content:"Selecionar Arquivo";}
</style>
'''

st.header("Insira seu Deck")
st.selectbox("Commander:", options=['A', 'B'])
uploaded_files = st.file_uploader("Selecione o arquivo do seu deck", accept_multiple_files=True, type='txt')
st.markdown(css, unsafe_allow_html=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.text_area('Deck: ', value=bytes_data.decode(), height=500)