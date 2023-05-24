from datetime import date, datetime
import holidays
import pandas as pd
from meteostat import Point, Daily
import pandas_datareader.data as web
import eurostat

us_holidays = holidays.AO()
LuandaPoint = Point(-8.838333, 13.234444, 70)

def GetHolidaysByYear(Year):
    return pd.DataFrame(holidays.AO(years=2023).items())


def GetWhetherByYear(Year):
    start = datetime(Year, 1, 1)
    end = datetime(Year, 12, 31)
    data = Daily(LuandaPoint, start, end)
    data = data.fetch()
    return data

# def GetPIB_ByYear(Year):
#     start_time = datetime(2021, 1, 1) 
#     end_time = datetime(2021, 12, 31)
#     df = web.DataReader('TUD', 'oecd', start_time, end_time)
#     print(df)


def GetInflationByYear(Year):
    #toc_df = eurostat.get_toc_df()
    #pars  =  eurostat . get_pars ( 'PRC_HICP_MANR' )
    myFilters = {'startPeriod': '2019-01', 'endPeriod': '2020-01', 'FREQ': ['M'], 'geo': ['US','EU'], 'coicop':['cp00']}
    data  =  eurostat.get_data_df( 'PRC_HICP_MANR',filter_pars=myFilters ) 
    print(data)

