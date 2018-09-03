import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from src.make_plots import generate_timeline, generate_hist, generate_map, colors, month_map

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

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
                                            html.H5('Select Regions to Explore Below', style={'color': colors['text'],
                                                                                              'align': 'center'}),
                                            html.Div(
                                               dcc.Dropdown(id='region_select',
                                                            value=['Middle East'],
                                                            options=[{'label': c, 'value': c}
                                                                      for c in sorted(df['region'].unique())],
                                                            multi=True
                                                             ),
                                               )
                                            ],
                                        style={'align': 'center'}
                                        ),

                               html.Br(),
                               html.Br(),

                               html.Div(className='row',
                                        children=[
                                            html.Div(id='conflict_timeline_div',
                                                     className='col m12',
                                                     children=generate_timeline(df_days)),
                                            html.Br(),

                                        ]),

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
    [dash.dependencies.Input('conflict_type_hist', 'clickData'),
     dash.dependencies.Input('region_select', 'value'),
     dash.dependencies.Input('conflict_timeline', 'relayoutData')])
def update_map(event_selection, region_selection, time_selection):

    conflict_type = event_selection["points"][0]['text']

    if type(conflict_type) == list:
        if len(conflict_type) == df['event_type'].nunique():
            mapping_events = 'All Events'
        else:
            mapping_events = ", ".join(conflict_type)
        mask = [True if e in set(conflict_type) and r in region_selection
                else False for (e, r) in zip(df['event_type'], df['region'])]

    else:
        mapping_events = conflict_type
        mask = [True if e == conflict_type and r in set(region_selection)
                else False for (e, r) in zip(df['event_type'], df['region'])]

    # Mask for selected event types
    dff = df[mask]

    title = 'Mapping {}'.format(mapping_events)

    return generate_map(df=dff, colors=colors, title=title,
                        min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)


@app.callback(
    dash.dependencies.Output('conflict_type_hist_div', 'children'),
    [dash.dependencies.Input('region_select', 'value'),
     dash.dependencies.Input('conflict_timeline', 'relayoutData')])
def update_hist(region_selection, timeline_selection):
    try:
        start_date = timeline_selection['xaxis.range'][0]
        end_date = timeline_selection['xaxis.range'][1]

        mask = [True if r in set(region_selection) and d > start_date and d < end_date
                        else False
                       for (r, d) in zip(df['region'], df['event_date'])]
    except KeyError:
        mask = [True if r in set(region_selection)
                else False
                for r in df['region']]

    dff = df[mask]
    return generate_hist(df=dff)


@app.callback(
    dash.dependencies.Output('conflict_timeline_div', 'children'),
    [dash.dependencies.Input('region_select', 'value')])
def update_hist(region_selection):
    mask = [True if r in region_selection
            else False for r in df['region']]
    dff = df[mask].groupby(['event_date', 'event_type'], as_index=False).agg({'fatalities': ['count', 'sum']})
    return generate_timeline(df=dff)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=5000)
