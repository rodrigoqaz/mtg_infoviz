import streamlit as st
import streamlit.components.v1 as components
from src.scryfall import ScryfallHandler
from src.visualizations import add_logo, vis_sinergy_graph, vis_word_cloud
from src.obtain_sinergy import obtain_sinergy


add_logo()

tab1, tab2, tab3, tab4 = st.tabs(["Importar o Deck", "Sinergia e Combos", "Nuvem de Palavras", "Estatísticas do Deck"])


with tab1:

    with open('styles/app.html', 'r') as file:
        css = file.read().rstrip()

    scryfall_handler = ScryfallHandler()
    @st.cache_data(experimental_allow_widgets = True, show_spinner = False)
    def get_data():
        return scryfall_handler.commander_cards()

    def display_deck_fileuploader(uploaded_file):
        if uploaded_file is not None:
            deck = uploaded_file.read().decode("utf-8")
            st.session_state["deck"] = deck
            st.text_area("Deck:", deck, height=300)

    df_commander_cards = get_data()

    st.markdown(css, unsafe_allow_html=True)
    st.header("Analise o seu Deck")

    # Selecionar o comandante
    # Importar o Deck
    # Processar
    #   Limpa a tela e mostra as análise
    #   Botão para nova análise

    if "show_commander_selectbox" not in st.session_state:
        st.session_state.show_commander_selectbox = True

    if "show_deck_fileuploader" not in st.session_state:
        st.session_state.show_deck_fileuploader = False

    if "show_process_button" not in st.session_state:
        st.session_state.show_process_button = False

    if "show_analisys_page" not in st.session_state:
        st.session_state.show_analisys_page = False

    if st.session_state.show_commander_selectbox:
        commander = st.selectbox("Seleciona o Commander:", options=df_commander_cards['name'].to_list())
        st.session_state["commander"] = commander
        if st.button('Selecionar o deck'):
            st.session_state.show_deck_fileuploader = True

    if st.session_state.show_deck_fileuploader:
        uploaded_file = st.file_uploader("Selecione o arquivo do seu deck", accept_multiple_files=False, type='txt')
        if uploaded_file is not None:
            display_deck_fileuploader(uploaded_file)
            st.session_state.show_process_button = True

    if st.session_state.show_process_button:
        if st.button("Importar o deck"):
            st.session_state.show_commander_selectbox = False
            st.session_state.show_deck_fileuploader = False
            st.session_state.show_process_button = False
            st.session_state.show_analisys_page = True
            st.rerun()



with tab2:
    if st.session_state.show_analisys_page:
        deck = [line[2:].strip() for line in st.session_state["deck"].strip().split('\n')]
        commander = st.session_state["commander"]
        sinergy = obtain_sinergy(commander, deck)
        vis_sinergy_graph(sinergy['cards_with_synergy'],commander)
        st.header('Sinergia entre o Commander e seu deck')
        HtmlFile = open("synergy.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 760)
        st.header('Grafo dos combos')
        st.header('Lista das cartas sem sinergia')

with tab3:
    if st.session_state.show_analisys_page:
        st.header("Nuvem de Palavras")
        df_commander_cards_deck = df_commander_cards.query('name in @deck')
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
                image_buffer = vis_word_cloud(df_commander_cards_deck, 'Palavras-chave',
                                            modulo)
                st.image(image_buffer, use_column_width=True)

        else:
            if st.button("Exibir nuvem de palavras"):
                image_buffer = vis_word_cloud(df_commander_cards_deck, 'Carta Texto', None)
                st.image(image_buffer, use_column_width=True)

with tab4:
    if st.session_state.show_analisys_page:
        st.header('Idade do Deck')
        st.header('CMC')
        st.header('Subtipos mais frequentes do deck')
        
        st.header('Raridade')
        st.header('top 10 mais caras')
        st.header('cartas banidas')

        st.header('Cores')
        
        
        
        st.header('Ver se tem carta engraçada')

if st.button('Nova análise'):
    st.session_state.show_commander_selectbox = True
    st.session_state.show_deck_fileuploader = False
    st.session_state.show_process_button = False
    st.session_state.show_analisys_page = False
    st.rerun()

