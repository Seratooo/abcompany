from dash import html, dcc, callback, Output, Input, State
import plotly.express as px
from api.clientApp import GetAllCollectionNames
from data.configs import getDatabase
import plotly.graph_objects as go
import dash_mantine_components as dmc

sales_train_all_df = getDatabase()
DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]

resume = html.Div([
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-names-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Painel de Resumo', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        dmc.MultiSelect(
                        label="",
                        placeholder="Select all you like!",
                        id="panel-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[
                            {"value": "react", "label": "React"},
                            {"value": "ng", "label": "data 2015-2020"},
                            {"value": "svelte", "label": "Svelte"},
                            {"value": "vue", "label": "data 2020 - 2022"},
                        ],
                        style={"width": 400, "marginBottom": 10,"fontSize":"1.2rem"},
                        ),
                    ])
                ])
            ),
            html.Div(
            dmc.Button("Criar relatório", style={"background":"#fff", "color":"#000","font":"3.2rem Nunito","marginTop":"1.2rem"}),
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
            html.Div([
                html.Div([dcc.Graph(id='graph1', className='dbc')],style={"width":"30%"}),
                html.Div([dcc.Graph(id='graph2', className='dbc')], style={"width":"30%"}),
                html.Div([dcc.Graph(id='graph3', className='dbc')], style={"width":"30%"}),
            ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
            html.Div([
                html.Div([dcc.Graph(id='graph4', className='dbc')], style={"width":"51%"}),
                html.Div([dcc.Graph(id='graph5', className='dbc')], style={"width":"40%"}),
            ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        ]
        , style={"width":"100%","height":"140%"}),
])






@callback(Output("graph1", "figure"),
          Output("graph2", "figure"),
          Output("graph3", "figure"),
          Output("graph4", "figure"),
          Output("graph5", "figure"),
          Input("panel-dataset-multi-select", "value")
          )
def select_value(value):
    fig1 = go.Figure() 
    fig1.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Período de Análise </span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{sales_train_all_df['Year'].min()} - {sales_train_all_df['Year'].max()}</span>"},
            value = (sales_train_all_df['Year'].max() - sales_train_all_df['Year'].min()),
            number = {'suffix': " Anos"}
    ))

    df2_dataframe = sales_train_all_df
    df2_dataframe[['Date', 'Sales']].rename(columns = {'Date': 'date', 'Sales':'sales'})


    df2 = df2_dataframe.groupby(['Date'])['Sales'].sum().reset_index()
    df2.sort_values(ascending=False, inplace=True, by='Sales')

    Year = (df2_dataframe['Year'].max()) - (df2_dataframe['Year'].min())

    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(mode='number+delta',
            title = {"text": f"<span style='font-size:150%'>Maior Rendimento diário <br> em {Year} anos</span><br><span style='font-size:70%'> em relação a média</span><br>"},
            value = df2['Sales'].iloc[0],
            number = {'prefix': "AKZ "},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df2['Sales'].mean()}
    ))


    df3 = df2_dataframe.groupby(['Date'])['Sales'].sum().reset_index()
    df3.sort_values(ascending=True, inplace=True, by='Sales')

    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(mode='number+delta',
            title = {"text": f"<span style='font-size:150%'>Menor Rendimento diário <br> em {Year} anos</span><br><span style='font-size:70%'> em relação a média</span><br>"},
            value = df3['Sales'].iloc[0],
            number = {'prefix': "AKZ "},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df3['Sales'].mean()}
    ))


    df4 = sales_train_all_df[sales_train_all_df.columns[1:6]].head(10)

    fig4 = go.Figure()
    fig4.add_trace(
        go.Table(
            header=dict(
                values=df4.columns,
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df4[k].tolist() for k in df4.columns[0:,]],
                align = "left")
        ))

    fig4.update_layout(
        showlegend=False,
        title_text="Amostra dos dados a serem analisados",
    )


    df5 = sales_train_all_df.groupby('Month')['Sales'].sum().reset_index()

    fig5 = px.pie(df5, values='Sales', names='Month', title='Distribuição das receitas por mês')

    fig1.update_layout(height=230)
    fig2.update_layout(height=230)
    fig3.update_layout(height=230)
    fig4.update_layout(height=430)
    fig5.update_layout(height=430)
    return fig1, fig2, fig3, fig4, fig5


@callback(Output('panel-dataset-multi-select', component_property='value'),
          Output('panel-dataset-multi-select', component_property='data'),
                Input('interval_db', component_property='n_intervals'),
              )
def SetDataValuesOnCompont(interval_db):
    value = PanelMultiSelectOptions
    return value, DatasetValues()[1]


def DatasetValues():
    data = []
    for name in DatasetsNames:
        data.append({"value": f"{name}", "label": f"{name}"})
    return DatasetsNames, data


@callback(
    Output('dataset-names-storage', 'data', allow_duplicate=True),
    Input("panel-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions