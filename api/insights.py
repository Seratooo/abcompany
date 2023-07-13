import pandas as pd

data = {
    'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Sales': [2321, 2209, 2327, 2180, 5407, 5350, 5508, 5416, 3753, 3662, 3737, 3839]
}

df = pd.DataFrame(data)

def semestre_tendencia_crescimento(df):
    # Agrupar por semestre e calcular a diferença de vendas entre o primeiro e último mês
    df['Semester'] = pd.cut(df['Month'], bins=[1, 6, 12], labels=['1º', '2º'])
    df_semester = df.groupby('Semester').agg({'Sales': lambda x: x.iloc[-1] - x.iloc[0]})

    # Identificar o semestre com maior crescimento
    semestre_max_crescimento = df_semester['Sales'].idxmax()
    
    return f"O {semestre_max_crescimento} semestre apresenta tendência de crescimento mais expressivo"

# O mesmo para os ultimos meses do ano tbm
def tendencia_crescimento_inicial(df, meses):
    primeiros_meses = df[df['Month'].isin(meses)]
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    firMonth = months[meses[0] - 1]
    lastMonth = months[meses[len(meses) - 2]]
    vendas_meses = df[df['Month'].isin(meses)]['Sales']

    variacoes_percentuais = vendas_meses.pct_change()
    variacoes_percentuais.pop(0)
    flutuacoes_insignificantes = all(abs(variacoes_percentuais) <= 0.07)

     # Verificar se há uma tendência de crescimento
    if primeiros_meses['Sales'].is_monotonic_increasing is True:
        tendencia = f"Há uma tendência de crescimento nos meses de {firMonth} à {lastMonth}. Observamos uma tendência de crescimento nos primeiros meses do negócio, indicando um aumento consistente nas vendas nesse período. Isso aponta para um potencial de crescimento significativo e sugere que as estratégias de marketing, vendas ou operacionais implementadas estão sendo eficazes. É importante analisar os fatores que impulsionam esse crescimento, identificando as estratégias bem-sucedidas, lançamentos de novos produtos ou fatores sazonais que contribuem para o aumento das vendas."
    elif primeiros_meses['Sales'].is_monotonic_decreasing is True:
        tendencia = f"Há uma tendência de decrescimento nos meses de {firMonth} à {lastMonth}. A tendência de decrescimento nos primeiros meses requer uma avaliação das estratégias de negócio implementadas nesse período, a fim de identificar possíveis melhorias ou ajustes necessários."
    elif primeiros_meses['Sales'].is_monotonic_increasing is False and primeiros_meses['Sales'].is_monotonic_decreasing is False:
        if flutuacoes_insignificantes:
          tendencia = f"Existe estabilidade nas vendas nos meses de {firMonth} à {lastMonth}. Que pode significar que há flutuações estáveis nos primeiros meses. Isso pode indicar que as vendas nesse período são relativamente estáveis e não mostram um padrão consistente de aumento ou diminuição superior a 7%. Isso pode ser resultado de uma demanda estável ou de fatores externos que mantêm as vendas em um nível constante."
        else:
          tendencia = f"Não existe estabilidade nas vendas nos meses de {firMonth} à {lastMonth}. Que pode significar que há flutuações instáveis nos primeiros meses. Nesse caso, os valores de vendas variam de forma imprevisível a uma percentagem superior a 7%, sem uma direção clara de crescimento ou diminuição. Essas flutuações podem ser causadas por fatores aleatórios, como eventos pontuais, mudanças nas condições econômicas locais ou outras influências imprevisíveis."
            
    return tendencia

#Meses Picos em relação os meses adjacentes
def identificar_picos_vendas(df):
     picos = []
     months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
     for i in range(1, len(df)-1):
        if df['Sales'][i] > df['Sales'][i-1] and df['Sales'][i] > df['Sales'][i+1]:
            picos.append(months[i])

     return picos



def find_peak_period(df):

    # Converter a coluna 'Date' para o tipo de data
    df['Date'] = pd.to_datetime(df['Date'])

    # Ordenar o dataframe pelo valor das vendas em ordem decrescente
    df = df.sort_values(by='Sales', ascending=False)

    # Obter as datas com as maiores vendas
    maiores_vendas = df[df['Sales'] == df['Sales'].max()]['Date']
    
    return maiores_vendas

def calcular_quantidade_vendas_maior_menor_media(dataset):
    # Calcular a média das vendas
    media_vendas = df['Sales'].mean()
    
    # Filtrar as datas com o maior número de vendas em relação à média
    vendas_maior_media = df[df['Sales'] > media_vendas]

    # Filtrar as datas com o menor número de vendas em relação à média
    vendas_menor_media = df[df['Sales'] < media_vendas]
    return vendas_maior_media, vendas_menor_media


