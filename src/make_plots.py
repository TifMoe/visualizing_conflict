import plotly.graph_objs as go
import dash_core_components as dcc

colors = {
    'background': '#F7F7F7',
    'text': '#37575B',
    'markers': '#ABC0C1',
    'event_types': {'Violence against civilians': '#37575B',
                    'Riots/Protests': '#A7C4C2',
                    'Remote violence': '#F05D5E',
                    'Battle': '#C8AD55'}
}


def generate_timeline(df):
    return dcc.Graph(
                    id='conflict_timeline',
                    figure={
                        'data': [
                            go.Scatter(
                                x=df[df['event_type']==i]['event_date'],
                                y=df[df['event_type']==i]['fatalities']['sum'],
                                line=dict(color=colors['event_types'][i])
                            ) for i in df.event_type.unique()
                        ],
                        'layout': go.Layout(
                            plot_bgcolor=colors['background'],
                            paper_bgcolor=colors['background'],
                            height=350,
                            title='Fatalities per day',
                            font={'color': colors['text']},
                            margin={'l': 30, 'b': 30, 't': 30, 'r': 10},
                            showlegend=False,
                            hovermode='closest',
                            xaxis=dict(
                                    rangeselector=dict(
                                        buttons=list([
                                            dict(count=1,
                                                 label='1m',
                                                 step='month',
                                                 stepmode='backward'),
                                            dict(count=6,
                                                 label='6m',
                                                 step='month',
                                                 stepmode='backward'),
                                            dict(step='all')
                                        ])
                                    ),
                                    rangeslider=dict(
                                        visible=True
                                    ),
                                    type='date'
                                ))
                    }
                )


def generate_map(df, colors, title, min_x, max_x, min_y, max_y):
    return dcc.Graph(
                id='conflict_map',
                figure={'data': [go.Scattergeo(
                                    lon=df[df['event_type'] == i]['longitude'],
                                    lat=df[df['event_type'] == i]['latitude'],
                                    text=df[df['event_type'] == i]['event_type'],
                                    mode='markers',
                                    marker={
                                        'size': 10,
                                        'line': {'width': 0.3,
                                                 'color': colors['text']},
                                        'color': [colors['event_types'][e]
                                                  for e in df[df['event_type'] == i]['event_type']],
                                        'opacity':.5
                                    },
                                    name=i
                                ) for i in df.event_type.unique()
                                ],
                        'layout': go.Layout(
                                    geo=dict(
                                        showland=True,
                                        landcolor= 'white',
                                        countrycolor=colors['text'],
                                        showsubunits=True,
                                        subunitcolor=colors['background'],
                                        subunitwidth=5,
                                        showcountries=True,
                                        oceancolor=colors['background'],
                                        showocean=True,
                                        showcoastlines=True,
                                        showframe=False,
                                        coastlinecolor=colors['text'],
                                        lonaxis={'range': [min_x, max_x]},
                                        lataxis={'range': [min_y, max_y]},
                                        resolution=50),
                                    xaxis={'title': 'Longitude', 'range': [min_x, max_x]},
                                    yaxis=dict(scaleanchor="x", scaleratio=1, range=[min_y, max_y]),
                                    title=title,
                                    plot_bgcolor=colors['background'],
                                    paper_bgcolor=colors['background'],
                                    autosize=True,
                                    font={'color': colors['text']},
                                    margin={'l': 10, 'b': 10, 't': 30, 'r': 10},
                                    showlegend=False,
                                    hovermode='closest'
                                )
                        }
                )


def generate_hist(df, title='Conflict Event Types'):
    return dcc.Graph(
                    id='conflict_type_hist',
                    clickData={'points': [{'text': list(colors['event_types'].keys())}]},
                    figure={
                        'data': [
                            go.Histogram(
                                y=df[df['event_type'] == i]['event_type'],
                                text=df[df['event_type'] == i]['event_type'],
                                name=i,
                                marker=dict(
                                            color=[colors['event_types'][e]
                                                   for e in df[df['event_type'] == i]['event_type']],
                                            line={'width': 0.5,
                                                  'color': colors['text']},
                                            opacity=.7
                                            )
                            ) for i in df.event_type.unique()
                        ],
                        'layout': go.Layout(
                            plot_bgcolor=colors['background'],
                            paper_bgcolor=colors['background'],
                            autosize=True,
                            title=title,
                            font={'color': colors['text']},
                            margin={'l': 200, 'b': 40, 't': 30, 'r': 10},
                            showlegend=False,
                            hovermode='closest'
                        )
                    }
                )
