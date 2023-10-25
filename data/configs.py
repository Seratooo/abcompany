#DATABASE
import pandas as pd
from prophet import Prophet

from api.externalFactors import future_euro_inflation, future_usd_inflation, future_weather

def sales_predition(store_id, sales_df, holidays, periods):
    # sales_df = sales_df[sales_df['Store'] == store_id]
    sales_df = sales_df[['Date', 'Sales']].rename(columns = {'Date': 'ds', 'Sales':'y'})
    sales_df['ds'] = pd.to_datetime(sales_df['ds'])
    sales_df = sales_df.sort_values(by = 'ds')
    
    model = Prophet(holidays=holidays)
    model.fit(sales_df)
    future = model.make_future_dataframe(periods = periods)
    forecast = model.predict(future)
    # figure1 = model.plot(forecast, xlabel= 'Data', ylabel='Vendas')
    # figure2 = model.plot_components(forecast)
    
    return sales_df, forecast

def sales_predition_v2( sales_df, holidays, periods, country_name, fourier, fourier_monthly, seasonality_mode):

    sales_df = sales_df[['Date', 'Quantity']].rename(columns = {'Date': 'ds', 'Quantity':'y'})
    sales_df['ds'] = pd.to_datetime(sales_df['ds'])
    sales_df = sales_df.sort_values(by = 'ds')
    
    has_holidays = holidays.empty
    if has_holidays:
        model = Prophet(yearly_seasonality=fourier, seasonality_mode=seasonality_mode) #)
    else:
        model = Prophet(yearly_seasonality=fourier, seasonality_mode=seasonality_mode, holidays=holidays) #)

    model.add_country_holidays(country_name=country_name)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=fourier_monthly)
    model.fit(sales_df)
    future = model.make_future_dataframe(periods = periods)
    forecast = model.predict(future)
    
    return sales_df, forecast, model


def sales_predition_Weather(sales_df, holidays, periods,country_name, fourier, fourier_monthly, seasonality_mode):

    paramters = ['Date','Quantity']
    
    if 'Weather' in sales_df.columns:
        paramters.append('Weather')

    if 'Inflation_euro' in sales_df.columns:
        paramters.append('Inflation_euro')

    if 'Inflation_dolar' in sales_df.columns:
        paramters.append('Inflation_dolar')

    sales_df = sales_df[paramters] 
    sales_df = sales_df.rename(columns = {'Date': 'ds', 'Quantity':'y'})
    sales_df = sales_df.sort_values(by = 'ds')
    
    has_holidays = holidays.empty
    if has_holidays:
        model = Prophet(yearly_seasonality=fourier, seasonality_mode=seasonality_mode) #)
    else:
        model = Prophet(yearly_seasonality=fourier, seasonality_mode=seasonality_mode, holidays=holidays) #)

    # model = Prophet(yearly_seasonality=fourier, seasonality_mode=seasonality_mode)  #, holidays=holidays)
    model.add_country_holidays(country_name=country_name)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=fourier_monthly)
    
    if 'Weather' in sales_df.columns:
        model.add_regressor('Weather')# , mode=seasonality_mode)
    
    if 'Inflation_euro' in sales_df.columns:
         model.add_regressor('Inflation_euro')#, mode=seasonality_mode)
    
    if 'Inflation_dolar' in sales_df.columns:
        model.add_regressor('Inflation_dolar')#, mode=seasonality_mode)

    model.fit(sales_df)
    
    future = model.make_future_dataframe(periods = periods)
    
    if 'Weather' in sales_df.columns:
        future['Weather'] = future['ds'].apply(future_weather)
    
    if 'Inflation_euro' in sales_df.columns:
        future['Inflation_euro'] = future['ds'].apply(future_euro_inflation)
    
    if 'Inflation_dolar' in sales_df.columns:
        future['Inflation_dolar'] = future['ds'].apply(future_usd_inflation)
        
    forecast = model.predict(future)
    return sales_df, forecast, model