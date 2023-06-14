from contextlib import nullcontext
from dash import html, dcc, callback, Output, Input, State, dash_table
import plotly.graph_objects as go
import dash_mantine_components as dmc
import base64
import datetime
import io
import pandas as pd
from dash_iconify import DashIconify
from datetime import datetime
from api import clientApp

upload = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Carregar ficheiro', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Carregue um ficheiro execel contendo os seus dados para análise', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
         
        html.Div([
        dmc.TextInput(label="Nome do conjunto de dados:", id="lb_dataset"),
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arraste e Solte ou ',
            html.A('Selecione Arquivos', style={"font":"1.8rem Nunito", "color":"#000", "fontWeight":"700"})
        ], style={"font":"1.8rem Nunito", "color":"#000","marginTop":"15px"}),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            "display":"flex",
            "justifyContent":"center",
            "display":"flex",
            "justifyContent":"center",
            "alginItems":"center",
            "cursor":"pointer",
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
        dmc.Button(
            "Guardar dataset",
            id="save-button",
            leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
        ),
        html.Div(id='output-data-upload'), 
        html.Div(id='data-output'), 
        ], id="upload-elements", style={"position":"absolute"}),
        dcc.Loading(children=(html.Div(id='data-output2')), color="#2B454E", type="dot", fullscreen=False,),   
         
], style={"width":"100%","height":"100vh","position":"relative","zIndex":"2"})


D_NAME = ''
PD_CSV = pd.DataFrame()
global LIST_CSV
LIST_CSV = []

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    global PD_CSV
    global LIST_CSV
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            PD_CSV = df 
            LIST_CSV.append(PD_CSV)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            PD_CSV = df 
            LIST_CSV.append(PD_CSV)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename, style={"font":"1.2rem Nunito"}),
        html.H6(datetime.fromtimestamp(date), style={"font":"1.2rem Nunito"}),

        # dash_table.DataTable(
        #     df.to_dict('records'),
        #     [{'name': i, 'id': i} for i in df.columns]
        # ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content', style={"font":"1.2rem Nunito"}),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all',
        #     "font":"1.2rem Nunito"
        # })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    

@callback(Output('data-output', 'children'),
        Input('lb_dataset','value'))
def getDataSetName(value):
    global D_NAME
    D_NAME = value


@callback(Output('data-output2', 'className'),
          Input('save-button','n_clicks'),
          )
def loadPopUp(n_clicks):
    if n_clicks is not None:
        return 'on'
    else:
        return ''

@callback(Output('data-output2', 'children'),
          Input('save-button','n_clicks'))
def saveDataSet(n_clicks):
    global LIST_CSV
    if n_clicks:
        if((PD_CSV.empty == False) and D_NAME):
            if all(col in PD_CSV.columns for col in ['Date', 'Sales', 'Customers', 'DayOfWeek', 'Year', 'Month', 'Day']):
                today = str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
                name = f'{D_NAME}-{today}'
                for index, df_csv in enumerate(LIST_CSV):
                    clientApp.CreateCollection(f'{name}-{index}', df_csv)
                LIST_CSV = []
                return [html.P(f"Dados {name} carregados na base de dados!", className="desc-popup"),  html.Button('OK', id='btn-popup')]
            return [html.P(f"Seu conjunto de dados precisa conter tabelas específicar com os seguintes nome: Date, Sales, Customers, DayOfWeek, Year, Month, Day", className="desc-popup"),  html.Button('OK', id='btn-popup')]
        elif(PD_CSV.empty == True):
            return [ html.P('Selecione um conjunto de dados!', className="desc-popup"), html.Button('OK', id='btn-popup')]
        else:
            return [ html.P('Digite um nome para de dados!', className="desc-popup"), html.Button('OK', id='btn-popup')]
    

@callback(Output('data-output2', 'className', allow_duplicate=True),
          Input('btn-popup','n_clicks'),
          State('data-output2', 'className'),
          prevent_initial_call='initial_duplicate'
          )
def loadPopUp(n_clicks, className):
    if n_clicks is not None and className == 'on':
        return ''
    else:
        return 'on'