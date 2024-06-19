import plotly.graph_objects as go


def vis_commander_by_released_date(df_commander_cards):
    df_commander_cards['released_year'] = df_commander_cards['released_at'].str[:4]
    commander_by_released_date = df_commander_cards.groupby('released_year').size()
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