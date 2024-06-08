import streamlit as st

tab1, tab2, tab3 = st.tabs(["Sobre", "Visão Geral Commander", "Analise seu Deck"])

with tab1:
   st.header("Sobre")
   st.write("""
            # MECAI-USP
            ## Visualização de Informação
            ### Magic the Gathering - Uma análise sobre seu Deck

            Alunos:

            Allana Silva
            Danielle Silveira
            Rodrigo Oliveira
            
            """)
   
   st.image('https://cards.scryfall.io/normal/front/e/d/ed0ace28-9a33-4f0d-b8c8-f5517f20ccf1.jpg?1572490057')

with tab2:
   st.header("Visão Geral Commander")
   

with tab3:
   st.header("Analise seu Deck")
   input_deck = st.text_area("Insira o seu deck")
   if st.button("Importar"):
      print(input_deck)
      st.write(input_deck)
   

 
