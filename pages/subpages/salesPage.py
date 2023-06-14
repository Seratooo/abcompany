from dash import html, dcc, callback, Output, Input, State
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from data.configs import getDatabase
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
import pandas as pd

DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]

sales = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-sales-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Painel de Vendas', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        dmc.MultiSelect(
                        label="",
                        placeholder="Select all you like!",
                        id="panelSales-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[
                            {"value": "react", "label": "React"},
                            {"value": "ng", "label": "data 2015-2020"},
                            {"value": "svelte", "label": "Svelte"},
                            {"value": "vue", "label": "data 2020 - 2022"},
                        ],
                        style={"width": 400, "marginBottom": 10,"fontSize":"1.2rem"},
                        ),
                    ])
                ])
            ),
            html.Div(
            dmc.Button("Criar relatório", style={"background":"#fff", "color":"#000","font":"3.2rem Nunito","marginTop":"1.2rem"}),
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
        dcc.Loading(children=[
            html.Div([
                html.Div([dcc.Graph(id='graph7', className='dbc')], style={"width":"47%"}),
                html.Div([dcc.Graph(id='graph8', className='dbc')], style={"width":"47%"}),
            ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        ], color="#2B454E", type="dot", fullscreen=False,),
        html.Div([
            html.Div([
                dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="sales-select",
                    value="Day",
                    data=[
                        {"value": "Month", "label": "Mês"},
                        {"value": "Year", "label": "Ano"},
                        {"value": "DayOfWeek", "label": "Semana"},
                        {"value": "Day", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Loading(children=[dcc.Graph(id='graph9', className='dbc'),], color="#2B454E", type="dot", fullscreen=False,),
            ], style={"width":"47%"}),
            html.Div([
                 dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="customers-select",
                    value="Day",
                    data=[
                        {"value": "Month", "label": "Mês"},
                        {"value": "Year", "label": "Ano"},
                        {"value": "DayOfWeek", "label": "Semana"},
                        {"value": "Day", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Loading(children=[dcc.Graph(id='graph10', className='dbc'),], color="#2B454E", type="dot", fullscreen=False,),
            ], style={"width":"47%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        
], style={"width":"100%","height":"140%"})



@callback(
          Output("graph7", "figure"),
          Output("graph8", "figure"),
          Input("panelSales-dataset-multi-select", "value")
          )
def select_value(value):
    sales_train_all_df = getColections(value)

    d7 = sales_train_all_df[sales_train_all_df['Customers']>0]
    fig7 = go.Figure()
    fig7.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Clientes Alcançados</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d7['Year'].min()} - {d7['Year'].max()}</span>"},
            value = (d7['Customers'].sum()),
            number = {'suffix': ""}
    ))

    d8 = sales_train_all_df
    fig8 = go.Figure()
    fig8.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Receitas Vendidas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d8['Year'].min()} - {d8['Year'].max()}</span>"},
            value = (d8['Sales'].sum()),
            number = {'prefix': ""}
    ))


    fig7.update_layout(height=230)
    fig8.update_layout(height=230)
    return fig7, fig8



@callback(
        Output("graph9", "figure"),
        Input("sales-select", "value"),
        State('sales-select','label'),
        State("panelSales-dataset-multi-select", "value")
)
def changeSales(value, label, dataset):
     sales_train_all_df = getColections(dataset)
     
     df9 = sales_train_all_df.groupby(f'{value}')['Sales'].mean().reset_index()
     
     if value == 'DayOfWeek':
        dia_semana_dict = {1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado', 7: 'Domingo'}
        df9['DayOfWeek'] = df9['DayOfWeek'].map(dia_semana_dict)

     if value == 'Month': 
        meses_dict = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
              7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        df9['Month'] = df9['Month'].map(meses_dict)

     fig = go.Figure()
     fig.add_trace(go.Bar(x=df9[f'{value}'], y=df9['Sales'], name='Média de Vendas', marker_color='blue'))

     # Adicionar o gráfico de linha
     fig.add_trace(go.Scatter(x=df9[f'{value}'], y=df9['Sales'], mode='lines', name='Média de Vendas', line_color='red'))

     salesBy = {'Year': 'Ano', 'Day': 'Dia', 'Month': 'Mês', 'DayOfWeek': 'Dia da Semana'}
     # Personalizar layout e estilo do gráfico
     fig.update_layout(
        title=f'Média de Vendas por {salesBy.get(value)}',
        xaxis_title=f'{salesBy.get(value)}',
        yaxis_title='Média de Vendas',
        plot_bgcolor='white',
        showlegend=False
     )

     # Personalizar cores das barras
    #  cores = px.colors.qualitative.Plotly
     fig.update_traces(marker_color='#2B454E')

     return fig

@callback(
        Output("graph10", "figure"),
        Input("customers-select", "value"),
        State('customers-select','label'),
        State("panelSales-dataset-multi-select", "value")
)
def changeCustomers(value, label, dataset):
     sales_train_all_df = getColections(dataset)

     df10 = sales_train_all_df.groupby(f'{value}')['Customers'].mean().reset_index()
     
     if value == 'DayOfWeek':
        dia_semana_dict = {1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado', 7: 'Domingo'}
        df10['DayOfWeek'] = df10['DayOfWeek'].map(dia_semana_dict)
     
     if value == 'Month': 
        meses_dict = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
              7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        df10['Month'] = df10['Month'].map(meses_dict)

     fig = go.Figure()
     fig.add_trace(go.Bar(x=df10[f'{value}'], y=df10['Customers'], name='Média de Clientes', marker_color='blue'))

     # Adicionar o gráfico de linha
     fig.add_trace(go.Scatter(x=df10[f'{value}'], y=df10['Customers'], mode='lines', name='Média de Clientes', line_color='red'))

     customersBy = {'Year': 'Ano', 'Day': 'Dia', 'Month': 'Mês', 'DayOfWeek': 'Dia da Semana'}
     # Personalizar layout e estilo do gráfico
     fig.update_layout(
        title=f'Média de Clientes por {customersBy.get(value)}',
        xaxis_title=f'{customersBy.get(value)}',
        yaxis_title='Média de Clientes', 
        plot_bgcolor='white',
        showlegend=False
     )

     # Personalizar cores das barras
     #  cores = px.colors.qualitative.Plotly
     fig.update_traces(marker_color='#2B454E')

     return fig


@callback(Output('panelSales-dataset-multi-select', component_property='value'),
          Output('panelSales-dataset-multi-select', component_property='data'),
                Input('interval_db', component_property='n_intervals'),
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
    Output('dataset-sales-storage', 'data', allow_duplicate=True),
    Input("panelSales-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions


def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD = pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    
    df_PD['Year'] = pd.DatetimeIndex(df_PD['Date']).year
    df_PD['Month'] = pd.DatetimeIndex(df_PD['Date']).month
    df_PD['Day'] = pd.DatetimeIndex(df_PD['Date']).day
    return df_PD