from dash import html
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from dash import dcc, callback, Output, Input, State, clientside_callback
from dash import Dash, dash_table
from collections import OrderedDict
import pandas as pd

names = GetAllCollectionNames()
analyzeFiles = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Analisar arquivos', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Analise um ficheiro contendo os seus dados ou junte varios ficheiros em um só', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    html.Div(
    id="datasets-names",
    style={"display":"flex", "gap":"10px", "alignItems":"center", "paddingLeft":"3rem"}),
    html.Div( id="dataset-display", style={"background":"#c4c4c4","width":"30rem","height":"76vh"})
], style={"display":"flex", "gap":"10px", "justifyContent":"space-between","alignItems":"center", "height":"76vh", "background":"#F0F0F0"}),
])


@callback(Output('datasets-names', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def datasetsLoads(n_intervals):
   elements = []
   for name in names:
       elements.append(html.P(f"{name}",id=name,n_clicks=0,style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}))
   return elements

for name in names:
        @callback(Output('dataset-display', component_property='children', allow_duplicate=True ),
                    Input(name, component_property='n_clicks'),
                    Input(name, component_property='children'),
                    prevent_initial_call=True
                    )
        def datasetDisplay(n_clicks, children):
            return GetTableByCollectionName(children)
        
        # clientside_callback(
        #     """
        #     function(n_clicks, children) {
        #         return children;
        #     }
        #     """,
        #     Output('dataset-display', 'children', allow_duplicate=True),
        #     Input(name, 'n_clicks'),
        #     Input(name, 'children'),
        #     prevent_initial_call=True
        # )


def GetTableByCollectionName(Name):
     data = GetCollectionByName(Name)

     df = pd.DataFrame(data)
     if(df.empty == False):
        df['_id'] = df['_id'].astype(str)
        print(df.shape)
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' },
        )
        return table
     else:
          return ''