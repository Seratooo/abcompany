from dash import html, dcc, callback, Output, Input, dash_table
from data.configs import getDatabase
from ydata_profiling import ProfileReport
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import json
import re

df = getDatabase().sample(500).iloc[:,:5]
profile = ProfileReport(df, title="Relatório")
json_data = profile.to_json()
report = json.loads(json_data)


AED = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Análise Exploratória Dos Dados', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Aqui você poderá analisar aspectos estatísticos e insights dos seus conjuntos de dados', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
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

@callback(
    Output('estatisticas-container', 'children'),
    [Input('estatisticas-container', 'id')]
)
def update_statistics(_):
    # Calcular as estatísticas do dataset
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


def get_variable_types(report):
    return report['table']['types']

@callback(
    Output('variable-types-container', 'children'),
    [Input('variable-types-container', 'id')]
)
def update_variable_types(_):
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



def get_alerts(report):
    alerts = report['alerts']
    padrao = r'\[(.*?)\]'
    elements = {}
    for alert in alerts:
        elements.setdefault(re.findall(padrao, alert)[0], re.findall(padrao, alert)[1])
    
    return elements

@callback(
    Output('alerts-container', 'children'),
    [Input('alerts-container', 'id')]
)
def update_alerts(_):
    alerts_container = get_alerts(report)
    alerts_container_html = []
    alerts_container_html.append(html.P("Alertas"))
    Main_div = []
    for type, value in alerts_container.items():
        element = html.Div([
            html.P(f'{type} está altamente correlacionado com '), 
            html.P(f'{value}')
        ])
        Main_div.append(element)

    alerts_container_html.append(html.Div(Main_div))
    return alerts_container_html




def get_variables(report):
    return report['variables']

def get_histogram_data(variablesName):
    histogram_data = get_variables(report)[variablesName]['histogram']
    return histogram_data

def get_variables_data_byName(name):
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

@callback(
    Output('variables-select', 'data'),
    Output('variables-select', 'value'),
    [Input('variables-container', 'id')]
)
def variables_alerts(_):
  variables_select = []
  variables_value = ''
  for variable in get_variables(report):
      variables_value = variable
      variables_select.append({"value": f"{variable}", "label": f"{variable}"})
  return variables_select, variables_value


@callback(
    Output('variables-output', 'children'),
    [Input('variables-select', 'value')]
)
def variables_output(variable):
  variables_HTML = []
  variables_data = get_variables_data_byName(variable)

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
