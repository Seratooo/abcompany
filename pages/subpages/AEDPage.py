from dash import html, dcc, callback, Output, Input, dash_table
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from data.configs import getDatabase
from ydata_profiling import ProfileReport
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import re
from googletrans import Translator


translator = Translator()
DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = DatasetsNames[0]


AED = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-sales-aed-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Análise Exploratória Dos Dados', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.Div([
                            html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                            dmc.Select(
                            label="",
                            placeholder="Select all you like!",
                            id="paneleAed-dataset-multi-select",
                            value=PanelMultiSelectOptions,
                            data=[
                                {"value": "react", "label": "React"},
                                {"value": "ng", "label": "data 2015-2020"},
                                {"value": "svelte", "label": "Svelte"},
                                {"value": "vue", "label": "data 2020 - 2022"},
                            ],
                            style={"width": 400, "marginBottom": 10,"fontSize":"1.2rem"},
                            ),
                        ]),
                        html.Div([
                            html.P('Aqui você poderá analisar aspectos estatísticos e insights dos seus conjuntos de dados', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        ])
                    ], style={"display":"flex", "justifyContent":"space-between", "width":"100%"}),
                    
                ])
            , style={"widht":"100%"})
        ],className='aed-page-class' , style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem", "width":"100%"}),
        html.Div([
          html.Div([
              html.Div(id='estatisticas-container', style={"width":"72%"}),
              html.Div([
                html.Div(id='variable-types-container', style={"height":"50%"}),
                html.Div(id='alerts-container', style={"height":"50%"}),
              ], style={"width":"38%", "display":"flex","flexDirection":"column","justifyContent":"space-between"}),
          ], style={"display":"flex"}),
          

          html.Div([
             html.P("Variáveis"),
             dmc.Select(
                placeholder="Selecione uma",
                id="variables-select",
                value="",
                data=[ ],
                style={"width": 200, "marginBottom": 10},
            ),
            html.Div(id='variables-output'),
          ],id='variables-container')
        ], id="report")
], id='aed-container')




#Carregar dados do select

@callback(Output('paneleAed-dataset-multi-select', 'value'),
          Output('paneleAed-dataset-multi-select', 'data'),
                Input('interval_db', 'n_intervals'),
              )
def SetDataValuesOnCompont(interval_db):
    value = PanelMultiSelectOptions
    return value, DatasetValues()[1]

def DatasetValues():
    data = []
    for name in DatasetsNames:
        data.append({"value": f"{name}", "label": f"{name.split('-')[0]}"})
    return DatasetsNames, data

