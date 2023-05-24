from dash import html, Output, Input, callback, dash_table, State, dcc
import dash_mantine_components as dmc
import pandas as pd

from api.externalFactors import GetHolidaysByYear, GetInflationByYear, GetWeatherByYear

HolidayMultiSelectOptions = ["2019", "2020"]
WeatherMultiSelectOptions = ["2019", "2020"]
InflationMultiSelectOptions = ["2019", "2020"]

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
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
        html.Div(id="holiday-multi-selected-value"),
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
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
        html.Div(id="weather-multi-selected-value"),
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
                        {"value": "2019", "label": "2019"},
                        {"value": "2020", "label": "2020"},
                        {"value": "2021", "label": "2021"},
                        {"value": "2022", "label": "2022"},
                    ],
                    style={"width": 400, "marginBottom": 10},
                ),
            ]
        ),
        html.Div(id="inflation-multi-selected-value"),
        dcc.Store(id='inflation-selected-value-storage', storage_type='local'),
]


externalFactorsPage = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Fatores Externos', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Aqui você poderá configurar fatores externos que impactam sua venas', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
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
            color="red",
            orientation="vertical",
        ),
    ], style={"padding":"5rem", "height":"100vh"}),
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
    Input("holiday-multi-select", "value")
)
def select_value_holiday(value):
    # if(len(dataStorage) > 0):
    value = HolidayMultiSelectOptions
    HolidayPD = pd.DataFrame()
    for year in value:
       HolidayPD =pd.concat((HolidayPD, GetHolidaysByYear(int(year))))
    
    HolidayPD['Data'] = HolidayPD.index
    table = dash_table.DataTable(
    data=HolidayPD.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in HolidayPD.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    )
    return table

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
    Input("weather-multi-select", "value")
)
def select_value_weather(value):
    value = WeatherMultiSelectOptions
    WeatherPD = pd.DataFrame()
    for year in value:
        WeatherPD =pd.concat((WeatherPD, GetWeatherByYear(int(year))[1]))
    
    WeatherPD['Data'] = WeatherPD.index
    table = dash_table.DataTable(
    data=WeatherPD.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in WeatherPD.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    )
    return table

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
    return table