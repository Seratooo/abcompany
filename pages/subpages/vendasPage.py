# import dash
# from dash import Dash, html,register_page, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd
# from data import configs
# import plotly.graph_objects as go
# import dash_mantine_components as dmc


# sales_train_all_df = configs.getDatabase()
# vendas = html.Div([
#         html.Div([
#             html.Div([dcc.Graph(id='graph6', className='dbc')],style={"width":"30%"}),
#             html.Div([dcc.Graph(id='graph7', className='dbc')], style={"width":"30%"}),
#             html.Div([dcc.Graph(id='graph8', className='dbc')], style={"width":"30%"}),
#         ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
#         html.Div([
#             html.Div([
#                 dmc.Select(
#                     label="",
#                     placeholder="Select one",
#                     id="framework-select",
#                     value="dia",
#                     data=[
#                         {"value": "mes", "label": "Mês"},
#                         {"value": "ano", "label": "Ano"},
#                         {"value": "semana", "label": "Semana"},
#                         {"value": "dia", "label": "Dia"},
#                     ],
#                     style={"width": 200, "marginBottom": 10},
#                 ),
#                 dcc.Graph(id='graph9', className='dbc'),
#             ], style={"width":"46%"}),
#             html.Div([
#                  dmc.Select(
#                     label="",
#                     placeholder="Select one",
#                     id="framework-select",
#                     value="dia",
#                     data=[
#                         {"value": "mes", "label": "Mês"},
#                         {"value": "ano", "label": "Ano"},
#                         {"value": "semana", "label": "Semana"},
#                         {"value": "dia", "label": "Dia"},
#                     ],
#                     style={"width": 200, "marginBottom": 10},
#                 ),
#                 dcc.Graph(id='graph10', className='dbc'),
#             ], style={"width":"46%"}),
#         ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
        
# ], style={"width":"100%","height":"140%"})



# @callback(
#           Output("graph6", "figure"),
#           Output("graph7", "figure"),
#           Output("graph8", "figure"),
#           Output("graph9", "figure"),
#           Output("graph10", "figure"),
#           Input("framework-multi-select", "value")
#           )
# def select_value(value):
#     d6 = sales_train_all_df[sales_train_all_df['Promo']==1]
#     fig6 = go.Figure()
#     fig6.add_trace(go.Indicator(
#             title = {"text": f"<span style='font-size:150%'>Promoções realizadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d6['Year'].min()} - {d6['Year'].max()}</span>"},
#             value = (d6['Promo'].count()),
#             number = {'suffix': ""}
#     ))

#     d7 = sales_train_all_df[sales_train_all_df['Customers']>0]
#     fig7 = go.Figure()
#     fig7.add_trace(go.Indicator(
#             title = {"text": f"<span style='font-size:150%'>Clientes Alcançados</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d7['Year'].min()} - {d7['Year'].max()}</span>"},
#             value = (d7['Customers'].count()),
#             number = {'suffix': ""}
#     ))

#     d8 = sales_train_all_df
#     fig8 = go.Figure()
#     fig8.add_trace(go.Indicator(
#             title = {"text": f"<span style='font-size:150%'>Receitas Arrecadadas</span><br><span style='font-size:70%'>entre o ano de:</span><br><span>{d8['Year'].min()} - {d8['Year'].max()}</span>"},
#             value = (d8['Sales'].sum()),
#             number = {'prefix': "AKZ "}
#     ))


#     df9 = sales_train_all_df.groupby('Day')['Sales'].mean().reset_index()
#     fig9 = go.Figure()
#     fig9.add_trace(go.Scatter(
#             x=df9["Day"],
#             y=df9["Sales"],
#             mode="lines",
#             name="hash-rate-TH/s"
#         ))
#     fig9.update_layout(
#         showlegend=False,
#         title_text="Média das vendas por dia",
#     )

#     df10 = sales_train_all_df.groupby('Day')['Customers'].mean().reset_index()
#     fig10 = go.Figure()
#     fig10.add_trace(go.Scatter(
#             x=df10["Day"],
#             y=df10["Customers"],
#             mode="lines",
#             name="hash-rate-TH/s"
#         ))
#     fig10.update_layout(
#         showlegend=False,
#         title_text="Média de clientes por dia",
#     )

#     fig6.update_layout(height=230)
#     fig7.update_layout(height=230)
#     fig8.update_layout(height=230)
#     return fig6, fig7, fig8, fig9, fig10,