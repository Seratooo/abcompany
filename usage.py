import json
from ydata_profiling import ProfileReport
import abcompany
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
import os
import sys
from api.clientApp import GetAllCollectionNames, GetCollectionByName

sys.path.append("pages")
sys.path.append("data")
sys.path.append("api")


# DatasetsNames = GetAllCollectionNames()

# def getColections(Names):
#     df_PD = pd.DataFrame()
#     for name in Names:
#         df_PD =pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    
#     return df_PD

# for dfName in DatasetsNames:
#     df = getColections([dfName])
#     df.drop('_id', axis=1, inplace=True)
#     df.drop('Unnamed: 0', axis=1, inplace=True)
#     profile = ProfileReport(df, title=f"Relatório: {dfName}")
#     profile.to_json()
#     profile.to_file(f"json/{dfName}.json")

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, update_title='Carregando...')
server = app.server

app.layout = html.Div([
    # abcompany.ExampleComponent(id='component'),
    # html.H1(children='Test for ABCompany', style={'textAlign':'center'}),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # dcc.Graph(id='graph-content'),
     dcc.Store(id='externarFactors', data={
                 'holiday': ['2013', '2014', '2015'],
                 'weather': ['2013', '2014', '2015'],
                 'inflation': ['2013', '2014', '2015']
     }),
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
