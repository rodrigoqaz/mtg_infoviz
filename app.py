import streamlit as st
import st_pages as sp
from src.visualizations import add_logo


add_logo()

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

            ### História de Magic: The Gathering
            Magic: The Gathering (MTG) foi criado por Richard Garfield e lançado em 1993 pela Wizards of the Coast. Desenvolvido como um jogo rápido e portátil, MTG estabeleceu o gênero de cartas colecionáveis. Jogadores atuam como "planeswalkers", magos que viajam entre mundos, invocando criaturas e lançando feitiços. Além do jogo competitivo, MTG atrai colecionadores devido às ilustrações e edições especiais. A iniciativa "Universes Beyond" trouxe coleções temáticas de franquias populares, como O Senhor dos Anéis e Assassin’s Creed.

            ### O Formato Commander
            Commander, popular nos últimos anos, permite jogos em grupos maiores, usando um "comandante" e um baralho de 99 cartas sem repetições. Este formato utiliza uma vasta gama de cartas, tornando-o diversificado e ideal para partidas em grupo.

            ### Construção de Decks
            Construir decks é uma das atividades mais empolgantes do Magic. Sites como Scryfall, EDHREC e MTGGoldfish ajudam jogadores a encontrar sinergias e combos, além de acompanhar o metagame.

            ### Mercado de Cartas
            Magic: The Gathering é um negócio bilionário, com uma indústria de produtos relacionados e cartas valiosas. Em 2022, MTG se tornou a primeira marca bilionária da Hasbro. Cartas como "Black Lotus" são extremamente valiosas, exemplificando o valor do mercado de cartas.

            ### Propósito do Projeto
            Atualmente, existem diversos sites que auxiliam na construção de decks para Commander, oferecendo recomendações de combinações de cartas, sinergias e metagame. No entanto, ainda falta uma ferramenta que ofereça uma análise completa e detalhada de um deck já construído. Este projeto visa preencher essa lacuna com uma análise detalhada dos decks enviados pelos usuários. A ferramenta irá:

            - **Identificar Combos e Sinergias:** Destacar combinações poderosas entre cartas e o comandante.
            - **Avaliação de Cartas:** Indicar cartas menos eficientes no deck.
            - **Recomendações de Cartas:** Sugerir alternativas para melhorar o desempenho.
            - **Análise de Edições e Reimpressões:** Fornecer estatísticas sobre as edições das cartas no deck.
            - **Informações Curiosas:** Oferecer dados sobre expansões, raridade e valor das cartas.

            """)

with tab2:
    st.header("Magic: The Gathering")
    st.write("""
            ### O Formato Commander de Magic: The Gathering

            **O que é Commander?**
            Commander, também conhecido como Elder Dragon Highlander (EDH), é um formato de jogo de Magic: The Gathering que enfatiza a jogabilidade em grupo e a construção de decks com diversidade. Este formato permite que os jogadores usem uma ampla variedade de cartas de toda a história do Magic, criando experiências de jogo únicas e dinâmicas.

            **Regras Básicas:**

            **Comandante:**
            - Cada jogador escolhe uma criatura lendária ou um planeswalker designado como seu "comandante".
            - O comandante começa o jogo na "zona de comando" e pode ser conjurado a partir dessa zona.

            **Deck:**
            - Cada deck deve conter exatamente 100 cartas, incluindo o comandante.
            - Exceto por terrenos básicos, nenhuma carta pode ser repetida no deck.
            - As cartas do deck devem corresponder à identidade de cores do comandante, definida pelos símbolos de mana na carta do comandante.

            **Pontos de Vida:**
            - Cada jogador começa com 40 pontos de vida.
            - Se um jogador receber 21 ou mais pontos de dano de combate de um único comandante, ele perde o jogo.

            **Jogabilidade:**
            - O formato é geralmente jogado em mesas de 4 jogadores, mas pode ser adaptado para diferentes números de participantes.
            - As regras do jogo são as mesmas do Magic tradicional, com algumas exceções específicas para o formato Commander.

            **Exemplos de Combos e Sinergias:**

            **Infinite Mana Combos:**
            - **Combo: “Dramatic Reversal” + “Isochron Scepter”**
                - Isochron Scepter imprints Dramatic Reversal.
                - Com pelo menos dois manas de quaisquer fontes (como artefatos que produzem mana), ativar Isochron Scepter para copiar e conjurar Dramatic Reversal, desvirando todas as suas permanentes não-terreno, incluindo as que produzem mana, gerando mana infinito.

            **Infinite Damage Combos:**
            - **Combo: “Kiki-Jiki, Mirror Breaker” + “Zealous Conscripts”**
                - Kiki-Jiki, Mirror Breaker cria uma cópia de Zealous Conscripts, desvirando Kiki-Jiki.
                - A nova cópia repete o processo, criando cópias infinitas de Zealous Conscripts, permitindo ataques ilimitados.

            **Card Draw Combos:**
            - **Combo: “Niv-Mizzet, Parun” + “Curiosity”**
                - Quando Niv-Mizzet causa dano, você compra uma carta.
                - Com Curiosity anexado a Niv-Mizzet, comprar uma carta faz com que Niv-Mizzet cause 1 de dano a qualquer alvo, desencadeando o ciclo novamente para comprar cartas infinitamente.

            **Estratégias e Dicas:**

            **Construção de Deck:**
            - Escolher um comandante com habilidades sinérgicas e construir o deck ao redor dessas habilidades.
            - Incluir cartas que protejam o comandante e permitam que suas habilidades sejam usadas efetivamente.
            - Balancear o deck com ramp (cartas que aceleram a produção de mana), remoção (cartas que eliminam ameaças) e draw (cartas que aumentam a quantidade de cartas na mão).

            **Jogabilidade:**
            - Focar em estabelecer uma presença no campo de batalha enquanto se defende contra ameaças dos oponentes.
            - Prestar atenção às jogadas e estratégias dos oponentes para antecipar e responder a ameaças.
            - Utilizar a política e diplomacia, especialmente em jogos com múltiplos jogadores, para criar alianças temporárias e evitar ser o alvo principal.

            **Fontes:**
            - [Magic: The Gathering - Commander Rules](https://magic.wizards.com/en/formats/commander)
            - [EDHREC - Combo Search](https://edhrec.com/combos)
            - [MTGGoldfish - Commander Decks and Strategy](https://www.mtggoldfish.com/metagame/commander)
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
                 - Capacity Planning Analyst
                 - Mestrando do Mecai
                 - Atribuições:
                    - Bases de informações
                    - Dashboards
                    - Play tester
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
   

 
# TODO:

# Introdução e Explicação do Magic - Dani
# Buscar referências sobre sinergia e EDHREC  - Dani

# Visão Geral - Allana

# - Distribuição do CMC, cores e tipos
# - Nuvem de Palavras - Colocar Dropdown para selecionar
# - Ranking do EDHREC

# Análise - Rodrigo

# - Input do Deck - Escreve o comandante e depois sobe o arquivo
# - Grafo de Sinergia
# - Nuvem de palavras
# - Cores e tipos