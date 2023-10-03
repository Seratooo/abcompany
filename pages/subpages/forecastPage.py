import base64
from dash import html, Output, Input, callback, State
from dash import dcc
from datetime import date, datetime
from api.chartsAPI import TemplateForceastChart
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from api.externalFactors import GetHolidaysByYear, GetInflationByYear, GetWeatherByYear, future_euro_inflation, future_usd_inflation, future_weather
from data import configs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.io as pio
#from sklearn.metrics import mean_absolute_percentage_error

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
                    html.H3('Realizar previsão', className='PainelStyle'),
                    html.Div([
                        dmc.MultiSelect(
                        label="",
                        placeholder="Selecione seus conjuntos de dados!",
                        id="panelForecast-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[],
                        style={"width": 200, "fontSize":"1.2rem"},
                        ),
                        dmc.DatePicker(
                        minDate=date(2023, 1, 1),
                        maxDate=datetime.now().date(),
                        value=date(2023, 1, 31),
                        inputFormat="DD-MM-YYYY",
                        id='forecast-date',
                        ),
                        dmc.Button("Prever", id="forecast-btn"),
                    ], style={"display":"flex","justifyContent":"space-between", "alignItems":"center", "gap":"10px"}, id='predition-elements')
                ]),
                
            ),
            dmc.Button("Gerar relatório", id='generate-report'),
        ],className='WrapperPainel'),
    html.Div([
        html.Div([
            dmc.Select(
                placeholder="Feriados Nacionais!",
                id="country-name-select",
                value="AO",
                description='Feriados',
                data=[
                    {"value": "AO", "label": "Angola"},
                    {"value": "MZ", "label": "Moçambique"},

                ],
                style={"width": 150},
            ),
            dmc.MultiSelect(
                    placeholder="Factores a considerar",
                    id="factors-multi-select",
                    description='Factores',
                    value=["schoolholiday"],
                    data=[
                        {"value": "schoolholiday", "label": "Feriados Escolares"},
                        {"value": "weather", "label": "Temperatura"},
                        {"value": "covid_19", "label": "Covid-19"},
                        {"value": "inflation_eur", "label": "Euro (Taxa de câmbio)"},
                        {"value": "inflation_usd", "label": "Dólar (Taxa de câmbio)"},

                    ],
                    style={"width": 325},
                ),
        ], id="factors-wrapper-components"),
        html.Div([
            dmc.NumberInput(
                id='fourier-number',
                description="Sazonalidade Anual",
                value=10,
                min=0,
                max=30,
                step=5,
                icon=DashIconify(icon="fa6-solid:weight-scale"),
                style={"width": 120},
            ),
            dmc.NumberInput(
                id='fourier-month-number',
                description="Sazonalidade Mensal",
                value=5,
                min=0,
                max=10,
                step=1,
                icon=DashIconify(icon="fa6-solid:weight-scale"),
                style={"width": 120},
            ),
            dmc.Select(
            description="Tipo de Sazonalidade",
            id="seasonality-mode-select",
            value="multiplicative",
            data=[
                {"value": "multiplicative", "label": "Multiplicativa"},
                {"value": "additive", "label": "Aditiva"},

            ],
            style={"width": 150},
            ),
            dmc.Select(
            description="Produto",
            id="product-select",
            value="Peixe Carapau",
            data=[
                {"value": "Água Pura 5L", "label": "Água Pura 5L"},
                {"value": "Abacate Nacional", "label": "Abacate Nacional"},
                {"value": "Asa de Frango 10Kg", "label": "Asa de Frango 10Kg"},
                {"value": "Peixe Carapau", "label": "Peixe Carapau"},
                {"value": "Peixe Corvina", "label": "Peixe Corvina"},
                {"value": "Peixe Pescada", "label": "Peixe Pescada"},
                {"value": "Batata Rena Nacional", "label": "Batata Rena Nacional"},
                {"value": "Batata Doce Nacional", "label": "Batata Doce Nacional"},
                {"value": "Cebola Nacional", "label": "Cebola Nacional"},
                {"value": "COXA USA KOCH FOODS", "label": "COXA USA KOCH FOODS"},
                {"value": "Coxa Seara Brasil", "label": "Coxa Seara Brasil"},
                {"value": "Chouriço Corrente 155", "label": "Chouriço Corrente"},
                {"value": "Entrecosto Especial", "label": "Entrecosto Especial"},
                {"value": "ENTRECOSTO DE PORCO (PERDIX) ", "label": "Entrecosto de porco (PERDIX)"},
                {"value": "Figado de Vaca", "label": "Figado de Vaca"},
                {"value": "Frango 1.200g", "label": "Frango 1.200g"},
                {"value": "Tomate Maduro Nacional", "label": "Tomate Maduro Nacional"},
                {"value": "Óleo Fula Soja", "label": "Óleo Fula Soja"},
                {"value": "VINAGRE PRIMAVERA 500ML", "label": "VINAGRE PRIMAVERA 500ML"},
                # banana pão
            ],
            style={"width": 150},
            ),

    ], id="parameters-components"),
    ], id="factors-components"),
     dcc.Loading(children=[
        html.Div(
            [
                html.Div(id='predition-results',style={"display":"flex","flexDirection":"column","gap":"15px"}),
                html.Div(id='holidays-results'),
            ], style={"background":"#F5F5F6", "padding":"10px 0", "height":"55vh"},),
        ], color="#2B454E", type="dot", fullscreen=False,),
       
])



@callback(Output('panelForecast-dataset-multi-select', component_property='value'),
          Output('panelForecast-dataset-multi-select', component_property='data'),
                Input('interval_db', component_property='n_intervals'),
                #Input('panelForecast-dataset-multi-select','id')
              )
