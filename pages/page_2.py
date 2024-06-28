import streamlit as st
import streamlit.components.v1 as components
from src.scryfall import ScryfallHandler
from src.visualizations import add_logo, vis_sinergy_graph, vis_word_cloud
from src.visualizations import vis_distribuition, vis_more_expensive_cards
from src.visualizations import vis_colors_rank, vis_type_line, vis_rarity
from src.visualizations import vis_age, vis_combos_graph, vis_cards_without_sinergy
from src.obtain_sinergy import obtain_sinergy


add_logo()

tab1, tab2, tab3, tab4 = st.tabs(["Importar o Deck", "Sinergia e Combos",
                                  "Nuvem de Palavras", "Estatísticas do Deck"])


with tab1:

    with open('styles/app.html', 'r') as file:
        css = file.read().rstrip()

    scryfall_handler = ScryfallHandler()
    @st.cache_data(experimental_allow_widgets=True, show_spinner=False)
    def get_data():
        return scryfall_handler.commander_cards(only_commander=False)

    def display_deck_fileuploader(uploaded_file):
        if uploaded_file is not None:
            deck = uploaded_file.read().decode("utf-8")
            st.session_state["deck"] = deck
            st.text_area("Deck:", deck, height=300)

    def display_example_card(card_name):

        if "select_file_text" not in st.session_state:
            st.session_state.select_file_text = False

        def callback_bt_select_file():
            st.session_state.show_analisys_page = True
            st.session_state.select_file_text = False

        match card_name:
            case 'Ayara, First of Locthwain':
                filename = 'exemplo_deck_ayara.txt'
            case 'Oloro, Ageless Ascetic':
                filename = 'exemplo_deck_oloro.txt'
            case 'Pantlaza, Sun-Favored':
                filename = 'exemplo_deck_pantlaza.txt'
        st.header(card_name)
        example_card = df_commander_cards[df_commander_cards[
            'name'] == card_name]
        st.image(example_card['image_uris.normal'].values[0])

        if st.button('Selecionar', key=card_name):
            with open(filename) as file:
                st.session_state['deck'] = file.read()
            st.text_area("Deck:", st.session_state['deck'], height=300)
            st.session_state["commander"] = card_name
            st.session_state.select_file_text = True

        if st.session_state.select_file_text:
            if st.button('Carregar Deck', key='carregar' + card_name,
                         on_click=callback_bt_select_file):
                print('teste')

    st.markdown(css, unsafe_allow_html=True)
    st.header("Analise o seu Deck")
    df_commander_cards = get_data()

    if "show_analisys_page" not in st.session_state:
        st.session_state.show_analisys_page = False

    if "show_commander_selectbox" not in st.session_state:
        st.session_state.show_commander_selectbox = False

    if "show_deck_fileuploader" not in st.session_state:
        st.session_state.show_deck_fileuploader = False

    if "show_process_button" not in st.session_state:
        st.session_state.show_process_button = False

    opcao_deck = st.radio(
        label = 'Que tipo de dado gostaria de utilizar?',
        options=['Utilizar um deck de exemplo', 'Importar o próprio deck'],
        horizontal=True,
        index=None
        )

    if opcao_deck == 'Utilizar um deck de exemplo':

        col1, col2, col3 = st.columns(3)
        with col1:
            display_example_card('Ayara, First of Locthwain')
        with col2:
            display_example_card('Oloro, Ageless Ascetic')
        with col3:
            display_example_card('Pantlaza, Sun-Favored')

    if opcao_deck == 'Importar o próprio deck':
        
        st.session_state.show_commander_selectbox = True
        
        if st.session_state.show_commander_selectbox:
            commander = st.selectbox("Seleciona o Commander:",
                                     options=df_commander_cards[
                                         'name'].to_list())
            st.session_state["commander"] = commander
            if st.button('Selecionar o deck'):
                st.session_state.show_deck_fileuploader = True

        if st.session_state.show_deck_fileuploader:
            uploaded_file = st.file_uploader("Selecione o arquivo do seu deck",
                                             accept_multiple_files=False,
                                             type='txt')
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
        deck = [line[2:].strip() for line in st.session_state[
            "deck"].strip().split('\n')]
        commander = st.session_state["commander"]
        sinergy = obtain_sinergy(commander, deck)
        vis_sinergy_graph(sinergy['cards_with_synergy'], commander)
        vis_combos_graph(commander, deck)
        
        st.header('Sinergia entre o Comandante e seu deck (EDHREC)')
        html_file_sinergy = open("synergy.html", 'r', encoding='utf-8')
        source_code_sinergy = html_file_sinergy.read()
        components.html(source_code_sinergy, height=760)
        
        st.header('Grafo dos combos relacionados ao Comandante (EDHREC)')
        html_file_combos = open("combos.html", 'r', encoding='utf-8')
        source_code_combos = html_file_combos.read()
        components.html(source_code_combos, height=760)

        st.header('Lista das cartas sem sinergia')
        html_content = vis_cards_without_sinergy(sinergy['cards_without_synergy'], commander)
        st.markdown(html_content, unsafe_allow_html=True)

