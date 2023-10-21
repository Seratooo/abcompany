import pandas as pd

df = pd.read_csv('data/trends/Entrecosto Especial.csv')
df['Ano'] = pd.DatetimeIndex(df.Semana).year
df['Mes'] = pd.DatetimeIndex(df.Semana).month

df.to_csv('data/trends/Entrecosto Especial.csv')
