import io
import math
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
from pyedhrec import EDHRec
from PIL import Image, ImageEnhance
import base64

def add_logo():
    st.set_page_config(
        page_title="MTG - Uma análise sobre seu Deck",
        page_icon="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/microsoft/106/mage_1f9d9.png",
        layout="wide"
    )
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(http://media.wizards.com/2016/images/daily/MM20161114_Wheel.png);
                background-repeat: no-repeat;
                padding-top: 100px;
                background-position: 100px 10px;
                background-size: 120px;  /* Set the width of the image */
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def vis_commander_by_released_date(df_commander_cards):
    df_commander_cards['released_year'] = df_commander_cards[
        'released_at'].str[:4]
    commander_by_released_date = df_commander_cards.groupby(
        'released_year').size()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                            x=commander_by_released_date.index,
                            y=commander_by_released_date.values,
                            mode='lines+markers',
                            name='lines+markers'))
    fig.update_layout(title='Quantidade de Comandantes lançados por ano',
                    xaxis_title='Ano',
                    yaxis_title='Quantidade')
    return fig


def vis_age(df):
    df['released_at'] = pd.to_datetime(df['released_at'])
    today = datetime.today()
    df['idade'] = today.year - df['released_at'].dt.year

    freq = df['idade'].value_counts().sort_values(ascending=False)

    fig = px.bar(x=freq.index, y=freq.values,
                 labels={'x': 'Idade (anos)', 'y': 'Frequência'},
                 title='Frequência da Idade das Cartas (anos)',
                 text=freq.values,
                 opacity=0.8,
                 color_discrete_sequence=['indianred'])

    fig.update_layout(showlegend=False)
    fig.update_xaxes(type='category')

    return fig


def vis_distribuition(df):

    fig = px.histogram(df,
                       x='cmc',
                       title=('Distribuição de Custo de Mana Convertido '
                              '(CMC) dos Comandantes'),
                       labels={'cmc': 'CMC'},
                       opacity=0.8,
                       color_discrete_sequence=['indianred'])
    fig.update_layout(yaxis_title="Quantidade")

    return fig


def vis_word_cloud(df, col_name: str, sep_keywords: str):
    if col_name == 'Palavras-chave':
        if sep_keywords == 'Módulos Combinados':
            all_keywords_combined = ' '.join([' '.join(keywords) for keywords
                                              in df['keywords']])
            # Gerar a nuvem de palavras combinada
            wordcloud_combined = WordCloud(width=800, height=400,
                                           background_color='white').generate(
                                               all_keywords_combined)
            # Plotar a nuvem de palavras combinada
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud_combined, interpolation='bilinear')
            plt.axis('off')

        else:
            individual_keywords = ' '.join([keyword for keywords in
                                            df['keywords'] for keyword in
                                            keywords])
            wordcloud_individual = WordCloud(
                width=800, height=400, background_color='white').generate(
                    individual_keywords)
            # Plotar a nuvem de palavras individual
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud_individual, interpolation='bilinear')
            plt.axis('off')

    else:
        all_text = ' '.join(df['oracle_text'].dropna())
        wordcloud = WordCloud(width=800,
                              height=400,
                              background_color='white').generate(all_text)
        # Plotar a nuvem de palavras
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Buffer de memória contendo a imagem
    return buf


def vis_colors_rank(df):
    df = df.explode('colors')
    color_distribution = df['colors'].value_counts()
    color_dict = {'B': 'rgba(0, 0, 0, 0.5)',
                  'U': 'rgba(0, 0, 255, 0.5)',
                  'G': 'rgba(0, 128, 0, 0.5)',
                  'R': 'rgba(255, 0, 0, 0.5)',
                  'W': 'rgba(255, 255, 0, 0.5)'}

    fig = px.bar(x=color_distribution.index,
                 y=color_distribution.values,
                 color_discrete_map=color_dict,
                 color=color_distribution.index,
                 text=color_distribution.values,
                 labels={'x': 'CORES', 'y': 'Total'},
                 title='<b>Predominâncias das Identidades dos Comandantes')

    fig.update_layout(showlegend=False)
    fig.update_yaxes(tickformat="000")

    return fig


