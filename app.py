import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from src.make_plots import generate_timeline, generate_hist, generate_map, colors

app = dash.Dash()

df = pd.read_csv('data/world_conflict.csv')
df = df.loc[:20000].copy()  # Limit data until performance optimization

# Create df aggregated by date for timeline
df_days = df.groupby(['event_date', 'event_type'], as_index=False).agg({'fatalities': ['count', 'sum']})

margin = 5

min_x = min(df['longitude']) - margin
max_x = max(df['longitude']) + margin
min_y = min(df['latitude']) - margin
max_y = max(df['latitude']) + margin


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
    app.run_server(host='0.0.0.0',
                   port=5000)
