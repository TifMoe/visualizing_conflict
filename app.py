import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv('data/world_conflict.csv', usecols=['longitude', 'latitude', 'region',
                                                     'event_type', 'fatalities', 'event_date'])
margin = 5

min_x = min(df['longitude']) - margin
max_x = max(df['longitude']) + margin

min_y = min(df['latitude']) - margin
max_y = max(df['latitude']) + margin

colors = {
    'background': '#F7F7F7',
    'text': '#37575B',
    'markers': '#ABC0C1'
}


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
                                        'color': colors['markers'],
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
                    clickData={'points': [{'text': 'Remote violence'}]},
                    figure={
                        'data': [
                            go.Histogram(
                                y=df[df['event_type'] == i]['event_type'],
                                text=df[df['event_type'] == i]['event_type'],
                                name=i,
                                marker=dict(
                                            color=colors['markers'],
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
                            margin={'l': 300, 'b': 40, 't': 30, 'r': 10},
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
                               html.Div(
                                   dcc.Dropdown(id='countries',
                                                multi=True,
                                                value=[''],
                                                placeholder='Select Countries',
                                                options=[{'label': c, 'value': c}
                                                         for c in sorted(df['region'].unique())]
                                                ),
                                   style={'width': '25%', 'margin-left': '5%', 'background-color': 'white',
                                          'font-size': '12px', 'color': colors['text']}),
                               html.Br(),
                               html.Br()
                               ],
                     style={'width': '90%', 'margin-left': '5%', 'margin-right': '5%'}),

            html.Div(className='row', children=[
                 html.Div(id='conflict_map_div', children='', className='col s12 m6 l6'),
                 html.Div(id='conflict_type_hist_div',
                          className='col s12 m6 l6',
                          children=generate_hist(df))]),

                ],
    style={'backgroundColor': colors['background'], 'margin-top':'-30px', 'height':'2000px'}
    )


@app.callback(
    dash.dependencies.Output('conflict_map_div', 'children'),
    [dash.dependencies.Input('conflict_type_hist', 'clickData')])
def update_map(clickData):
    try:
        conflict_type = [clickData["points"][0]['text']]
        mapping_events = ", ".join(conflict_type)
    except TypeError:
        conflict_type = list(df.event_type.unique())
        mapping_events = 'All Events'

    # Mask for selected event types
    mask = [True if i in set(conflict_type) else False for i in list(df['event_type'])]
    dff = df[mask]

    title = 'Mapping {}'.format(mapping_events)

    return generate_map(df=dff, colors=colors, title=title,
                        min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()