def split_types(type_line):
    if pd.isna(type_line):
        return []
    parts = type_line.split('—')
    if len(parts) > 1:
        subtypes = parts[1].split('//')
        return [subtype.strip() for subtype in subtypes]
    return []


def vis_type_line(df):
    # Aplica a função split_types para processar os subtipos
    df['subtypes'] = df['type_line'].apply(split_types)
    
    # Explode os subtipos em linhas separadas para cada subtipo
    df_exploded = df.explode('subtypes')

    # Calcula a contagem dos subtipos
    rank_subtype = df_exploded['subtypes'].value_counts().sort_values(ascending=False)
    top_subtype = rank_subtype.head(10)

    # Filtra apenas os subtipos mais frequentes para análise
    df_filtered_subtype = df_exploded[df_exploded['subtypes'].isin(top_subtype.index)]

    # Agrupa por subtipo e calcula a média e a contagem do CMC
    grouped_data = df_filtered_subtype.groupby('subtypes')['cmc'].agg(['mean', 'count']).reset_index()
    grouped_data.columns = ['subtypes', 'cmc', 'TYPE_COUNT']
    mean_cmc = grouped_data.sort_values(by='cmc', ascending=False)
    mean_cmc['cmc'] = round(mean_cmc['cmc'], 2)

    # Cria os gráficos
    fig1 = px.bar(top_subtype, x=top_subtype.index, y=top_subtype.values,
                  color=top_subtype.index, text=top_subtype.values,
                  labels={'subtypes': 'Subtipos Mais Frequentes dos Comandantes', 'y': 'Total'},
                  template='seaborn', title='<b>Subtipos Mais Frequentes dos  Comandantes')
    fig1.update_layout(showlegend=False)
    fig1.update_yaxes(tickformat="000")

    fig2 = px.bar(mean_cmc, x='subtypes', y='cmc',
                  color='subtypes',
                  labels={'subtypes': 'Subtipos de Criaturas', 'cmc': 'CMC Médio'},
                  text='TYPE_COUNT',
                  template='seaborn', title='<b>CMC Médio por Subtipo de Criatura Comandante')
    fig2.update_layout(showlegend=False)
    fig2.update_yaxes(tickformat="000")
    fig2.update_traces(textfont_size=8)

    return fig1, fig2


def vis_rarity(df):

    rank_rarity = df['rarity'].value_counts().sort_values(
        ascending=False)

    grouped_data = df.groupby('rarity')['cmc'].agg(
        ['mean', 'count']).reset_index()

    grouped_data.columns = ['rarity', 'cmc', 'TYPE_COUNT']
    mean_cmc = grouped_data.sort_values(by='cmc', ascending=False)

    mean_cmc['cmc'] = round(mean_cmc['cmc'], 2)

    fig1 = px.bar(rank_rarity, x=rank_rarity.index, y=rank_rarity.values,
                  color=rank_rarity.index, text=rank_rarity.values,
                  labels={'rarity': 'Raridade',
                          'y': 'Total'},
                  title='<b> Frequência de raridade dos comandantes',
                  template='seaborn')
    fig1.update_layout(showlegend=False)
    fig1.update_yaxes(tickformat="000")

    fig2 = px.bar(mean_cmc, x='rarity', y='cmc',
                  color='rarity',
                  labels={'rarity': 'Raridade',
                        'cmc': 'CMC MÉDIO'},
                  text='TYPE_COUNT',
                  template='seaborn',
                  title='<b> CMC Médio por Raridade do Comandante')
    fig2.update_layout(showlegend=False)
    fig2.update_yaxes(tickformat="000")
    fig2.update_traces(textfont_size=8)

    return fig1, fig2


