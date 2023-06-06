#DATABASE
import pandas as pd
from prophet import Prophet

def getDatabase():
  sales_train_df = pd.read_csv('data/train.csv', low_memory=False)
  store_info_df = pd.read_csv('data/store.csv')

  sales_train_df = sales_train_df[sales_train_df['Open'] == 1]
  sales_train_df.drop(['Open'], axis=1, inplace=True)

  str_cols = ['Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval', 'CompetitionOpenSinceYear', 'CompetitionOpenSinceMonth']
  for str in str_cols:
      store_info_df[str].fillna(0, inplace=True)

  store_info_df['CompetitionDistance'].fillna(store_info_df['CompetitionDistance'].mean(), inplace=True)

  sales_train_all_df = pd.merge(sales_train_df, store_info_df, how = 'inner', on='Store')

  sales_train_all_df['Year'] = pd.DatetimeIndex(sales_train_all_df['Date']).year
  sales_train_all_df['Month'] = pd.DatetimeIndex(sales_train_all_df['Date']).month
  sales_train_all_df['Day'] = pd.DatetimeIndex(sales_train_all_df['Date']).day
  return sales_train_all_df


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