def SetDataValuesOnCompont(interval_db):
    value = PanelMultiSelectOptions
    return value, DatasetValues()[1]


def DatasetValues():
    data = []
    DatasetsNames = GetAllCollectionNames()
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
    State('country-name-select','value'),
    State('fourier-number','value'),
    State('fourier-month-number','value'),
    State('seasonality-mode-select','value'),
    State('product-select','value'),
    State('forecast-date','value'),
)
def set_forecast(factorsSeleted, externarFactors, nclicks, country_name, fourier, fourier_monthly, seasonality_mode, product, date):
    
    if nclicks is not None:
        global figures
        figures = []
        Holidays = pd.DataFrame()
        Weather = pd.DataFrame()
        Inflation = pd.DataFrame()
        Dataset = getColections(PanelMultiSelectOptions)
        Dataset = Dataset[Dataset['Product']==product]
        Dataset = cleanDataset(Dataset)
        Selected_date = datetime.strptime(date, '%Y-%m-%d')
        Last_df_date = datetime.strptime(Dataset['Date'].max(), '%Y-%m-%d')
        Lenght = abs((Selected_date - Last_df_date).days)
        global df_predition
        
        for sFactor in factorsSeleted:
            if(sFactor == 'schoolholiday' or sFactor == 'covid_19'):
                if(sFactor == 'schoolholiday'):
                    Holidays = pd.concat((Holidays, pd.read_csv('data/school_holiday.csv'))) 
                if(sFactor == 'covid_19'):
                    Holidays = pd.concat((Holidays, pd.read_csv('data/covid_19.csv'))) 

            elif(sFactor == 'weather'):
                Dataset.loc[:, 'Weather'] = Dataset['Date'].apply(future_weather)
            elif(sFactor == 'inflation_eur'):
                Dataset.loc[:, 'Inflation_euro'] = Dataset['Date'].apply(future_euro_inflation)
            elif(sFactor == 'inflation_usd'):
                Dataset.loc[:, 'Inflation_dolar'] = Dataset['Date'].apply(future_usd_inflation)
        
        if 'Weather' in Dataset.columns or 'Inflation_euro' in  Dataset.columns or 'Inflation_dolar' in  Dataset.columns:
            df_original, df_predition, model = configs.sales_predition_Weather(Dataset,Holidays, Lenght, country_name, fourier, fourier_monthly, seasonality_mode)
         #   print(df_original.head(200)['y'])
          #  print( df_predition.head(200)['yhat'])

            #mape = mean_absolute_percentage_error(df_original.head(230)['y'], df_predition.head(230)['yhat'])
            #print("MAPE: {:.2f}%".format(mape*100))
            if 'Weather' in df_predition:
                Weather_regressor = dcc.Graph(
                id='regressors-plot',
                figure={
                    'data': [
                        {'x': df_predition['ds'], 'y': df_predition[f'Weather'], 'type': 'line'}
                    ],
                    'layout': {
                        'title': 'Regressores (Clima)',
                        'xaxis': {'title': 'Data'},
                        'yaxis': {'title': 'Clima'}
                    }
                }
                )

            if 'Inflation_euro' in df_predition:
                Inflation_Euro_regressor = dcc.Graph(
                id='regressors-plot',
                figure={
                    'data': [
                        {'x': df_predition['ds'], 'y': df_predition[f'Inflation_euro'], 'type': 'line'}
                    ],
                    'layout': {
                        'title': 'Regressores (Inflação - Euro)',
                        'xaxis': {'title': 'Data'},
                        'yaxis': {'title': 'Euro'}
                    }
                }
                )
                
            if 'Inflation_dolar' in df_predition:
                Inflation_Dolar_regressor = dcc.Graph(
                id='regressors-plot',
                figure={
                    'data': [
                        {'x': df_predition['ds'], 'y': df_predition[f'Inflation_dolar'], 'type': 'line'}
                    ],
                    'layout': {
                    'title': 'Regressores (Inflação - Dólar)',
                    'xaxis': {'title': 'Data'},
                    'yaxis': {'title': 'Dolar'}
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

        fig3 = px.line(df_predition, x='ds', y='trend', color='trend', symbol="trend", title='Tendência')
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

        returned_items = [Predition_graph, seasonality, fig3_graph]
        if 'Weather' in Dataset.columns:
            returned_items.insert(1, Weather_regressor)
            #return [Predition_graph, Weather_regressor, seasonality, fig3_graph], HolidaysTabs
        if 'Inflation_euro' in Dataset.columns:
            returned_items.insert(1, Inflation_Euro_regressor)
            #return [Predition_graph, Inflation_Euro_regressor, seasonality, fig3_graph], HolidaysTabs
        if 'Inflation_dolar' in Dataset.columns:
            returned_items.insert(1, Inflation_Dolar_regressor)
            
        
        return returned_items, HolidaysTabs
    else:
        return html.Div('Realize sua previsão aqui!', id="predition-banner"), html.Div()


def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, GetCollectionByName(name)))
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

def cleanDataset(sales_df):
    aggregated_data = sales_df.groupby('Date')['Quantity'].sum().reset_index()
    sales_df = pd.DataFrame(aggregated_data)

    q1_qntd = sales_df.Quantity.quantile(.25)
    q3_qntd = sales_df.Quantity.quantile(.75)
    IQR_price = q3_qntd - q1_qntd

    # Setting the limits
    sup_qntd = q3_qntd + 1.5*IQR_price
    inf_qntd = q1_qntd - 1.5*IQR_price

    sales_df.drop(sales_df[sales_df.Quantity > sup_qntd].index,axis =0, inplace = True)
    return sales_df

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