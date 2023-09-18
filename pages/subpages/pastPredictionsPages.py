from datetime import datetime
from dash import html, callback, Input, Output, dcc, dash_table
import pandas as pd
from api.clientApp import GetAllCollectionNames, GetCollectionByName
from api.externalFactors import future_euro_inflation, future_usd_inflation, future_weather
from data.configs import sales_predition_Weather
import dash_mantine_components as dmc

DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]

pastPredictions = html.Div([
    dcc.Store(id='dataset-sales-Insight-storage', storage_type='local'),
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Previsões anteriores', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Aqui você poderá visualizar todas as previsões já realizadas', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ]),
                    dmc.MultiSelect(
                        label="",
                        placeholder="Selecione seus conjuntos de dados!",
                        id="panelInsight-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[],
                        style={"width": 400, "fontSize":"1.2rem"},
                        ),
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    html.Div([
        html.P("Mostrar dados do arquivo",style={"font":"1.8rem Nunito"}, id='wrapper-result')
    ], style={"background":"#c4c4c4","width":"100%","height":"76vh"})
], style={"display":"flex", "gap":"10px", "justifyContent":"space-between","alignItems":"center", "height":"76vh", "background":"#F0F0F0"}),
])


@callback(Output('panelInsight-dataset-multi-select', component_property='value'),
          Output('panelInsight-dataset-multi-select', component_property='data'),
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
    Output('dataset-sales-Insight-storage', 'data', allow_duplicate=True),
    Input("panelInsight-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions


@callback(
    Output('wrapper-result', 'children'),
    Input('interval_db', component_property='n_intervals'),
    Input("panelInsight-dataset-multi-select", "value"),
)
def hanldleInsight(_,__):
    
    Produts = ['Água Pura 5L','Abacate Nacional','Asa de Frango 10Kg',
               'Batata Rena Nacional','Batata Doce Nacional','Cebola Nacional',
               'COXA USA KOCH FOODS','Coxa Seara Brasil','Entrecosto Especial',
               'ENTRECOSTO DE PORCO (PERDIX) ','Figado de Vaca','Frango 1.200g',
               'Tomate Maduro Nacional','Óleo Fula Soja',
               'Peixe Corvina','Peixe Carapau',
               'VINAGRE PRIMAVERA 500ML']
    Holidays = pd.DataFrame()
    Df_Table = pd.DataFrame()
    
    Holidays = pd.concat((Holidays, pd.read_csv('data/school_holiday.csv'))) 
    Holidays = pd.concat((Holidays, pd.read_csv('data/covid_19.csv')))
    
    for produt in Produts:
        
        Dataset = getColections(PanelMultiSelectOptions)
        Dataset = Dataset[Dataset['Product']== produt]
        Dataset = cleanDataset(Dataset)      
        
        Dataset.loc[:, 'Weather'] = Dataset['Date'].apply(future_weather)
        Dataset.loc[:, 'Inflation_euro'] = Dataset['Date'].apply(future_euro_inflation)
        Dataset.loc[:, 'Inflation_dolar'] = Dataset['Date'].apply(future_usd_inflation)

        Final_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
        Intial_date = datetime.strptime(Dataset['Date'].max(), '%Y-%m-%d')
        period = abs((Final_date - Intial_date).days)
        
        Lenght = period
        country_name = 'AO'
        fourier = 10
        fourier_monthly = 5
        seasonality_mode = 'additive'
        
        df_original, df_predition, model = sales_predition_Weather(Dataset,Holidays, Lenght, country_name, fourier, fourier_monthly, seasonality_mode)

        df = df_predition[df_predition.ds == Final_date]
        df = df[['ds','school_holiday','COVID_19','Weather','Inflation_euro','Inflation_dolar']]
        df = df.rename(columns={'ds':'Data','school_holiday':'Feriado Escolar',
                                'COVID_19':'Covid 19','Weather':'Temperatura Climática',
                                'Inflation_euro':'Euro', 'Inflation_dolar':'Dolar'})
        
        df['Produto'] = produt
        
        Df_Table = pd.concat((Df_Table, df))

    return dash_table.DataTable(Df_Table.to_dict('records'), [{"name": i, "id": i} for i in Df_Table.columns])

def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, GetCollectionByName(name)))
    return df_PD




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