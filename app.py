import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

app = dash.Dash()

df = pd.read_csv('data/world_conflict.csv', usecols=['longitude', 'latitude', 'region', 'admin1', 'location',
                                                     'event_type', 'fatalities', 'event_date'])

df = df.loc[:20000].copy()

df['event_type'] = ['Battle' if e[:6] == 'Battle' else e
                    for e in df['event_type']]

df['event_date'] = [datetime.strptime(d, "%d-%b-%y") for d in df['event_date']]
df_days = df.groupby(['event_date', 'event_type'], as_index=False).agg({'fatalities': ['count', 'sum']})

margin = 5

min_x = min(df['longitude']) - margin
max_x = max(df['longitude']) + margin

min_y = min(df['latitude']) - margin
max_y = max(df['latitude']) + margin

colors = {
    'background': '#F7F7F7',
    'text': '#37575B',
    'markers': '#ABC0C1',
    'event_types': {'Violence against civilians': '#810f7c',
                    'Riots/Protests': '#e0ecf4',
                    'Remote violence': '#8c96c6',
                    'Battle': '#8856a7'}
}


def generate_timeline(df):
    print(df.event_type.unique())
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


def generate_hist(df):
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
                            title='Conflict Event Types',
                            font={'color': colors['text']},
                            margin={'l': 200, 'b': 40, 't': 30, 'r': 10},
                            showlegend=False,
                            hovermode='closest'
                        )
                    }
                )


app.layout = html.Div(
    children=[
            html.Div(className='container-fluid',
                     children=[html.Br(),
                               html.H2('Visualizing Conflict', style={'color': colors['text']}),

                               html.Div(className='row',
                                        children=[
                                           html.Div(
                                               dcc.Dropdown(id='countries',
                                                            multi=True,
                                                            value=[''],
                                                            placeholder='Select Countries',
                                                            options=[{'label': c, 'value': c}
                                                                     for c in sorted(df['region'].unique())]
                                                            ),
                                               className='col s3 m3 l3 center-align',
                                               style={'font-size': '12px',
                                                      'color': colors['text']}),

                                           html.Br(),
                                           html.Br(),

                                           html.Div(id='conflict_timeline_div',
                                                    className='col s12',
                                                    children=generate_timeline(df_days))
                                    ]),

                               html.Br(),

                               html.Div(className='row', children=[
                                   html.Div(id='conflict_map_div', children='', className='col s12 m8 l8'),
                                   html.Div(id='conflict_type_hist_div',
                                            className='col s12 m4 l4',
                                            children=generate_hist(df))]),

                               ],
                     style={'width': '90%', 'margin-left': '5%', 'margin-right': '5%'}
                     )

            ],
    style={'backgroundColor': colors['background'], 'margin-top': '-30px', 'height': '2000px'})



@app.callback(
    dash.dependencies.Output('conflict_map_div', 'children'),
    [dash.dependencies.Input('conflict_type_hist', 'clickData')])
def update_map(clickData):

    conflict_type = clickData["points"][0]['text']

    if type(conflict_type) == list:
        if len(conflict_type) == df['event_type'].nunique():
            mapping_events = 'All Events'
        else:
            mapping_events = ", ".join(conflict_type)
        mask = [True if i in set(conflict_type) else False for i in list(df['event_type'])]

    else:
        mapping_events = conflict_type
        mask = [True if i == conflict_type else False for i in list(df['event_type'])]

    # Mask for selected event types
    dff = df[mask]

    title = 'Mapping {}'.format(mapping_events)

    return generate_map(df=dff, colors=colors, title=title,
                        min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()