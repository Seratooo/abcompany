import pandas as pd

df = pd.read_csv('vendasReais.csv')

#df['Ano'] = pd.DatetimeIndex(df.Semana).year
#df['Mes'] = pd.DatetimeIndex(df.Semana).month

print(df['school_holiday'])