# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import logging

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites=['ALL']
launch_sites.extend(list(spacex_df['Launch Site'].unique()))
logging.info(list(spacex_df['Launch Site'].unique()))

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': i, 'value': i} for i in launch_sites],
                                    value='ALL',
                                    placeholder="Site select dropdown",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', figure='')),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-bar-chart', figure='')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min_payload, max_payload, value=[0, 10000], id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', figure='')),
                                html.Br(),
                                html.Div(dcc.Graph(id='booster-success-chart', figure=px.bar(data_frame=spacex_df.groupby('Booster Version Category')['class'].mean().reset_index(), x='Booster Version Category', y='class')))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'), Output(component_id='success-bar-chart', component_property='figure')], Input(component_id='site-dropdown', component_property='value'))
def site_graphs(site_selected):
    if site_selected == 'ALL':
        spacex_site_success = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        spacex_site_success_rate = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        return px.pie(data_frame = spacex_site_success, names='Launch Site', values='class'), px.bar(data_frame = spacex_site_success_rate, x='Launch Site', y='class')
    else:
        spacex_st_success = spacex_df[spacex_df['Launch Site']==site_selected].groupby('Launch Site')['class'].sum().reset_index()
        spacex_st_success_rate = spacex_df[spacex_df['Launch Site']==site_selected].groupby('class')['Launch Site'].count().reset_index()
        spacex_st_success_rate['class'] = spacex_st_success_rate['class'].astype(str)
        return px.pie(data_frame = spacex_df[spacex_df['Launch Site']==site_selected], names='class'), px.bar(data_frame = spacex_st_success_rate, x='class', y='Launch Site')



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def payload_graphs(site_selected, payload_value_range):
    if site_selected == 'ALL':
        if payload_value_range is not None:
            return px.scatter(data_frame = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_value_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_value_range[1])], x='Payload Mass (kg)', y='class', color='Booster Version Category')
        else:
            #spacex_site_success = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
            #spacex_site_success_rate = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
            return px.scatter(data_frame = spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        spacex_st_success = spacex_df[spacex_df['Launch Site']==site_selected]
        if payload_value_range is not None:
            return px.scatter(data_frame = spacex_st_success[(spacex_st_success['Payload Mass (kg)'] >= payload_value_range[0]) & (spacex_st_success['Payload Mass (kg)'] <= payload_value_range[1])], x='Payload Mass (kg)', y='class', color='Booster Version Category')
        else:
        #spacex_st_success_rate = spacex_df[spacex_df['Launch Site']==site_selected].groupby('Launch Site')['class'].mean().reset_index()
            return px.scatter(data_frame = spacex_st_success, x='Payload Mass (kg)', y='class', color='Booster Version Category')

# Run the app
if __name__ == '__main__':
    app.run()
