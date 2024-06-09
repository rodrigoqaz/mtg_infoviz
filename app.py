import streamlit as st
import st_pages as sp


sp.show_pages(
    [
        sp.Page("app.py", "Página Inicial", "🏠"),
        sp.Page("pages/page_1.py", "Visão Geral Commander", ":eye:"),
        sp.Page("pages/page_2.py", "Avalie o seu deck", "🃏"),
    ]
)


tab1, tab2, tab3 = st.tabs(["Introdução", "Magic the Gathering", "Equipe"])

with tab1:
   st.write("""
            # MECAI-USP
            ## Visualização de Informação
            ### Magic the Gathering - Uma análise sobre seu Deck

            Trabalho apresentado para a disciplina de Visualização de Informação do programa de Mestrado
            do MECAI - USP

            - Explicar de forma macro o que é magic e apontar para a aba com mais detalhes
            - Explicar sobre a Dinâmica de cartas
            - Explicar sobre o Commander
            - Explicar os objetivos do trabalho
            """)

with tab2:
   st.header("Magic: The Gathering")
   st.write("""
            - Explicar de forma mais detalhada sobre o jogo
            """)   

with tab3:
    st.header("Equipe")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.html('<div style="text-align: center; font-size: 30px"> Allana Silva </div>')
        st.image("https://github.com/allanaasilva.png")
        st.write("""
                 - Estatístico
                 - Mestrando do Mecai
                 - Atribuições:
                    - Arquitetura do projeto
                    - Módulos do Streamlit
                    - Engenharia dos dados
                 """)   

    with col2:
        st.html('<div style="text-align: center; font-size: 30px"> Danielle Silveira </div>')
        st.image("https://github.com/danifowl.png")
        st.write("""
                 - Estatístico
                 - Mestrando do Mecai
                 - Atribuições:
                    - Arquitetura do projeto
                    - Módulos do Streamlit
                    - Engenharia dos dados
                 """)   

    with col3:
        st.html('<div style="text-align: center; font-size: 30px"> Rodrigo Oliveira </div>')
        st.image("https://github.com/rodrigoqaz.png")
        st.write("""
                 - Estatístico
                 - Mestrando do Mecai
                 - Atribuições:
                    - Arquitetura do projeto
                    - Módulos do Streamlit
                    - Engenharia dos dados
                 """)   
   

 
