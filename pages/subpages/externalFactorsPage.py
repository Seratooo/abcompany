from dash import html, Output, Input, callback, dash_table, State, dcc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objs as go
from api.externalFactors import GetHolidaysByYear, GetInflationByYear, GetWeatherByYear

HolidayMultiSelectOptions = ['2021', '2022']
WeatherMultiSelectOptions = ['2021', '2022']
InflationMultiSelectOptions = ['2021', '2022']

HolidayTab = [
     html.P(children='Feriados', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#000","marginBottom":".8rem"}),
        html.Div(
            [
                dmc.MultiSelect(
                    label="Anos à considerar",
                    placeholder="Select all you like!",
                    id="holiday-multi-select",
                    value=HolidayMultiSelectOptions,
                    data=[
                        {"value": "2013", "label": "2013"},
                        {"value": "2014", "label": "2014"},
                        {"value": "2015", "label": "2015"},
                        {"value": "2016", "label": "2016"},
                        {"value": "2017", "label": "2017"},
                        {"value": "2018", "label": "2018"},
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
         dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Dados", value="data_holiday"),
                        dmc.Tab("Gráficos", value="graph_holiday")
                    ]
                ),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="holiday-multi-selected-value", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="data_holiday"),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="holiday-graph", style={"height":"55vh"}),], color="var(--primary)", type="dot", fullscreen=False,), value="graph_holiday"),
            ],
            color="green",
            orientation="horizontal",
            value="data_holiday"
        ),
        dcc.Store(id='holiday-selected-value-storage', storage_type='local'),
]

WeatherTab = [
     html.P(children='Clima', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#000","marginBottom":".8rem"}),
        html.Div(
            [
                dmc.MultiSelect(
                    label="Anos à considerar",
                    placeholder="Select all you like!",
                    id="weather-multi-select",
                    value=WeatherMultiSelectOptions,
                    data=[
                        {"value": "2013", "label": "2013"},
                        {"value": "2014", "label": "2014"},
                        {"value": "2015", "label": "2015"},
                        {"value": "2016", "label": "2016"},
                        {"value": "2017", "label": "2017"},
                        {"value": "2018", "label": "2018"},
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Dados", value="data_weather"),
                        dmc.Tab("Gráficos", value="graph_weather")
                    ]
                ),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="weather-multi-selected-value", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="data_weather"),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="weather-graph", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="graph_weather")
            ],
            color="green",
            orientation="horizontal",
            value="data_weather"
        ),
        dcc.Store(id='weather-selected-value-storage', storage_type='local'),
]


InflationTab = [
     html.P(children='Inflação', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#000","marginBottom":".8rem"}),
        html.Div(
            [
                dmc.MultiSelect(
                    label="Anos à considerar",
                    placeholder="Select all you like!",
                    id="inflation-multi-select",
                    value=InflationMultiSelectOptions,
                    data=[
                        {"value": "2013", "label": "2013"},
                        {"value": "2014", "label": "2014"},
                        {"value": "2015", "label": "2015"},
                        {"value": "2016", "label": "2016"},
                        {"value": "2017", "label": "2017"},
                        {"value": "2018", "label": "2018"},
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
         dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Dados", value="data_inflation"),
                        dmc.Tab("Gráficos", value="graph_inflation")
                    ]
                ),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="inflation-multi-selected-value", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="data_inflation"),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="inflation-graph", style={"height":"55vh"}),], color="var(--primary)", type="dot", fullscreen=False,), value="graph_inflation")
            ],
            color="green",
            orientation="horizontal",
            value="data_inflation"
        ),
        dcc.Store(id='inflation-selected-value-storage', storage_type='local'),
]


externalFactorsPage = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Fatores Externos', className='PainelStyle'),
                    html.Div([
                        html.P('Aqui você analisar os fatores externos ao longo do tempo', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"var(--primary)", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Feriados", value="holidays"),
                        dmc.Tab("Clima", value="weather"),
                        dmc.Tab("Inflação", value="inflation"),
                    ]
                ),
                dmc.TabsPanel(HolidayTab, value="holidays", style={"padding":"10px"}),
                dmc.TabsPanel(WeatherTab, value="weather", style={"padding":"10px"}),
                dmc.TabsPanel(InflationTab, value="inflation", style={"padding":"10px"}),
            ],
            color="green",
            orientation="vertical",
            value="holidays"
        ),
    ], style={"padding":"10px 0", "height":"100vh", "background":"#f0f0f0","overflow":"scroll","marginBottom":"30px"}),
])


@callback(Output("holiday-multi-select", "value"),
          Output("weather-multi-select", "value"),
          Output("inflation-multi-select", "value"),
              Input('interval_db', component_property='n_intervals')
              )