@callback(
    Output('dataset-sales-aed-storage', 'data', allow_duplicate=True),
    Input("paneleAed-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions

#Carregar dados do select

######----- Funcoes Estatísticas ---######
def get_estatistics_dataset(report):
    # Retornar as estatísticas calculadas
    data = report['table']
    return {
        'Número de Variáveis': data['n_var'],
        'Número de Observações': data['n'],
        'Células Ausentes': data['n_cells_missing'],
        'Tamanho Total na Memória': data['memory_size'],
        'Tamanho Médio da Linha na Memória': data['record_size'],
        'Linhas duplicadas': data['n_duplicates'],
        'Linhas duplicadas (%)': data['p_duplicates']
    }

def get_variable_types(report):
    return report['table']['types']

def get_alerts(report):
    alerts = report['alerts']
    frases_traduzidas = []
    for alert in alerts:
        traducao = translator.translate(alert, dest='pt')
        frases_traduzidas.append(traducao.text)
    return frases_traduzidas

def get_histogram_data(variablesName):
    histogram_data = get_variables(report)[variablesName]['histogram']
    return histogram_data

def get_variables_data_byName(name, report):
    variable = get_variables(report)[name]

    return {
        'Tipo da Variável': variable['type'],
        'Nº de elementos': variable['n'],
        'Nº de elementos distintos': variable['n_distinct'],
        'Nº de elementos distintos (%)': variable['p_distinct'],
        'Valores ausentes': variable['n_missing'],
        'Valores ausentes (%)': variable['p_missing'],
        'Infinitos': variable['n_infinite'] if variable['n_infinite'] else '',
        'Infinitos (%)': variable['p_infinite'],
        'Média': variable['mean'],
        'Mínimo': variable['min'],
        'Máximo': variable['max'],
        'Zeros': variable['n_zeros'],
        'Zeros (%)': variable['p_zeros'],
        'Valores negativos': variable['n_negative'],
        'Valores negativos (%)': variable['p_negative'],
        'Variança': variable['variance'],
        'Desvio padrão': variable['std'],
        'Coeficiente de variação': variable['cv'],
        'Curtose': variable['kurtosis'],
        '5º percentil': variable['5%'],
        'Q1': variable['25%'],
        'Mediana': variable['50%'],
        'Q3': variable['75%'],
        'Percentil 95': variable['95%'],
        'Intervalo interquartílico (IQR)': variable['iqr'],
        'Distorção': variable['skewness'],
        'Soma': variable['sum'],
        'Aumento monotônico': 'verdadeiro' if variable['monotonic_increase'] else 'falso',
        'Diminuição monotônica':  'verdadeiro' if variable['monotonic_decrease'] else 'falso',
        'Desvio absoluto mediano (MAD)': variable['mad'],
        'Valores Únicos': variable['n_unique'],
        'Valores Únicos (%)': variable['p_unique'],

    }

def get_variables(report):
    return report['variables']

######----- Funcoes Estatísticas ---######


######----- CallBakcs Estatísticas ---######

@callback(
    Output('estatisticas-container', 'children'),
    [Input('estatisticas-container', 'id'),
     Input("paneleAed-dataset-multi-select", "value")]
)
def update_statistics(_, value):
    # Calcular as estatísticas do dataset
    report = getJson(value) 
    estatisticas = get_estatistics_dataset(report)

    # Criar uma lista de elementos HTML para exibir as estatísticas
    estatisticas_html = []
    estatisticas_html.append(html.P('Estatísticas do conjunto de dados'))
    for chave, valor in estatisticas.items():
        element = html.Div([
            html.P(f'{chave}:'), 
            html.P(f'{valor}')
        ])
        estatisticas_html.append(element)

    return estatisticas_html

@callback(
    Output('variable-types-container', 'children'),
    [Input('variable-types-container', 'id'),
     Input("paneleAed-dataset-multi-select", "value")]
)
def update_variable_types(_, value):
    report = getJson(value) 
    variable_types = get_variable_types(report)
    variable_types_html = []
    variable_types_html.append(html.P("Tipo de Variáveis"))
    Main_div = []
    for type, value in variable_types.items():
        element = html.Div([
            html.P(f'{type}:'), 
            html.P(f'{value}')
        ])
        Main_div.append(element)

    variable_types_html.append(html.Div(Main_div))
    return variable_types_html

@callback(
    Output('alerts-container', 'children'),
    [Input('alerts-container', 'id'),
     Input("paneleAed-dataset-multi-select", "value")]
)
def update_alerts(_, value):
    report = getJson(value) 
    alerts_container = get_alerts(report)
    alerts_container_html = []
    alerts_container_html.append(html.P("Alertas"))
    Main_div = []
    for value in alerts_container:
        element = html.Div([
            html.P(f'{value}')
        ])
        Main_div.append(element)

    alerts_container_html.append(html.Div(Main_div))
    return alerts_container_html

@callback(
    Output('variables-select', 'data'),
    Output('variables-select', 'value'),
    [Input('variables-container', 'id'),
     Input("paneleAed-dataset-multi-select", "value")]
)
def variables_alerts(_, value):
  report = getJson(value) 
  variables_select = []
  variables_value = ''
  for variable in get_variables(report):
      variables_value = variable
      variables_select.append({"value": f"{variable}", "label": f"{variable}"})
  return variables_select, variables_value

@callback(
    Output('variables-output', 'children'),
    [Input('variables-select', 'value'),
     Input("paneleAed-dataset-multi-select", "value")]
)
def variables_output(variable, value):
  df = getColections([value])
  report = getJson(value) 
  variables_HTML = []
  variables_data = get_variables_data_byName(variable, report)

  fig = px.histogram(df[variable], x=variable, nbins=50)

  variables_HTML.append(html.Div([
      html.H3(variable),
      html.P(f"Tipo da Variável: {variables_data.get('Tipo da Variável')}")
  ]))

  first_table = []
  second_table = []

  index = 0
  for type,value in variables_data.items():
      index = index + 1
      if(index<14):
          element = html.Div([
              html.P(type),
              html.P(value)
            ], className='table-row')
          first_table.append(element)
      else:
          element2 = html.Div([
              html.P(type),
              html.P(value)
            ], className='table-row')
          second_table.append(element2)

  variables_HTML.append(html.Div([
       html.Div(first_table, id='first_table'),
       dcc.Graph(
        id='histogram-graph',
        figure=fig
       ),
   ], className='container-first_table'))       


  Tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Mais detalhes", value="datails"),
                dmc.Tab("Distribuição", value="distribution"),
            ]
        ),
        dmc.TabsPanel(html.Div(second_table, id='second_table'), value="datails"),
        dmc.TabsPanel(dcc.Graph(
            id='histogram-graph2',
            figure=fig
            ), value="distribution"
          ),
    ],
    color="green",
    #orientation="horizontal",
  )

  variables_HTML.append(
      Tabs,
  )

  return variables_HTML


######----- CallBakcs Estatísticas ---######

### --- Funções Auxiliares --- ####
def getJson(name):
    caminho_arquivo = f'json/{name}.json'
    with open(caminho_arquivo) as arquivo_json:
        dados_json = json.load(arquivo_json)
    return dados_json

def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    
    return df_PD

### --- Funções Auxiliares --- ####