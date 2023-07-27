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


DatasetsNames = GetAllCollectionNames()

def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    
    return df_PD

for dfName in DatasetsNames:
    if not os.path.exists(f"json/{dfName.replace(':','')}.json"):
        df = getColections([dfName])
        df.drop('_id', axis=1, inplace=True)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        profile = ProfileReport(df, title=f"Relatório: {dfName}")
        profile.to_json()
        profile.to_file(f"json/{dfName.replace(':','')}.json")

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, update_title='Carregando...')
server = app.server
app.layout = html.Div([
    # abcompany.ExampleComponent(id='component'),
    # html.H1(children='Test for ABCompany', style={'textAlign':'center'}),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
     dcc.Store(id='externarFactors', data={
                 'holiday': ['2021', '2022'],
                 'weather': ['2021', '2022'],
                 'inflation': ['2021', '2022']
     }),
     dcc.Store(id='User', data={}, storage_type='local'),
     dash.page_container,
    #  dcc.Loading(children=[dash.page_container], color="#119DFF", type="dot", fullscreen=True,),
    #  dmc.Loader(color="green", size="xl", variant="oval", style={"position":"absolute","top":"50%","left":"60%", "zIndex":"1"})
], style={
    'background':'#F0F0F0',
    'margin': '0',
    'padding': '0',
    'boxSizing': 'border-box',
    'height': '100vh',
    'overflow': 'hidden',
    }) 

if __name__ == '__main__':
    app.run_server(debug=True)
