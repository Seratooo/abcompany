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
            dmc.Button("Gerar relatório", id='generate-report', style={'display':'none'}),
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
                        {"value": "tasks", "label": "Tarefas Realizadas"},
                        {"value": "promo", "label": "Promoções Realizadas"},


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
                #{"value": "Água Pura 5L", "label": "Água Pura 5L"},
                {"value": "Abacate Nacional", "label": "Abacate Nacional"},
                {"value": "Asa de Frango 10Kg", "label": "Asa de Frango 10Kg"},
                {"value": "Peixe Carapau", "label": "Peixe Carapau"},
                #{"value": "Peixe Corvina", "label": "Peixe Corvina"},
                #{"value": "Peixe Pescada", "label": "Peixe Pescada"},
                {"value": "Batata Rena Nacional", "label": "Batata Rena Nacional"},
                {"value": "Batata Doce Nacional", "label": "Batata Doce Nacional"},
                {"value": "Cebola Nacional", "label": "Cebola Nacional"},
                {"value": "COXA USA KOCH FOODS", "label": "COXA USA KOCH FOODS"},
                {"value": "Coxa Seara Brasil", "label": "Coxa Seara Brasil"},
                {"value": "Chouriço Corrente 155", "label": "Chouriço Corrente"},
                {"value": "Entrecosto Especial", "label": "Entrecosto Especial"},
                {"value": "ENTRECOSTO DE PORCO (PERDIX) ", "label": "Entrecosto de porco (PERDIX)"},
                #{"value": "Figado de Vaca", "label": "Figado de Vaca"},
                {"value": "Frango 1.200g", "label": "Frango 1.200g"},
                {"value": "Tomate Maduro Nacional", "label": "Tomate Maduro Nacional"},
                #{"value": "Óleo Fula Soja", "label": "Óleo Fula Soja"},
                #{"value": "VINAGRE PRIMAVERA 500ML", "label": "VINAGRE PRIMAVERA 500ML"},
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
        ], color="var(--primary)", type="dot", fullscreen=False,),
       
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
        df_ProductInterest = pd.read_csv(f'data/trends/{product}.csv')
        df_task = pd.read_csv('data/df_task.csv')
        df_promo = pd.read_csv('data/df_promo.csv')
        returned_items = []
        global df_predition
        
        for sFactor in factorsSeleted:
            if(sFactor == 'schoolholiday' or sFactor == 'covid_19' or sFactor == 'tasks' or sFactor == 'promo'):
                if(sFactor == 'schoolholiday'):
                    Holidays = pd.concat((Holidays, pd.read_csv('data/school_holiday.csv')))
                    Holidays = Holidays.drop('Unnamed: 0', axis=1)
                if(sFactor == 'covid_19'):
                    Holidays = pd.concat((Holidays, pd.read_csv('data/covid_19.csv')))
                    Holidays = Holidays.drop('Unnamed: 0', axis=1)
                if(sFactor == 'tasks'):
                    df_task_ = df_task[['Date', 'Name']].rename(columns = {'Date': 'ds', 'Name':'holiday'})
                    Holidays = pd.concat((Holidays, df_task_))
                if(sFactor == 'promo'):
                    df_promo_ = df_promo[['Date', 'Name']].rename(columns = {'Date': 'ds', 'Name':'holiday'})
                    Holidays = pd.concat((Holidays, df_promo_))

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
            df_predition = df_predition.sort_values(by='ds')
            if 'Weather' in df_predition:
                
                figWeather = go.Figure()
                figWeather.update_layout(
                    title='Impacto das alterações climáticas nas Vendas',
                )
                
                figWeather.add_trace(
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition['Weather']*100,
                        fill='tozeroy',
                        mode='lines',
                        name='Impacto nas vendas',
                        line=dict(color='#636EFA')
                    )
                )

                WeatherDataset = pd.read_csv('data/df_weather.csv')
                WeatherDataset = WeatherDataset.sort_values(by='Date')
                WeatherDataset['Date'] = pd.to_datetime(WeatherDataset['Date'])
                WeatherDataset = WeatherDataset[(WeatherDataset.Date >=df_predition['ds'].min()) & (WeatherDataset.Date <=df_predition['ds'].max())]
                
                figWeather.add_trace(
                    go.Scatter(
                        x=WeatherDataset['Date'],
                        y=WeatherDataset['Weather'],
                        fill='tonexty',
                        mode='lines',
                        name='Temperatura Climática',
                        line=dict(color='#F7AA9D')
                    )
                )


                Weather_regressor = dcc.Graph(
                id='regressors-plot-weather',
                figure=figWeather
                )

            if 'Inflation_euro' in df_predition:
                figEUR = go.Figure()
                figEUR.update_layout(
                    title='Impacto do Euro nas Vendas',
                )
                figEUR.add_trace(
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition['Inflation_euro']*5000,
                        fill='tozeroy',
                        mode='lines',
                        name='Impacto nas vendas',
                        line=dict(color='#636EFA')
                    )
                )
                
                EurDataset = pd.read_csv('data/df_eur.csv')
                EurDataset = EurDataset.sort_values(by='ds')
                EurDataset['ds'] = pd.to_datetime(EurDataset['ds'])
                EurDataset = EurDataset[(EurDataset.ds >=df_predition['ds'].min()) & (EurDataset.ds <=df_predition['ds'].max())]
                figEUR.add_trace(
                    go.Scatter(
                        x=EurDataset['ds'],
                        y=EurDataset['Valor'],
                        fill='tonexty',
                        mode='lines',
                        name='Taxa de cambio (EURO)',
                        line=dict(color='#F7AA9D')
                    )
                )

                Inflation_Euro_regressor =  dcc.Graph(
                id='regressors-plot-eur',
                figure=figEUR
                )
                
            if 'Inflation_dolar' in df_predition:

                figUSD = go.Figure()
                figUSD.update_layout(
                    title='Impacto do USD nas Vendas',
                )
                figUSD.add_trace(
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition['Inflation_dolar']*5000,
                        fill='tozeroy',
                        mode='lines',
                        name='Impacto nas vendas',
                        line=dict(color='#636EFA')
                    )
                )
                
                UsdDataset = pd.read_csv('data/df_eur.csv')
                UsdDataset = UsdDataset.sort_values(by='ds')
                UsdDataset['ds'] = pd.to_datetime(UsdDataset['ds'])
                UsdDataset = UsdDataset[(UsdDataset.ds >=df_predition['ds'].min()) & (UsdDataset.ds <=df_predition['ds'].max())]
                figUSD.add_trace(
                    go.Scatter(
                        x=UsdDataset['ds'],
                        y=UsdDataset['Valor'],
                        fill='tonexty',
                        mode='lines',
                        name='Taxa de cambio (USD)',
                        line=dict(color='#F7AA9D')
                    )
                )

                Inflation_Dolar_regressor = dcc.Graph(
                id='regressors-plot-usd',
                figure=figUSD
                )          
        else:
            df_original, df_predition, model = configs.sales_predition_v2(Dataset,Holidays, Lenght, country_name, fourier, fourier_monthly, seasonality_mode)

        
        
        fig = px.line(df_predition, x='ds', y='yhat', title='Previsões de Vendas')
        figInt = go.Figure() #px.line(df_ProductInterest, x='Semana', y=f'{product}', title='Interesse das pessoas pelo produto')
        figInt.update_layout(
            title=f'Interesse das pessoas pelo produto: {product}',
            #xaxis_title='Título do Eixo X',  # Opcional: título do eixo X
            yaxis_title=f'{product}'   # Opcional: título do eixo Y
        )
        figInt.add_trace(
                    go.Scatter(
                        x=df_ProductInterest['Semana'],
                        y=df_ProductInterest[f'{product}'],
                        fill='tonexty',
                        mode='lines',
                        name='Interesse',
                    )
                )
        
        FigPredict = go.Figure()
        FigPredict.add_trace(go.Indicator(
            mode = "number+delta",
            value = df_predition[pd.DatetimeIndex(df_predition.ds).year > 2022]['yhat'].mean(),
            title = {"text": f"<span style='font-size:2.4rem'>Média de vendas prevista</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média anual de 2022</span>"},
            delta = {'reference': df_predition[pd.DatetimeIndex(df_predition.ds).year == 2022]['yhat'].mean(), 'relative': True, 'valueformat': '.1%'},
            domain = {'x': [0, 0.33], 'y': [0.5, 1]}))
        
        PredictIndicators = handleSazonality(df_predition, 2023)
        FigPredict.add_trace(go.Indicator(
            mode = "gauge+number",
            value = PredictIndicators[1],
            domain = {'x': [0.33, 0.66], 'y': [0.5, 1]},
            title = {'text': f"Alta prevista em {PredictIndicators[0]}"}
            ))
        FigPredict.add_trace(go.Indicator(
            mode = "gauge+number",
            value = PredictIndicators[3],
            domain = {'x': [0.66, 1], 'y': [0.5, 1]},
            title = {'text': f"Baixa prevista em {PredictIndicators[2]}"},
            gauge = {'bar': {'color': 'red'}}
            ))
        PredictTab = dcc.Graph(
                id='regressors-plot-predict',
                figure=FigPredict
            )          

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
        Interesting_graph =  dcc.Graph(
            id='graphInt',
            figure=figInt
        )

        
        InterestResults = handleInterest(df_ProductInterest, df_original, 2020, product)
        figInd = go.Figure()
        figInd.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults[2],
                    title = {"text": f"<span style='font-size:2.4rem'>Maior interesse em {InterestResults[4]}/{2020}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults[0], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0, 0.5], 'y': [0.5, 1]}))
        figInd.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults[3],
                    title = {"text": f"<span style='font-size:2.4rem'>Media vendas em {InterestResults[4]}/{2020}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults[1], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0.6, 1], 'y': [0.5, 1]}))
        Indicator_01 = dcc.Graph(
            id='graphInd',
            figure=figInd
        )

        InterestResults2 = handleInterest(df_ProductInterest, df_original, 2021, product)
        figInd2 = go.Figure()
        figInd2.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults2[2],
                    title = {"text": f"<span style='font-size:2.4rem'>Maior interesse em {InterestResults2[4]}/{2021}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults2[0], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0, 0.5], 'y': [0.5, 1]}))
        figInd2.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults2[3],
                    title = {"text": f"<span style='font-size:2.4rem'>Media vendas em {InterestResults2[4]}/{2021}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults2[1], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0.6, 1], 'y': [0.5, 1]}))
        Indicator_02 = dcc.Graph(
            id='graphInd',
            figure=figInd2
        )

        InterestResults3 = handleInterest(df_ProductInterest, df_original, 2022, product)
        figInd3 = go.Figure()
        figInd3.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults3[2],
                    title = {"text": f"<span style='font-size:2.4rem'>Maior interesse em {InterestResults3[4]}/{2022}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults3[0], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0, 0.5], 'y': [0.5, 1]}))
        figInd3.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = InterestResults3[3],
                    title = {"text": f"<span style='font-size:2.4rem'>Media vendas em {InterestResults3[4]}/{2022}</span><br><span style='font-size:1.2rem;color:gray'>Em relação a média</span>"},
                    delta = {'reference': InterestResults3[1], 'relative': True, 'valueformat': '.1%'},
                    domain = {'x': [0.6, 1], 'y': [0.5, 1]}))
        Indicator_03 = dcc.Graph(
            id='graphInd',
            figure=figInd3
        )

        IndicatorTab = dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab("Interesse X Vendas (2020)", value="2020"),
                    dmc.Tab("Interesse X Vendas (2021)", value="2021"),
                    dmc.Tab("Interesse X Vendas (2022)", value="2022"),
                ]
            ),
            dmc.TabsPanel(Indicator_01, value="2020"),
            dmc.TabsPanel(Indicator_02, value="2021"),
            dmc.TabsPanel(Indicator_03, value="2022"),
        ],
        color="green",
        value='2020',
        orientation="horizontal",
        )

        
        MyHolidays = []
        MyHolidays.append(dcc.Tab(label='Feriados Nacionais', value='holiday'))
        for hday in model.train_holiday_names:
            MyHolidays.append(dcc.Tab(label=hday, value=f'{hday}'))
        
        HolidaysTabs = [
            dcc.Tabs(id="tabs-holiday", value='holiday', children=MyHolidays),
            html.Div(id='tabs-content-holiday-graph')
        ]

        fig3 = px.line(df_predition, x='ds', y='trend', color='trend', symbol="trend", title=f'Tendência do produto: {product}')
        fig3_graph = dcc.Graph(
            id='graph13',
            figure=fig3
        )
        figures.append(fig3)
        
        yearly_seasonality_fig = go.Figure(
            data=[
                go.Scatter(x=df_predition['ds'], y=df_predition['yearly'], mode='lines+markers', fill='none', line=dict(color='#636EFA'))
            ],
            layout=go.Layout(
                title='Sazonalidade Anual',
                #xaxis={'title': 'Data'},
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
                    #'xaxis': {'title': 'Data'},
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
                    #'xaxis': {'title': 'Data'},
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

        SazonalityIndicators = handleSazonality(df_predition, 2020)
        figSZ_01 = go.Figure()
        
        figSZ_01.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators[1],
            domain = {'x': [0, 0.5], 'y': [0.5, 1]},
            title = {'text': f"Alta em {SazonalityIndicators[0]}"}
            ))
        figSZ_01.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators[3],
            domain = {'x': [0.6, 1], 'y': [0.5, 1]},
            title = {'text': f"Baixa em {SazonalityIndicators[2]}"},
            gauge = {'bar': {'color': 'red'}}
            ))
        
        IndicatorSZ_01 = dcc.Graph(
            id='graphInd',
            figure=figSZ_01
        )

        SazonalityIndicators2 = handleSazonality(df_predition, 2021)
        figSZ_02 = go.Figure()
        
        figSZ_02.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators2[1],
            domain = {'x': [0, 0.5], 'y': [0.5, 1]},
            title = {'text': f"Alta em {SazonalityIndicators2[0]}"}
            ))
        figSZ_02.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators2[3],
            domain = {'x': [0.6, 1], 'y': [0.5, 1]},
            title = {'text': f"Baixa em {SazonalityIndicators2[2]}"},
            gauge = {'bar': {'color': 'red'}}
            ))
        
        IndicatorSZ_02 = dcc.Graph(
            id='graphInd',
            figure=figSZ_02
        )

        SazonalityIndicators3 = handleSazonality(df_predition, 2022)
        figSZ_03 = go.Figure()
        
        figSZ_03.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators3[1],
            domain = {'x': [0, 0.5], 'y': [0.5, 1]},
            title = {'text': f"Alta em {SazonalityIndicators3[0]}"}
            ))
        figSZ_03.add_trace(go.Indicator(
            mode = "gauge+number",
            value = SazonalityIndicators3[3],
            domain = {'x': [0.6, 1], 'y': [0.5, 1]},
            title = {'text': f"Baixa em {SazonalityIndicators3[2]}"},
            gauge = {'bar': {'color': 'red'}}
            ))
        
        IndicatorSZ_03 = dcc.Graph(
            id='graphInd',
            figure=figSZ_03
        )

        SazonalityTab = dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab("2020", value="2020"),
                    dmc.Tab("2021", value="2021"),
                    dmc.Tab("2022", value="2022"),
                ]
            ),
            dmc.TabsPanel(IndicatorSZ_01, value="2020"),
            dmc.TabsPanel(IndicatorSZ_02, value="2021"),
            dmc.TabsPanel(IndicatorSZ_03, value="2022"),
        ],
        color="green",
        value='2020',
        orientation="horizontal",
        )

        CompetitionFig = go.Figure()
        SociaTrend = pd.read_csv('data/trends/Socia.csv')
        SociaTrend = SociaTrend[pd.to_datetime(SociaTrend.Semana) < df_predition['ds'].max()]
        
        CompetitionFig.update_layout(
            title='Interesse pela SOCIA em relação ao interesse pela concorrência',
            #xaxis_title='Título do Eixo X',  # Opcional: título do eixo X
            yaxis_title='Impacto no mercado'   # Opcional: título do eixo Y
        )
        CompetitionFig.add_trace(
            go.Scatter(
                x=SociaTrend['Semana'],
                y=SociaTrend['Socia'],
                mode='lines+markers',
                name='Socia',
                fill='tonexty',
                line=dict(color='blue'),
            )
        )
        Competidor1 = pd.read_csv('data/trends/Mamboo.csv')
        Competidor1 = Competidor1[pd.to_datetime(Competidor1.Semana) < df_predition['ds'].max()]
        CompetitionFig.add_trace(
            go.Scatter(
                x=Competidor1['Semana'],
                y=Competidor1['Mamboo'],
                mode='none',
                name='Competidor 1',
                fill='tozeroy',
            )
        )

        Competidor2 = pd.read_csv('data/trends/Tupuca.csv')
        Competidor2 = Competidor2[pd.to_datetime(Competidor2.Semana) < df_predition['ds'].max()]
        CompetitionFig.add_trace(
            go.Scatter(
                x=Competidor2['Semana'],
                y=Competidor2['Tupuca'],
                mode='none',
                name='Competidor 2',
                fill='tozeroy',
            )
        )

        Competidor3 = pd.read_csv('data/trends/MeuMerkado.csv')
        Competidor3 = Competidor3[pd.to_datetime(Competidor3.Semana) < df_predition['ds'].max()]
        CompetitionFig.add_trace(
            go.Scatter(
                x=Competidor3['Semana'],
                y=Competidor3['MeuMerkado'],
                mode='none',
                name='Competidor 3',
                fill='tozeroy',
            )
        )

        CompetitonElement = dcc.Graph(
            id='graphCompetition',
            figure=CompetitionFig
        )

        FigTasks = go.Figure()
        FigTasks.update_layout(
            title='Impacto dos Factores Internos nas vendas em %',
            #xaxis_title='Título do Eixo X',  # Opcional: título do eixo X
            #yaxis_title='Impacto no mercado'   # Opcional: título do eixo Y
        )
        tasks = list(df_task['Name'].unique())
        if all(col in df_predition.columns for col in tasks):
            for task in tasks:
                FigTasks.add_trace(
                go.Scatter(
                    x=df_predition['ds'],
                    y=df_predition[task]*100,
                    mode='lines',
                    fill='toself',
                    name=f'{task}',
                ))
        
        promos = list(df_promo['Name'].unique())
        if all(col in df_predition.columns for col in promos):
            for promo in promos:
                FigTasks.add_trace(
                go.Scatter(
                    x=df_predition['ds'],
                    y=df_predition[promo]*100,
                    fill='toself',
                    mode='lines',
                    name=f'{promo}',
                ))
        TaskElement = dcc.Graph(
            id='graphTask',
            figure=FigTasks
        )

        PriceFig = go.Figure()
        PriceFig.update_layout(
            title='Preço praticado em relação quantidade vendida',
            #xaxis_title='Título do Eixo X',  # Opcional: título do eixo X
            #yaxis_title='Impacto no mercado'   # Opcional: título do eixo Y
        )
        PriceFig.add_trace(
                go.Scatter(
                    x=Dataset['Date'],
                    y=Dataset['Price'],
                    fill='tonexty',
                    mode='lines',
                    name=f'Preço Praticado',
                    line=dict(color='#008000')
                ))
        PriceFig.add_trace(
                go.Scatter(
                    x=Dataset['Date'],
                    y=Dataset['Quantity']*100,
                    fill='tozeroy',
                    mode='lines',
                    name=f'Quantidade vendida',
                    line=dict(color='#636EFA')
                ))
        
        PriceElement = dcc.Graph(
            id='graphPrice',
            figure=PriceFig
        )
        
    
        
        HolidayFig = go.Figure()
        HolidayFig.update_layout(
            title='Impacto dos feriados e eventos personalizados',
            yaxis_title='Impacto do evento (%)'   # Opcional: título do eixo Y
        )
        for holyName in model.train_holiday_names:
            if holyName not in promos and holyName not in tasks:
                HolidayFig.add_trace(
                    go.Scatter(
                        x=df_predition['ds'],
                        y=df_predition[f'{holyName}']*100,
                    # fill='none',
                        mode='lines+markers',
                        fill='toself',
                        name=f'{holyName}',
                    ))
        HolydayElement = dcc.Graph(
            id='graphHoly',
            figure=HolidayFig
        )

        returned_items = [Predition_graph, PredictTab, Interesting_graph, IndicatorTab, seasonality,SazonalityTab, fig3_graph, PriceElement, TaskElement, HolydayElement, CompetitonElement]
        if 'Weather' in Dataset.columns:
            returned_items.insert(2, Weather_regressor)
            #return [Predition_graph, Weather_regressor, seasonality, fig3_graph], HolidaysTabs
        if 'Inflation_euro' in Dataset.columns:
            returned_items.insert(2, Inflation_Euro_regressor)
            #return [Predition_graph, Inflation_Euro_regressor, seasonality, fig3_graph], HolidaysTabs
        if 'Inflation_dolar' in Dataset.columns:
            returned_items.insert(2, Inflation_Dolar_regressor)
            
        
        return returned_items, html.Div() #HolidaysTabs
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
    aggregated_data = sales_df.groupby('Date')['Quantity','Price'].sum().reset_index()
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
    