def vis_more_expensive_cards(df):

    top_10_expensive_cards = df.sort_values(by='prices.usd', ascending=False).head(10)
    html_content = '<h3>Cartas mais caras:</h3><div style="display: flex; flex-wrap: wrap;">'

    count = 0
    for _, card in top_10_expensive_cards.iterrows():
        if count % 3 == 0 and count != 0:
            html_content += '</div><div style="display: flex; flex-wrap: wrap;">'
        html_content += '<div style="margin: 10px; text-align: center;">'
        html_content += f'<img src="{card["image_uris.small"]}" alt="{card["name"]}" style="width: 150px;"/>'
        html_content += f'<p style="font-size: 11px;">{card["name"]} - USD {card["prices.usd"]}</p>'
        html_content += '</div>'
        count += 1

    html_content += '</div>'
    return html_content


# def vis_edhrec_rank(df):

#     df = df[df['edhrec_rank'].notnull()]
#     df = df.sort_values('edhrec_rank').head(10)

#     fig, axes = plt.subplots(2, 5, figsize=(20, 8))
#     axes = axes.flatten()

#     for i, (index, row) in enumerate(df.iterrows()):
#         img_url = row['image_uris.normal']
#         if img_url:
#             response = requests.get(img_url)
#             img = Image.open(io.BytesIO(response.content))
#             axes[i].imshow(img)
#             axes[i].axis('off')
#             axes[i].set_title(f"{row['name']} (Rank: {row['edhrec_rank']})", fontsize=12)
#         else:
#             axes[i].axis('off')
#             axes[i].set_title(f"{row['name']} (Rank: {row['edhrec_rank']})\nImagem não disponível", fontsize=12)

#     plt.tight_layout()

#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)

#     # Buffer de memória contendo a imagem
#     return buf


def vis_sinergy_graph(cards_sinergy, commander):

    def get_card_image_url(card_name):
        response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
        if response.status_code == 200:
            card_data = response.json()
            if 'image_uris' in card_data:
                return card_data['image_uris']['normal']
            else:
                return card_data['card_faces'][0]['image_uris']['normal'] if 'card_faces' in card_data else ""
        else:
            print(f"Erro ao obter imagem da carta {card_name}")
            return ""

    # Adiciona URLs de imagens às cartas com sinergia
    sinergies = []
    for card in cards_sinergy:
        card['image_url'] = get_card_image_url(card['name'])
        sinergies.append(card['synergy'])
    max_sinergy = max(sinergies)
    min_sinergy = min(sinergies)

    def normalize_sinergy(value, max=max_sinergy, min=min_sinergy):
        return ((value - min) / (max - min)) * (50-20)+20
    
    graph = nx.Graph()
    commander_image = get_card_image_url(commander)
    graph.add_node(commander, label=commander, color='red', size=60, image=commander_image, 
                   shape='image', physics=False, x=0, y=0)
    
    angle_step = 2 * math.pi / len(cards_sinergy)  
    angle = 0

    for card in cards_sinergy:
        x = (1 - card['synergy'])*600 * math.cos(angle)
        y = (1 - card['synergy'])*600 * math.sin(angle)
        graph.add_node(
            card['name'], 
            label=f"{card['name']} \n(synergy: {card['synergy']})", 
            size=normalize_sinergy(card['synergy']), 
            image=card['image_url'], 
            shape='image', 
            physics = False, 
            x=x, 
            y=y)
        graph.add_edge(commander, card['name'], weight=1)
        angle += angle_step

    net = Network(notebook=True, height="750px")

    net.from_nx(graph)
    net.show('synergy.html')


