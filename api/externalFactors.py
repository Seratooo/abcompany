from datetime import date, datetime
import holidays
import pandas as pd
from meteostat import Point, Daily
import pandas_datareader.data as web
import eurostat

us_holidays = holidays.AO()
LuandaPoint = Point(-8.838333, 13.234444, 70)

def GetHolidaysByYear(Year):
    df = pd.DataFrame(holidays.AO(years=Year).items())
    df.rename(columns={0: 'ds'}, inplace=True)
    df.rename(columns={1: 'holidays'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    df.set_index('ds', inplace=True)
    df.sort_values('ds', inplace=True)
    return df


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


GetInflationByYear(2018)