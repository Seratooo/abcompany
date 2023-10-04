from datetime import date, datetime
import holidays
import pandas as pd
from meteostat import Point, Daily
import pandas_datareader.data as web
import eurostat
import requests
import os

us_holidays = holidays.AO()
LuandaPoint = Point(-8.838333, 13.234444, 70)

def GetHolidaysByYear(Year):
    df = pd.DataFrame(holidays.AO(years=Year).items())
    df.rename(columns={0: 'ds'}, inplace=True)
    df.rename(columns={1: 'holiday'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    df_st = df.copy()
    df_st['holiday'] = 'state_holiday'
    df.sort_values('ds', inplace=True)
    return df_st, df


def GetWeatherByYear(Year):
    start = datetime(Year, 1, 1)
    end = datetime(Year, 12, 31)
    df = Daily(LuandaPoint, start, end)
    df = df.fetch()
    df_reduzido = df.iloc[:, :3].copy()
    df_reduzido.index.name = 'ds'
    df_reduzido.rename(columns={'tavg': 'Temperatura média'}, inplace=True)
    df_reduzido.rename(columns={'tmin': 'Temperatura mínima'}, inplace=True)
    df_reduzido.rename(columns={'tmax': 'Temperatura máxima'}, inplace=True)
    df_reduzido.sort_values('ds', inplace=True)
    df_reduzido.index = pd.to_datetime(df.index)
    
    data = df_reduzido.iloc[:, :1].copy()
    data['Date'] = data.index
    data.rename(columns={'Temperatura média': 'Weather'}, inplace=True)
    return data, df_reduzido.copy()


def GetWeatherByDay(_start, _end):
    start = pd.to_datetime(_start)
    end = pd.to_datetime(_end)
    df = Daily(LuandaPoint, start, end)
    df = df.fetch()
    df_reduzido = df.iloc[:, :3].copy()
    df_reduzido.index.name = 'ds'
    df_reduzido.rename(columns={'tavg': 'Temperatura média'}, inplace=True)
    df_reduzido.rename(columns={'tmin': 'Temperatura mínima'}, inplace=True)
    df_reduzido.rename(columns={'tmax': 'Temperatura máxima'}, inplace=True)
    df_reduzido.sort_values('ds', inplace=True)
    df_reduzido.index = pd.to_datetime(df.index)
    
    data = df_reduzido.iloc[:, :1].copy()
    data['Date'] = data.index
    data.rename(columns={'Temperatura média': 'Weather'}, inplace=True)
    return data, df_reduzido.copy()

# def GetPIB_ByYear(Year):
#     start_time = datetime(2021, 1, 1) 
#     end_time = datetime(2021, 12, 31)
#     df = web.DataReader('TUD', 'oecd', start_time, end_time)
#     print(df)


def GetInflationByYear(Year):
    myFilters = {'startPeriod': f'{Year}-01', 'endPeriod': f'{Year}-12', 'FREQ': ['M'], 'geo': ['US','EU'], 'coicop':['cp00']}
    data  =  eurostat.get_data_df( 'PRC_HICP_MANR',filter_pars=myFilters ) 
    data = data.iloc[:, 4:].copy()
    df = data.T
    df.index.name = 'ds'
    df.rename(columns={0: 'Dolar'}, inplace=True)
    df.rename(columns={1: 'Euro'}, inplace=True)
    df.index = pd.to_datetime(df.index)
    df_Eur = df.iloc[:, 1:].copy()
    df_Dol = df.iloc[:, :1].copy()
    
    return df_Dol, df_Eur, df

def GetInflationByYear_V2(ds):
    date = pd.to_datetime(ds)
    mes = f'0{date.month}' if date.month < 10 else date.month
    ano = date.year
    myFilters = {'startPeriod': f'{ano}-{mes}', 'endPeriod': f'{ano}-{mes}', 'FREQ': ['M'], 'geo': ['US','EU'], 'coicop':['cp00']}
    data  =  eurostat.get_data_df( 'PRC_HICP_MANR',filter_pars=myFilters ) 
    data = data.iloc[:, 4:].copy()
    df = data.T
    df.index.name = 'ds'
    df.rename(columns={0: 'Dolar'}, inplace=True)
    df.rename(columns={1: 'Euro'}, inplace=True)
    df.index = pd.to_datetime(df.index)
    df_Eur = df.iloc[:, 1:].copy()
    df_Dol = df.iloc[:, :1].copy()
    
    return df_Dol, df_Eur, df

def future_weather(ds):
    _date = pd.to_datetime(ds).strftime('%Y-%m-%d')
    df_weather = pd.read_csv('data/df_weather.csv')
    data_atual = date.today()
    data_formatada = data_atual.strftime('%Y-%m-%d')

    if not df_weather[df_weather.Date == data_formatada]['Weather'].values:
        future_weather = GetWeatherByDay(data_formatada, data_formatada)[0]
        has_value = future_weather['Weather'].notnull().any()
        if has_value:
            Weather = float(future_weather['Weather'])
            if Weather is not None and int(Weather) > 0:
                new_element = {
                'time': data_formatada,
                'Date': data_formatada,
                'Weather': Weather,
                }
                df_weather = pd.concat([df_weather, pd.DataFrame([new_element])], ignore_index=True)
                df_weather.to_csv('data/df_weather.csv')
    try:
        return df_weather[df_weather.Date == _date]['Weather'].values[0]
    except:
        return 0.0

def future_euro_inflation(ds):
    ds = pd.to_datetime(ds).strftime('%Y-%m-%d')
    data_atual = date.today()
    data_formatada = data_atual.strftime('%Y-%m-%d')
    df_eur = pd.read_csv('data/df_eur.csv')

    # if not df_eur[df_eur.ds == data_formatada]['Valor'].values:
    #     currency = float(getCurrency('EUR','EURAOA',data_formatada))
    #     if currency>0:             
    #         new_element = {
    #             'ds': data_formatada,
    #             'Valor': currency,
    #         }
    #         df_eur = pd.concat([df_eur, pd.DataFrame([new_element])], ignore_index=True)
    #         df_eur = df_eur.drop('Unnamed: 0', axis=1)
    #         df_eur.to_csv('data/df_eur.csv')
    try:
        return df_eur[df_eur.ds == ds]['Valor'].values[0]
    except:
        return 0.0


def future_usd_inflation(ds):
    ds = pd.to_datetime(ds).strftime('%Y-%m-%d')
    data_atual = date.today()
    data_formatada = data_atual.strftime('%Y-%m-%d')
    df_usd = pd.read_csv('data/df_usd.csv')
    

    # if not df_usd[df_usd.ds == data_formatada]['Valor'].values:
    #     currency = float(getCurrency('USD','USDAOA',data_formatada))
    #     if currency>0:             
    #         new_element = {
    #             'ds': data_formatada,
    #             'Valor': currency,
    #         }
    #         df_usd = pd.concat([df_usd, pd.DataFrame([new_element])], ignore_index=True)
    #         df_usd = df_usd.drop('Unnamed: 0', axis=1)
    #         df_usd.to_csv('data/df_usd.csv')
    try:
        return df_usd[df_usd.ds == ds]['Valor'].values[0]
    except:
        return 0.0
    

def getCurrency(Base,Code,Date):
    import requests

    url = f"https://api.apilayer.com/currency_data/historical?date={Date}&source={Base}&cies=AOA"

    payload = {}
    headers= {
    "apikey": f"{os.getenv('PYTHON_CURRENCY_APIKEY')}"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.json()
    return result['quotes'][Code]

