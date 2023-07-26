import base64
from dash import html, Output, Input, callback, State
from dash import dcc
from datetime import date, datetime
from api.chartsAPI import TemplateForceastChart
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from api.externalFactors import GetHolidaysByYear, GetInflationByYear, GetWeatherByYear, future_weather
from data import configs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.io as pio

from report.reports import convert_html_to_pdf

DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]
global df_predition, report_html, figures
figures = []
template = TemplateForceastChart

forecast = html.Div([
    dcc.Download(id="download-forecast"),
    html.Div(id='report-output-forecast', className='report_output'),
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-sales-forecast-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Realizar previsão', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Realize a previsão de vendas até uma data pretendida', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ]),
                    html.Div([
                        dmc.MultiSelect(
                        label="",
                        placeholder="Selecione seus conjuntos de dados!",
                        id="panelForecast-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[],
                        style={"width": 400, "fontSize":"1.2rem"},
                        ),
                        dmc.Button("Gerar relatório", style={"background":"#fff", "color":"#000","font":"3.2rem Nunito","marginTop":"1.2rem"}, id='generate-report'),
                    ], style={"display":"flex","justifyContent":"space-between", "alignItems":"center"})
                ])
            )
        ], style={"background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
        html.Div([
             dmc.Button("Prever", id="forecast-btn"),
             dmc.Select(
                        label="",
                        placeholder="Selecione o periodo",
                        id="period-multi-select",
                        value=31,
                        data=[
                            {"value": 1, "label": "Diária"},
                            {"value": 31, "label": "Mensal"},
                            {"value": 365, "label": "Anual"},
                        ],
                        style={"width": 150, "marginBottom": 10,"fontSize":"1.2rem"},
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
                        style={"width": 150, "marginBottom": 10,"fontSize":"1.2rem"},
                )
        ], id='predition-elements', style={"display":"flex", "gap":"20px"}),
        html.Div([
            dmc.Select(
                label="Feriados Nacionais",
                placeholder="Selecione o seu país!",
                id="country-name-select",
                value="AO",
                data=[
                    {"value": "AO", "label": "Angola"},
                ],
                style={"width": 200},
            ),
            dmc.MultiSelect(
                    label="Factores a considerar",
                    placeholder="Selecione os fatores a considerar!",
                    id="factors-multi-select",
                    value=["schoolholiday"],
                    data=[
                        {"value": "weather", "label": "Clima"},
                        {"value": "schoolholiday", "label": "Feriados Escolares"},
                        {"value": "inflation", "label": "Inflação"},
                    ],
                    style={"width": 300},
                ),
        ], id="factors-wrapper-components"),
    ], id="factors-components"),
    html.Div([
            dmc.NumberInput(
                id='fourier-number',
                label="Sazonalidade Anual",
                description="Suavização da sazonalidade",
                value=10,
                min=0,
                max=30,
                step=5,
                icon=DashIconify(icon="fa6-solid:weight-scale"),
                style={"width": 180},
            ),
            dmc.NumberInput(
                id='fourier-month-number',
                label="Sazonalidade Mensal",
                description="Suavização da sazonalidade",
                value=5,
                min=0,
                max=10,
                step=1,
                icon=DashIconify(icon="fa6-solid:weight-scale"),
                style={"width": 180},
            ),
            dmc.Select(
            label="Tipo de Sazonalidade",
            description="Relação entre a sozalidade e a tendência!",
            id="seasonality-mode-select",
            value="multiplicative",
            data=[
                {"value": "multiplicative", "label": "Multiplicativa"},
                {"value": "additive", "label": "Aditiva"},

            ],
            style={"width": 250},
        ),

    ], id="parameters-components"),
     dcc.Loading(children=[
        html.Div(
            [
                html.Div(id='predition-results'),
                html.Div(id='holidays-results'),
            ], style={"background":"#F0F0F0", "padding":"10px 0", "height":"55vh"},),
        ], color="#2B454E", type="dot", fullscreen=False,),
       
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
    Output("predition-results", "children"),
    Output("holidays-results","children"),
    State('factors-multi-select','value'),
    Input('externarFactors', 'data'),
    Input('forecast-btn','n_clicks'),
    State('lenght-multi-select', 'value'),
    State('country-name-select','value'),
    State('fourier-number','value'),
    State('fourier-month-number','value'),
    State('seasonality-mode-select','value'),
    State('period-multi-select','value'),
)
def set_forecast(factorsSeleted, externarFactors, nclicks, lenght, country_name, fourier, fourier_monthly, seasonality_mode, period):
    
    if nclicks is not None:
        global figures
        figures = []
        Holidays = pd.DataFrame()
        Weather = pd.DataFrame()
        Inflation = pd.DataFrame()
        Dataset = getColections(PanelMultiSelectOptions)
        Lenght = int(lenght) * period
        global df_predition
        if Dataset['_id'].any():
            Dataset.drop('_id', axis=1, inplace=True)
        
        for sFactor in factorsSeleted:
            if(sFactor == 'schoolholiday'):
                Holidays = pd.read_csv('data/school_holiday.csv')
            elif(sFactor == 'weather'):
                Dataset.loc[:, 'Weather'] = Dataset['Date'].apply(future_weather)
            elif(sFactor == 'inflation'):
                Inflation = getInflation(externarFactors)
        
        if 'Weather' in Dataset.columns:
            df_original, df_predition, model = configs.sales_predition_Weather(Dataset,Holidays, Lenght, country_name, fourier, fourier_monthly, seasonality_mode)
            Weather_regressor = dcc.Graph(
            id='regressors-plot',
            figure={
                'data': [
                    {'x': df_predition['ds'], 'y': df_predition['extra_regressors_multiplicative'], 'type': 'line'}
                ],
                'layout': {
                    'title': 'Regressores (Clima)',
                    'xaxis': {'title': 'Data'},
                    'yaxis': {'title': 'Clima'}
                }
            }
            )
        else:
            df_original, df_predition, model = configs.sales_predition_v2(Dataset,Holidays, Lenght, country_name, fourier, fourier_monthly, seasonality_mode)

        
        
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
        figures.append(fig)
        Predition_graph = dcc.Graph(
            id='graph11',
            figure=fig
        )
        
        
        MyHolidays = []
        MyHolidays.append(dcc.Tab(label='Feriados Nacionais', value='holiday'))
        for hday in model.train_holiday_names:
            MyHolidays.append(dcc.Tab(label=hday, value=f'{hday}'))

        HolidaysTabs = [
            dcc.Tabs(id="tabs-holiday", value='holiday', children=MyHolidays),
            html.Div(id='tabs-content-holiday-graph')
        ]

        fig3 = px.line(df_predition, x='ds', y='trend', color='trend', symbol="trend")
        fig3_graph = dcc.Graph(
            id='graph13',
            figure=fig3
        )
        figures.append(fig3)
        
        yearly_seasonality_fig = go.Figure(
            data=[
                go.Scatter(x=df_predition['ds'], y=df_predition['yearly'], mode='lines')
            ],
            layout=go.Layout(
                title='Sazonalidade Anual',
                xaxis={'title': 'Data'},
                yaxis={'title': 'Sazonalidade'}
            )
        )
        yearly_seasonality = dcc.Graph(
            id='seasonality-yearly-plot',
            figure=yearly_seasonality_fig
        )
        figures.append(yearly_seasonality_fig)
        
        monthly_seasonality = dcc.Graph(
            id='seasonality-monthly-plot',
            figure={
                'data': [
                    {'x': df_predition['ds'], 'y': df_predition['monthly'], 'type': 'line'}
                ],
                'layout': {
                    'title': 'Sazonalidade Mensal',
                    'xaxis': {'title': 'Data'},
                    'yaxis': {'title': 'Sazonalidade'}
                }
            }
        )
        
        weekly_seasonality = dcc.Graph(
            id='seasonality-weekly-plot',
            figure={
                'data': [
                    {'x': df_predition['ds'], 'y': df_predition['weekly'], 'type': 'line'}
                ],
                'layout': {
                    'title': 'Sazonalidade Semanal',
                    'xaxis': {'title': 'Data'},
                    'yaxis': {'title': 'Sazonalidade'}
                }
            }
        )

        seasonality = dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab("Sazonalidade Anual", value="yearly"),
                    dmc.Tab("Sazonalidade Mensal", value="monthly"),
                    dmc.Tab("Sazonalidade Semanal", value="weekly"),
                ]
            ),
            dmc.TabsPanel(yearly_seasonality, value="yearly"),
            dmc.TabsPanel(monthly_seasonality, value="monthly"),
            dmc.TabsPanel(weekly_seasonality, value="weekly"),
        ],
        color="green",
        value='yearly',
        orientation="horizontal",
        )

        if 'Weather' in Dataset.columns:
            return [Predition_graph, Weather_regressor, seasonality, fig3_graph], HolidaysTabs
        else:
            return [Predition_graph, seasonality, fig3_graph], HolidaysTabs
    else:
        return html.Div('Realize sua previsão aqui!', id="predition-banner"), html.Div()


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

    

