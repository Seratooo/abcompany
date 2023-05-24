import abcompany
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
import os
import sys

sys.path.append("pages")
sys.path.append("data")
sys.path.append("api")



app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    # abcompany.ExampleComponent(id='component'),
    # html.H1(children='Test for ABCompany', style={'textAlign':'center'}),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # dcc.Graph(id='graph-content'),
     dash.page_container,
     dmc.Loader(color="green", size="xl", variant="oval", style={"position":"absolute","top":"50%","left":"60%", "zIndex":"1"})
], style={
    'background':'#F0F0F0',
    'margin': '-8px',
    'padding': '0',
    'boxSizing': 'border-box',
    'height': '100vh',
    'overflow': 'hidden',
    }) 

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run_server(debug=True)
