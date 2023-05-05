from dash import html, Output, Input, callback
from dash import dcc
from datetime import date
from data import configs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc


sales_train_all_df = configs.getDatabase()

forecast = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Realizar previsão', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('realize a previsão de vendas até uma data pretendida', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
        dcc.DatePickerRange(
        month_format='MMM Do, YY',
        end_date_placeholder_text='MMM Do, YY',
        start_date=date(2017, 6, 21),
        id="datePicker"
    ),
     dmc.MultiSelect(
            label="Factores a considerar",
            placeholder="Select all you like!",
            id="framework-multi-select",
            value=["ng", "vue"],
            data=[
                {"value": "react", "label": "Eventos Climáticos"},
                {"value": "ng", "label": "Feridos de Estado"},
                {"value": "svelte", "label": "Feriados Escolares"},
                {"value": "vue", "label": "Inflação"},
            ],
            style={"width": 400, "marginBottom": 10},
        ),
    ], style={"display":"flex","justifyContent":"space-between"}),
     html.Div([
            html.Div([
                dcc.Graph(id='graph11', className='dbc'),
            ], style={"width":"46%"}),
            html.Div([
                dcc.Graph(id='graph12', className='dbc'),
            ], style={"width":"46%"}),
        ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
       
])


school_holidays = sales_train_all_df[sales_train_all_df['SchoolHoliday'] == 1].loc[:,'Date'].values
state_holidays = sales_train_all_df[(sales_train_all_df['StateHoliday'] == 'a') | 
                                    (sales_train_all_df['StateHoliday'] == 'b') |
                                    (sales_train_all_df['StateHoliday'] == 'c')].loc[:,'Date'].values

state_holiday = pd.DataFrame({'ds': pd.to_datetime(state_holidays), 'holiday': 'state_holiday'})
school_holiday = pd.DataFrame({'ds': pd.to_datetime(school_holidays), 'holiday': 'school_holiday'})
school_state_holiday = pd.concat((state_holiday, school_holiday))

#df_original, df_predition = configs.sales_predition(10,sales_train_all_df,school_state_holiday,3)
# print(df_predition.tail(5))


# @callback(
#           Output("graph11", "figure"),
#           Output("graph12", "figure"),
#           Input("datePicker", "value")
#           )
# def select_value(value):
#     fig = px.area(df_predition, x="ds", y="yhat")
#     fig2 = px.histogram(df_predition, x="ds", y="holidays", hover_data=df_predition.columns)
#     return fig, fig2