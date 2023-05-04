import dash
import dash_mantine_components as dmc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from prophet import Prophet
import plotly.express as px
import plotly.graph_objects as go
#from subpages import resumePage
from data import configs
from components import headerComponent, sidebarComponent, containerComponent
dash.register_page(__name__,  suppress_callback_exceptions=True)


#DATABASE
sales_train_all_df = configs.getDatabase()

#COMPOENTS
sidebar = sidebarComponent.sidebar
header = headerComponent.header

content = containerComponent.content

DashboardWrapper = html.Div([
    header,
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Painel de Resumo', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        dmc.MultiSelect(
                        label="",
                        placeholder="Select all you like!",
                        id="framework-multi-select",
                        value=["ng", "vue"],
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
    content], style={"width":"100%"})

layout = html.Div([dcc.Location(id='url', refresh=False), sidebar, DashboardWrapper], style={"display":"flex"})


#PAGES
ResumePage = html.Div([
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
    , style={"width":"100%","height":"140%"})

VendasPage = html.Div([
        html.Div([
            html.Div([dcc.Graph(id='graph6', className='dbc')],style={"width":"30%"}),
            html.Div([dcc.Graph(id='graph7', className='dbc')], style={"width":"30%"}),
            html.Div([dcc.Graph(id='graph8', className='dbc')], style={"width":"30%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        html.Div([
            html.Div([
                dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="framework-select",
                    value="dia",
                    data=[
                        {"value": "mes", "label": "Mês"},
                        {"value": "ano", "label": "Ano"},
                        {"value": "semana", "label": "Semana"},
                        {"value": "dia", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Graph(id='graph9', className='dbc'),
            ], style={"width":"46%"}),
            html.Div([
                 dmc.Select(
                    label="",
                    placeholder="Select one",
                    id="framework-select",
                    value="dia",
                    data=[
                        {"value": "mes", "label": "Mês"},
                        {"value": "ano", "label": "Ano"},
                        {"value": "semana", "label": "Semana"},
                        {"value": "dia", "label": "Dia"},
                    ],
                    style={"width": 200, "marginBottom": 10},
                ),
                dcc.Graph(id='graph10', className='dbc'),
            ], style={"width":"46%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        
], style={"width":"100%","height":"140%"})



@callback(
          Output("page-content", "children"), 
          [Input("url", "pathname"), Input("url", "search")])
def render_page_content(pathname, search):
    link = f'{pathname}{search}'
    if link == "/dashboard":
        return ResumePage
    elif  link == "/dashboard?vendas":
        return VendasPage
    elif  link == "/dashboard?page-2":
        return html.P("This is the content of back page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )






@callback(Output("graph1", "figure"),
          Output("graph2", "figure"),
          Output("graph3", "figure"),
          Output("graph4", "figure"),
          Output("graph5", "figure"),
          Input("framework-multi-select", "value")
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
    return fig1, fig2, fig3, fig4, fig5,



@callback(
          Output("graph6", "figure"),
          Output("graph7", "figure"),
          Output("graph8", "figure"),
          Output("graph9", "figure"),
          Output("graph10", "figure"),
          Input("framework-multi-select", "value")
          )
def select_value(value):
    d6 = sales_train_all_df[sales_train_all_df['Promo']==1]
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Promoções realizadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d6['Year'].min()} - {d6['Year'].max()}</span>"},
            value = (d6['Promo'].count()),
            number = {'suffix': ""}
    ))

    d7 = sales_train_all_df[sales_train_all_df['Customers']>0]
    fig7 = go.Figure()
    fig7.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Clientes Alcançados</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d7['Year'].min()} - {d7['Year'].max()}</span>"},
            value = (d7['Customers'].count()),
            number = {'suffix': ""}
    ))

    d8 = sales_train_all_df
    fig8 = go.Figure()
    fig8.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Receitas Arrecadadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d8['Year'].min()} - {d8['Year'].max()}</span>"},
            value = (d8['Sales'].sum()),
            number = {'prefix': "AKZ "}
    ))


    df9 = sales_train_all_df.groupby('Day')['Sales'].mean().reset_index()
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(
            x=df9["Day"],
            y=df9["Sales"],
            mode="lines",
            name="hash-rate-TH/s"
        ))
    fig9.update_layout(
        showlegend=False,
        title_text="Média das vendas por dia",
    )

    df10 = sales_train_all_df.groupby('Day')['Customers'].mean().reset_index()
    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(
            x=df10["Day"],
            y=df10["Customers"],
            mode="lines",
            name="hash-rate-TH/s"
        ))
    fig10.update_layout(
        showlegend=False,
        title_text="Média de clientes por dia",
    )

    fig6.update_layout(height=230)
    fig7.update_layout(height=230)
    fig8.update_layout(height=230)
    return fig6, fig7, fig8, fig9, fig10,