@callback(Output('tabs-content-holiday-graph', 'children'),
              Input('tabs-holiday', 'value'))
def render_content(tab):
    global df_predition
    if tab == 'holiday':
        return html.Div([
            html.H3('Impacto dos Feriados Nacionais'),
            dcc.Graph(
            id=tab,
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
        ])
    else:
        return html.Div([
            html.H3(tab),
            dcc.Graph(
            id=tab,
            figure={
                "data": [
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition[f'{tab}'],
                        mode="lines+markers",
                        name="Feriado",
                        line=dict(color='rgb(31, 119, 180)'),
                        marker=dict(size=8, color='rgb(31, 119, 180)', symbol='circle'),
                    )
                ],
                "layout": go.Layout(
                    title=f"Impacto {tab}",
                    xaxis=dict(title="Data", showgrid=False),
                    yaxis=dict(title="Feriado", showgrid=False),
                    plot_bgcolor="rgb(240, 240, 240)",
                    paper_bgcolor="rgb(255, 255, 255)",
                    font=dict(color="rgb(0, 0, 0)"),
                ),
            },
        )
        ])
    
@callback(
    Output('report-output-forecast','children'),
    Output('report-output-forecast', 'style', allow_duplicate=True),
    Input('generate-report','n_clicks'),
    prevent_initial_call=True
)
def generate_report(n_clicks):
    images = [base64.b64encode(pio.to_image(figure, format='png', width='1240px', height='auto')).decode('utf-8') for figure in figures]
    
    global report_html
    report_html = ''
    for index, image in enumerate(images):
        _ = template
        _ = _.format(image=image, width='900px', height='auto')
        report_html += _

    if n_clicks is not None:
        return [
            html.Div([
                html.Div('Download', id="dowload-report"),
                html.Div('Fechar', id='close-report'),
            ], className="wrapper-btn-report"),
            html.Iframe(srcDoc=report_html, width="100%", height="100%")
            ], {'display': 'block'}
    else:
        return '', {'display': 'none'}
    

@callback(
    Output('report-output-forecast', 'style'),
    Input('close-report','n_clicks'),
)
def close_report(n_clicks):
    if n_clicks is not None:
       return {'display': 'none'}
    else:
        return {'display': 'block'}
    
@callback(
    Output('download-forecast', 'data'),
    Input('dowload-report','n_clicks'),
)
def dowload_report(n_clicks):
    if n_clicks is not None:
        convert_html_to_pdf(report_html,'report_html.pdf')
        return dcc.send_file(
        "./report_html.pdf", "forecast_report.pdf")