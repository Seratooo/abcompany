from api.clientApp import GetAllCollectionNames, GetCollectionByName
from dash import dcc, callback, Output, Input, State, html, Dash, dash_table, clientside_callback
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd

names = GetAllCollectionNames()
DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = DatasetsNames[0]

analyzeFiles = html.Div([
    dcc.Store(id='datasets-names-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Analisar arquivos', className='PainelStyle'),
                    html.Div([
                        html.P('Analise um ficheiro contendo os seus dados ou junte varios ficheiros em um só', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
        html.Div([
            dmc.Select(
                        label="",
                        placeholder="Selecione um conjunto",
                        id="dataset-select",
                        value=f"{PanelMultiSelectOptions}",
                        data=[],
                        style={"width": 200, "marginBottom": 10},
                    ),
            dcc.Loading(children=[
                html.Div( id="dataset-display", style={"width":"100%","minHeight":"55vh"}),
            ], color="#2B454E", type="dot", fullscreen=False,),
        ], style={"padding":"20px"}),
])

@callback(Output('dataset-select', 'value'),
          Output('dataset-select', 'data'),
                Input('dataset-select', 'id'),
              )
def SetDataValuesOnCompont(_):
    value = PanelMultiSelectOptions
    return value, DatasetValues()[1]

def DatasetValues():
    data = []
    for name in DatasetsNames:
        data.append({"value": f"{name}", "label": f"{name.split('-')[0]}"})
    return DatasetsNames, data

@callback(
    Output('dataset-display', 'children'),
    Input("dataset-select", "value")
)
def getGraph(value):
    data = GetCollectionByName(value)

    if not data.empty:
        df = data
        df.drop('_id', axis=1, inplace=True)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.drop('Unnamed: 0.1', axis=1, inplace=True)
        
        # Criar um gráfico com base nos dados do DataFrame
        histograms = []
        for col in df.columns:
            trace = go.Histogram(x=df[col], name=col)
            histograms.append(trace)

        layout = go.Layout(
            title='Distribuição de Variáveis',
            barmode='overlay',
            xaxis=dict(title='Valores'),
            yaxis=dict(title='Frequência')
        )

        figure = go.Figure(data=histograms, layout=layout)

        # Exibir o gráfico
        graph = dcc.Graph(figure=figure)

        #Exibir a tabela
        table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        fixed_rows={'headers': True},
        style_data={'fontSize': '1.2rem'},
        sort_action='native',
        )
        return [graph, table]

