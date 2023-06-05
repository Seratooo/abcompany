from dash import html, Output, Input, callback, State
from dash import dcc
from datetime import date, datetime
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from api.externalFactors import GetHolidaysByYear, GetInflationByYear, GetWeatherByYear
from data import configs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc


DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]

forecast = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-sales-forecast-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Realizar previsão', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('realize a previsão de vendas até uma data pretendida', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ]),
                    html.Div([
                        html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        dmc.MultiSelect(
                        label="",
                        placeholder="Select all you like!",
                        id="panelForecast-dataset-multi-select",
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
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
        html.Div([
            dmc.Button("Prever", id="forecast-btn"),
            dmc.Select(
                        label="",
                        placeholder="Selecione o periodo",
                        id="period-multi-select",
                        value="M",
                        data=[
                            {"value": "D", "label": "Diária"},
                            {"value": "M", "label": "Mensal"},
                            {"value": "Y", "label": "Anual"},
                        ],
                        style={"width": 200, "marginBottom": 10,"fontSize":"1.2rem"},
                        ),
             dmc.Select(
                        label="",
                        placeholder="Prever até:",
                        id="lenght-multi-select",
                        value="1",
                        data=[
                            {"value": "1", "label": "1"},
                            {"value": "2", "label": "2"},
                            {"value": "3", "label": "3"},
                            {"value": "4", "label": "4"},
                            {"value": "5", "label": "5"},
                            {"value": "6", "label": "6"},
                            {"value": "7", "label": "7"},
                            {"value": "8", "label": "8"},
                            {"value": "9", "label": "9"},
                            {"value": "10", "label": "10"},
                            {"value": "11", "label": "11"},
                            {"value": "12", "label": "12"},
                        ],
                        style={"width": 200, "marginBottom": 10,"fontSize":"1.2rem"},
                )
        ], style={"display":"flex", "gap":"20px"}),
     dmc.MultiSelect(
            label="Factores a considerar",
            placeholder="Select all you like!",
            id="factors-multi-select",
            value=["holiday"],
            data=[
                {"value": "weather", "label": "Clima"},
                {"value": "holiday", "label": "Feridos Nacionais"},
                #{"value": "svelte", "label": "Feriados Escolares"},
                {"value": "inflation", "label": "Inflação"},
            ],
            style={"width": 400, "marginBottom": 10},
        ),
    ], id="predition-componets"),
     html.Div([
            html.Div(id='graph11'),
            html.Div(id='graph12'),
            html.Div(id='graph13'),
        ], style={"background":"#F0F0F0", "padding":"10px 0"}),
       
])



@callback(Output('panelForecast-dataset-multi-select', component_property='value'),
          Output('panelForecast-dataset-multi-select', component_property='data'),
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
    Output('dataset-sales-forecast-storage', 'data', allow_duplicate=True),
    Input("panelForecast-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions


@callback(
    Output("graph11", "children"),
    Output("graph12", "children"),
    Output("graph13", "children"),
    State('factors-multi-select','value'),
    Input('externarFactors', 'data'),
    Input('forecast-btn','n_clicks'),
    State('lenght-multi-select', 'value')
)
def set_forecast(factorsSeleted, externarFactors, nclicks, lenght):
    Holidays = pd.DataFrame()
    Weather = pd.DataFrame()
    Inflation = pd.DataFrame()
    Dataset = getColections(PanelMultiSelectOptions)
    Lenght = int(lenght) * 30
    if Dataset['_id'].any():
        Dataset.drop('_id', axis=1, inplace=True)
    
    for sFactor in factorsSeleted:
        if(sFactor == 'holiday'):
            Holidays = getHolidays(externarFactors)
        elif(sFactor == 'weather'):
            Weather = getWeather(externarFactors)
        elif(sFactor == 'inflation'):
            Inflation = getInflation(externarFactors)
    
    df_original, df_predition = configs.sales_predition(0,Dataset,Holidays, Lenght)
    
    fig = px.line(df_predition, x='ds', y='yhat', title='Previsões de Vendas')

    # Adicionando faixa de incerteza
    fig.add_trace(
        go.Scatter(
            x=df_predition['ds'],
            y=df_predition['yhat_upper'],
            fill='tonexty',
            mode='none',
            name='Faixa de Incerteza',
            line=dict(color='rgba(0, 176, 246, 0.2)')
        )
    )

    fig.add_scatter(x=df_original['ds'], y=df_original['y'], mode='markers', name='Vendas reais')

    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Vendas',
        legend_title='Dados',
        hovermode='x',
        template='plotly_white'
    )
    
    fig = dcc.Graph(
        id='graph11',
        figure=fig
    )
    

    fig2 = dcc.Graph(
            id="graph12",
            figure={
                "data": [
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition['holidays'],
                        mode="lines+markers",
                        name="Feriados",
                        line=dict(color='rgb(31, 119, 180)'),
                        marker=dict(size=8, color='rgb(31, 119, 180)', symbol='circle'),
                    )
                ],
                "layout": go.Layout(
                    title="Impacto de Feriados nas Vendas",
                    xaxis=dict(title="Data", showgrid=False),
                    yaxis=dict(title="Feriados", showgrid=False),
                    plot_bgcolor="rgb(240, 240, 240)",
                    paper_bgcolor="rgb(255, 255, 255)",
                    font=dict(color="rgb(0, 0, 0)"),
                ),
            },
        )
    
    #fig = px.area(df_predition, x="ds", y="yhat")
    #fig2 = px.histogram(df_predition, x="ds", y="holidays", hover_data=df_predition.columns)

    fig3 = px.line(df_predition, x='ds', y='trend', color='trend', symbol="trend")
    fig3_graph = dcc.Graph(
        id='graph13',
        figure=fig3
    )
    
    return fig, fig2, fig3_graph



def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    return df_PD

def getHolidays(data):
    Years = data.get('holiday')
    HolidayPD = pd.DataFrame()
    for year in Years:
       HolidayPD = pd.concat((HolidayPD, GetHolidaysByYear(int(year))[0]))
    return HolidayPD


def getWeather(data):
    Years = data.get('weather')
    WeatherPD = pd.DataFrame()
    for year in Years:
       WeatherPD = pd.concat((WeatherPD, GetWeatherByYear(int(year))[0]))
    return WeatherPD

def getInflation(data):
    Years = data.get('inflation')
    InflationPD = pd.DataFrame()
    for year in Years:
       InflationPD = pd.concat((InflationPD, GetInflationByYear(int(year))[2]))
    return InflationPD

    