with tab3:
    if st.session_state.show_analisys_page:
        st.header("Nuvem de Palavras")
        df_commander_cards_deck = df_commander_cards.query('name in @deck')
        input_type = st.selectbox(
            "Escolha nuvem de palavras que gostaria de exibir:",
            ['Carta Texto', 'Palavras-chave'],
            help="""Selecione o tipo de nuvem de palavras que deseja visualizar.""")

        if input_type == 'Palavras-chave':
            modulo = st.selectbox("Escolha como gostaria que as palavras-chave fossem"
                                " exibidas:",
                                ['Módulos Combinados', 'Módulos Separados'],
                                help="""Em alguns casos, há mais de uma palavra-chave
                                por módulo. Por isso, escolha se prefere que elas
                                sejam tratadas em conjunto, ou individualmente!""")

            # Exibi a nuvem de palavras apenas após a seleção do usuário
            
            if st.button("Exibir nuvem de palavras"):
                df_commander_cards_deck.to_csv('teste.csv')
                # Nuvem de palavras
                image_buffer = vis_word_cloud(df_commander_cards_deck,
                                              'Palavras-chave', modulo)
                st.image(image_buffer, use_column_width=True)

        else:
            if st.button("Exibir nuvem de palavras"):
                image_buffer = vis_word_cloud(df_commander_cards_deck,
                                              'Carta Texto', None)
                st.image(image_buffer, use_column_width=True)

with tab4:
    if st.session_state.show_analisys_page:
        df_commander_cards_deck = df_commander_cards.query('name in @deck')
        st.header('Idade do Deck')
        st.plotly_chart(vis_age(df_commander_cards_deck))

        st.header('CMC')
        st.plotly_chart(vis_distribuition(df_commander_cards_deck))

        st.header('Subtipos mais frequentes do deck')
        fig_count, fig_avg_cmc = vis_type_line(df_commander_cards_deck)
        st.plotly_chart(fig_count)
        st.plotly_chart(fig_avg_cmc)

        st.header('Raridade')
        fig_count, fig_avg_cmc = vis_rarity(df_commander_cards_deck)
        st.plotly_chart(fig_count)
        st.plotly_chart(fig_avg_cmc)

        html_content = vis_more_expensive_cards(df_commander_cards_deck)
        st.markdown(html_content, unsafe_allow_html=True)

        # st.header('Cartas banidas')

        st.header('Cores')
        st.plotly_chart(vis_colors_rank(df_commander_cards_deck))

        # st.header('Ver se tem carta engraçada')

if st.button('Nova análise'):
    st.session_state.show_commander_selectbox = True
    st.session_state.show_deck_fileuploader = False
    st.session_state.show_process_button = False
    st.session_state.show_analisys_page = False
    st.rerun()