def handleInterest(df_ProductInterest, df_vendasReais, Year, Product):
  df_vendasReais = df_vendasReais[pd.DatetimeIndex(df_vendasReais.ds).year == Year]
  df_byYear = df_ProductInterest[df_ProductInterest.Ano == Year]

  month_map = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
  
  SemanaMaior = int(df_byYear[df_byYear[Product]==df_byYear[Product].max()]['Mes'].iloc[:1])
  result = df_byYear[df_byYear.Mes == SemanaMaior].mean()
  
  return [df_byYear[Product].mean(), df_vendasReais['y'].mean(), float(result[Product]), df_vendasReais[pd.DatetimeIndex(df_vendasReais.ds).month == SemanaMaior]['y'].mean(), month_map[SemanaMaior]]


def handleSazonality(df, Year):
    df_year = df[pd.DatetimeIndex(df.ds).year == Year]
    month_map = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    max_date = pd.to_datetime(df_year[df_year.yearly == df_year['yearly'].max()]['ds'].values[0])
    max_date = f"{month_map[max_date.month]}/{str(max_date.day)}"
    max_value = float(df_year[df_year.yearly == df_year['yearly'].max()]['yearly'].values[0]) * 100
    
    min_date = pd.to_datetime(df_year[df_year.yearly == df_year['yearly'].min()]['ds'].values[0])
    min_date = f"{month_map[min_date.month]}/{str(min_date.day)}"
    min_value = float(df_year[df_year.yearly == df_year['yearly'].min()]['yearly'].values[0]) * 100
    
    return max_date, max_value, min_date, min_value