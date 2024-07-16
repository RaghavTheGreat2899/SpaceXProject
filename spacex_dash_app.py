# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),
    
    # Pie chart for success counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Range slider for payload selection
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0 kg', 10000: '10000 kg'},
        value=[min_payload, max_payload]
    ),
    
    html.Br(),
    
    # Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Callback function to update pie chart based on selected launch site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Success vs Failure for All Launch Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failure for {selected_site}')
    return fig

# TASK 4:
# Callback function to update scatter plot based on selected launch site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs Success for All Sites | Payload Range: {payload_range[0]} kg - {payload_range[1]} kg',
                         hover_name='Launch Site')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs Success for {selected_site} | Payload Range: {payload_range[0]} kg - {payload_range[1]} kg',
                         hover_name='Booster Version Category')
    
    fig.update_layout(xaxis_title='Payload Mass (kg)', yaxis_title='Success (1) / Failure (0)')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