def vis_combos_graph(commander, deck_cards):
    
    edhrec = EDHRec()

    def load_image(url, alpha):
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        alpha_img = ImageEnhance.Brightness(img.split()[3]).enhance(alpha)
        img.putalpha(alpha_img)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"


    def get_card_image_url(card_name):
        response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
        if response.status_code == 200:
            card_data = response.json()
            if 'image_uris' in card_data:
                return card_data['image_uris']['normal']
            else:
                return card_data['card_faces'][0]['image_uris']['normal'] if 'card_faces' in card_data else ""
        else:
            print(f"Erro ao obter imagem da carta {card_name}")
            return ""

    def sanitize_card_name(card_name):
        return card_name.lower().replace(' ', '-').replace(',', '').replace("'", "").strip()
    
    def check_combos(deck, combos):
        sanitized_deck = {sanitize_card_name(card): card for card in deck}
        result = []
        for combo in combos['container']['json_dict']['cardlists']:
            combo_cards = [(card['name'], card['sanitized']) for card in combo['cardviews']]
            cards_in_deck = [original_name for original_name, sanitized_name in combo_cards if sanitized_name in sanitized_deck]
            cards_not_in_deck = [original_name for original_name, sanitized_name in combo_cards if sanitized_name not in sanitized_deck]
            result.append({
                'combo': combo['tag'],
                'cards': [original_name for original_name, sanitized_name in combo_cards],
                'cards_in_deck': cards_in_deck,
                'cards_not_in_deck': cards_not_in_deck
            })
        return result
    
    cmd_combos = edhrec.get_card_combos(commander)
    
    if commander not in deck_cards:
        deck_cards.append(commander)
    
    combo_results = check_combos(deck_cards, cmd_combos)

    G = nx.Graph()

    # Adiciona nós e arestas para cada combo
    for result in combo_results:
        for card in result['cards']:
            image_url = get_card_image_url(card)
            if card in result['cards_in_deck']:
                G.add_node(card, label=card, image=image_url, shape='image')
            else:
                img_base64 = load_image(image_url, 0.5)
                G.add_node(card, label=card, image=img_base64, shape='image')
            
            # Adiciona informações sobre o combo
            if 'title' in G.nodes[card]:
                G.nodes[card]['title'] += f"<br>{result['combo']}"
            else:
                G.nodes[card]['title'] = result['combo']

        # Adiciona arestas entre as cartas do combo
        for i in range(len(result['cards']) - 1):
            G.add_edge(result['cards'][i], result['cards'][i+1])

    # Cria o grafo interativo com a biblioteca pyvis
    net = Network(notebook=True, height='750px')
    net.from_nx(G)
    net.show('combos.html')

import requests

def vis_cards_without_sinergy(cards_without_sinergy, commander):
    # Lista de nomes a serem removidos
    names_to_remove = ['Island', 'Forest', 'Plains', 'Swamp', 'Mountain']
    
    # Remove o comandante da lista se estiver presente
    if commander in cards_without_sinergy:
        cards_without_sinergy.remove(commander)

    def get_card_image_url(card_name):
        response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
        if response.status_code == 200:
            card_data = response.json()
            if 'image_uris' in card_data:
                return card_data['image_uris']['small']
            else:
                return card_data['card_faces'][0]['image_uris']['small'] if 'card_faces' in card_data else ""
        else:
            print(f"Erro ao obter imagem da carta {card_name}")
            return ""

    # Filtra a lista removendo as cartas indesejadas
    filtered_deck_cards = [card for card in cards_without_sinergy if card not in names_to_remove]

    cards_without_sinergy_url = []

    for card in filtered_deck_cards:
        cards_without_sinergy_url.append({'name': card, 'image_url': get_card_image_url(card)})

    # html_content = '<h3>Cartas sem sinergia:</h3><div style="display: flex; flex-wrap: wrap;">'
    html_content = '<div style="display: flex; flex-wrap: wrap;">'

    
    count = 0
    for card in cards_without_sinergy_url:
        if count % 3 == 0 and count != 0:
            html_content += '</div><div style="display: flex; flex-wrap: wrap;">'
        html_content += '<div style="margin: 10px; text-align: center;">'
        html_content += f'<img src="{card["image_url"]}" alt="{card["name"]}" style="width: 150px;"/>'
        html_content += f'<p style="font-size: 11px;">{card["name"]}</p>'
        html_content += '</div>'
        count += 1
    html_content += '</div>'
    
    return html_content

