import io
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
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
    fig.update_layout(title='Quantidade de cartas lançadas por ano',
                    xaxis_title='Ano',
                    yaxis_title='Quantidade')
    return fig


def vis_cmd_distribuition(df):

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


def vis_edhrec_rank():
    pass

def vis_sinergy_graph():
    pass

def vis_histogram():
    pass