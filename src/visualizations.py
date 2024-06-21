import plotly.graph_objects as go
import streamlit as st


def add_logo():
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

def vis_cmd_distribuition():
    pass

def vis_word_cloud():
    pass

def vis_edhrec_rank():
    pass

def vis_sinergy_graph():
    pass

def vis_histogram():
    pass