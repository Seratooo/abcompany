from dash import html, dcc, callback, Output, Input, State
from api.clientApp import GetAllCollectionNames
from data.configs import getDatabase
import plotly.graph_objects as go
import dash_mantine_components as dmc


sales_train_all_df = getDatabase()
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
        html.Div([
            html.Div([dcc.Graph(id='graph6', className='dbc')],style={"width":"30%"}),
            html.Div([dcc.Graph(id='graph7', className='dbc')], style={"width":"30%"}),
            html.Div([dcc.Graph(id='graph8', className='dbc')], style={"width":"30%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        html.Div([
            html.Div([
                dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="framework-select",
                    value="dia",
                    data=[
                        {"value": "mes", "label": "Mês"},
                        {"value": "ano", "label": "Ano"},
                        {"value": "semana", "label": "Semana"},
                        {"value": "dia", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Graph(id='graph9', className='dbc'),
            ], style={"width":"46%"}),
            html.Div([
                 dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="framework-select",
                    value="dia",
                    data=[
                        {"value": "mes", "label": "Mês"},
                        {"value": "ano", "label": "Ano"},
                        {"value": "semana", "label": "Semana"},
                        {"value": "dia", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Graph(id='graph10', className='dbc'),
            ], style={"width":"46%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        
], style={"width":"100%","height":"140%"})



@callback(
          Output("graph6", "figure"),
          Output("graph7", "figure"),
          Output("graph8", "figure"),
          Output("graph9", "figure"),
          Output("graph10", "figure"),
          Input("panelSales-dataset-multi-select", "value")
          )
def select_value(value):
    d6 = sales_train_all_df[sales_train_all_df['Promo']==1]
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Promoções realizadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d6['Year'].min()} - {d6['Year'].max()}</span>"},
            value = (d6['Promo'].count()),
            number = {'suffix': ""}
    ))

    d7 = sales_train_all_df[sales_train_all_df['Customers']>0]
    fig7 = go.Figure()
    fig7.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Clientes Alcançados</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d7['Year'].min()} - {d7['Year'].max()}</span>"},
            value = (d7['Customers'].count()),
            number = {'suffix': ""}
    ))

    d8 = sales_train_all_df
    fig8 = go.Figure()
    fig8.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Receitas Arrecadadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d8['Year'].min()} - {d8['Year'].max()}</span>"},
            value = (d8['Sales'].sum()),
            number = {'prefix': "AKZ "}
    ))


    df9 = sales_train_all_df.groupby('Day')['Sales'].mean().reset_index()
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(
            x=df9["Day"],
            y=df9["Sales"],
            mode="lines",
            name="hash-rate-TH/s"
        ))
    fig9.update_layout(
        showlegend=False,
        title_text="Média das vendas por dia",
    )

    df10 = sales_train_all_df.groupby('Day')['Customers'].mean().reset_index()
    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(
            x=df10["Day"],
            y=df10["Customers"],
            mode="lines",
            name="hash-rate-TH/s"
        ))
    fig10.update_layout(
        showlegend=False,
        title_text="Média de clientes por dia",
    )

    fig6.update_layout(height=230)
    fig7.update_layout(height=230)
    fig8.update_layout(height=230)
    return fig6, fig7, fig8, fig9, fig10



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
        data.append({"value": f"{name}", "label": f"{name}"})
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