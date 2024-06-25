import io
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def add_logo():
    st.set_page_config(
        page_title="MTG - Uma análise sobre seu Deck",
        page_icon="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/microsoft/106/mage_1f9d9.png"
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
    fig.update_layout(title='Quantidade de Commandantes lançados por ano',
                    xaxis_title='Ano',
                    yaxis_title='Quantidade')
    return fig


def vis_distribuition(df):

    fig = px.histogram(df,
                    x='cmc',
                    title = ('Distribuição de Custo de Mana Convertido '
                             '(CMC) dos Comandantes'),
                    labels={'cmc':'CMC'},
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
                 title='<b>Predominâncias das Identidades dos Commandantes')

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
    df['main_type'] = df['type_line'].apply(split_types)
    df_exploded = df.explode('subtypes')
    rank_type_line = df_exploded['subtypes'].value_counts().sort_values(ascending=False)
    top_type_line = rank_type_line.head(10)
    # df['main_type'] = df['type_line'].apply(lambda x: x.split('—')[0].strip())
    # rank_type_line = df['main_type'].value_counts().sort_values(
    #     ascending=False)
    # top_type_line = rank_type_line.head(10)
    # df_filtered_type_line = df[df['main_type'].isin(top_type_line.index)]
    df_filtered_type_line = df_exploded[df_exploded['subtypes'].isin(top_type_line.index)]
    grouped_data = df_filtered_type_line.groupby('main_type')[
        'cmc'].agg(['mean', 'count']).reset_index()

    grouped_data.columns = ['main_type', 'cmc', 'TYPE_COUNT']
    mean_cmc = grouped_data.sort_values(by='cmc', ascending=False)

    mean_cmc['cmc'] = round(mean_cmc['cmc'], 2)

    fig1 = px.bar(top_type_line, x=top_type_line.index, y=top_type_line.values,
                  color=top_type_line.index, text=top_type_line.values,
                  labels={'main_type': 'Tipos de Criaturas dos Comandantes',
                          'y': 'Total'},
             template='seaborn',
             title='<b> Criaturas mais frequentes')
    fig1.update_layout(showlegend=False)
    fig1.update_yaxes(tickformat="000")

    fig2 = px.bar(mean_cmc, x='main_type', y='cmc',
                color='main_type',
                labels={'main_type': 'Tipos de Criaturas dos Comandantes',
                        'cmc': 'CMC MÉDIO'},
                text='TYPE_COUNT',
                template='seaborn',
                title='<b> CMC Médio por Tipo de Criatura')
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
                  title='<b> Frequência com que cada categoria de raridade aparece',
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


def vis_edhrec_rank(df):

    df = df[df['edhrec_rank'].notnull()]
    df = df.sort_values('edhrec_rank').head(10)

    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.flatten()

    for i, (index, row) in enumerate(df.iterrows()):
        img_url = row['image_uris.normal']
        if img_url:
            response = requests.get(img_url)
            img = Image.open(io.BytesIO(response.content))
            axes[i].imshow(img)
            axes[i].axis('off')
            axes[i].set_title(f"{row['name']} (Rank: {row['edhrec_rank']})", fontsize=12)
        else:
            axes[i].axis('off')
            axes[i].set_title(f"{row['name']} (Rank: {row['edhrec_rank']})\nImagem não disponível", fontsize=12)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Buffer de memória contendo a imagem
    return buf


def vis_sinergy_graph():
    pass

def vis_histogram():
    pass