def LoadPage(n_intervals):
    return HolidayMultiSelectOptions, WeatherMultiSelectOptions, InflationMultiSelectOptions

### --- Holiday --- ###
@callback(
    Output('holiday-selected-value-storage', 'data'),
    Input("holiday-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_holiday(value):
    global HolidayMultiSelectOptions
    HolidayMultiSelectOptions = value
    return HolidayMultiSelectOptions

@callback(
    Output("holiday-multi-selected-value", "children"),
    Output("holiday-graph", "children"), 
    Input("holiday-multi-select", "value")
)
def select_value_holiday(value):
    value = HolidayMultiSelectOptions
    HolidayPD = pd.DataFrame()
    for year in value:
       HolidayPD =pd.concat((HolidayPD, GetHolidaysByYear(int(year))[1]))
    
    HolidayPD.rename(columns={'ds': 'Data'}, inplace=True)
    table = dash_table.DataTable(
    data=HolidayPD.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in HolidayPD.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    )


    graph = dcc.Graph(
        id='holiday-mygraph',
        figure={
            'data': [
                go.Scatter(
                    x=HolidayPD['Data'],
                    y=[1] * len(HolidayPD['holiday']),  # Usamos 1 em todos os feriados para criar um gráfico de pontos
                    mode='markers',
                    marker={'size': 10},
                    name='Feriados'
                )
            ],
            'layout': {
                'title': 'Feriados Nacionais',
                'xaxis': {'title': 'Data'},
                'yaxis': {'showticklabels': False}
            }
        }
    )


    return table, graph

### --- Weather --- ###


@callback(
    Output('weather-selected-value-storage', 'data'),
    Input("weather-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_weather(value): 
    global WeatherMultiSelectOptions
    WeatherMultiSelectOptions = value
    return WeatherMultiSelectOptions

@callback(
    Output("weather-multi-selected-value", "children"),
    Output("weather-graph","children"),
    Input("weather-multi-select", "value")
)
def select_value_weather(value):
    value = WeatherMultiSelectOptions
    WeatherPD = pd.DataFrame()
    for year in value:
        WeatherPD = pd.concat((WeatherPD, GetWeatherByYear(int(year))[1]))
    
    WeatherPD['Data'] = WeatherPD.index

    table = dash_table.DataTable(
    data=WeatherPD.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in WeatherPD.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    )

    graph = dcc.Graph(
        id='temperature-graph',
        figure={
            'data': [
                {'x': WeatherPD['Data'], 'y': WeatherPD['Temperatura média'], 'type': 'scatter', 'name': 'Temperatura Média'},
                {'x': WeatherPD['Data'], 'y': WeatherPD['Temperatura mínima'], 'type': 'scatter', 'name': 'Temperatura Mínima'},
                {'x': WeatherPD['Data'], 'y': WeatherPD['Temperatura máxima'], 'type': 'scatter', 'name': 'Temperatura Máxima'},
            ],
            'layout': {
                'title': 'Variação da Temperatura',
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Temperatura (°C)'}
            }
        }
    )

    return table, graph

### --- Inflation ---###


@callback(
    Output('inflation-selected-value-storage', 'data'),
    Input("inflation-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_inflation(value):
    global InflationMultiSelectOptions
    InflationMultiSelectOptions = value
    return InflationMultiSelectOptions

@callback(
    Output("inflation-multi-selected-value", "children"),
    Output("inflation-graph", "children"), 
    Input("inflation-multi-select", "value")
)
def select_value_inflation(value):
    value = InflationMultiSelectOptions
    InflationPD = pd.DataFrame()
    for year in value:
        InflationPD =pd.concat((InflationPD, GetInflationByYear(int(year))[2]))
    
    InflationPD['Data'] = InflationPD.index
    table = dash_table.DataTable(
    data=InflationPD.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in InflationPD.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    )

    graph = dcc.Graph(
        id='inflation-mygraph',
        figure={
            'data': [
                go.Scatter(
                    x=InflationPD['Data'],
                    y=InflationPD['Dolar'],
                    mode='lines',
                    name='Dólar'
                ),
                go.Scatter(
                    x=InflationPD['Data'],
                    y=InflationPD['Euro'],
                    mode='lines',
                    name='Euro'
                )
            ],
            'layout': {
                'title': 'Inflação do Dólar e do Euro',
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Inflação (%)'}
            }
        }
    )

    return table, graph


@callback(
    Output('externarFactors', 'data'),
    [Input("holiday-multi-select", "value"),
    Input("weather-multi-select", "value"),
    Input("inflation-multi-select", "value")]
)
def setData(holiday, weather, inflation):
    store = {
        'holiday': holiday,
        'weather': weather,
        'inflation': inflation
    }
    return store
