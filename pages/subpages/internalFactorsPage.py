from dash import html, Output, Input, callback, dash_table, State, dcc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objs as go

TasksTab = [
     html.P(children='Tarefas', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#000","marginBottom":".8rem"}),
         dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Dados", value="task_board"),
                        dmc.Tab("Gráficos", value="task_graph")
                    ]
                ),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="task-board", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="task_board"),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="task-graph", style={"height":"55vh"}),], color="var(--primary)", type="dot", fullscreen=False,), value="task_graph"),
            ],
            color="green",
            orientation="horizontal",
            value="task_board"
        ),
]

PromotionTab = [
     html.P(children='Promoção', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#000","marginBottom":".8rem"}),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Dados", value="data_promotion"),
                        dmc.Tab("Gráficos", value="graph_promotion")
                    ]
                ),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="promotion-board", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="data_promotion"),
                dmc.TabsPanel(dcc.Loading(children=[html.Div(id="promotion-graph", style={"height":"55vh"})], color="var(--primary)", type="dot", fullscreen=False,), value="graph_promotion")
            ],
            color="green",
            orientation="horizontal",
            value="data_promotion"
        ),
]


internalFactorsPage = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Fatores Internos', className='PainelStyle'),
                    html.Div([
                        html.P('Aqui você analisar os fatores internos', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"var(--primary)", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Tarefas", value="tasks"),
                        dmc.Tab("Promoção", value="promotion"),
                    ]
                ),
                dmc.TabsPanel(TasksTab, value="tasks", style={"padding":"10px"}),
                dmc.TabsPanel(PromotionTab, value="promotion", style={"padding":"10px"}),
            ],
            color="green",
            orientation="vertical",
            value="tasks"
        ),
    ], style={"padding":"10px 0", "height":"100vh", "background":"#f0f0f0","overflow":"scroll","marginBottom":"30px"}),
])


@callback(
   Output('task-board','children'),
   Input('task-board', 'id'),
)
def handleSetBoard(_):
    df_task = pd.read_csv('data/df_task.csv')

    table = dash_table.DataTable(
    data=df_task.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df_task.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    page_action="native",
    page_current= 0,
    page_size= 10,
    )
    return table

@callback(
   Output('task-graph','children'),
   Input('task-graph', 'id'),
)
def handleSetBoard(_):
    df_task = pd.read_csv('data/df_task.csv')

    graph = dcc.Graph(
        id='task-mygraph',
        figure={
            'data': [
                go.Scatter(
                    x=df_task['Date'],
                    y=[1] * len(df_task['Name']),
                    mode='markers',
                    marker={'size': 10},
                    name='Tarefas'
                )
            ],
            'layout': {
                'title': 'Tarefas realizadas',
                'xaxis': {'title': 'Data'},
                'yaxis': {'showticklabels': False}
            }
        }
    )
    return graph


@callback(
   Output('promotion-board','children'),
   Input('promotion-board', 'id'),
)
def handleSetBoard(_):
    df_promo = pd.read_csv('data/df_promo.csv')

    table = dash_table.DataTable(
    data=df_promo.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df_promo.columns],
    fixed_rows={'headers': True},
    style_data={'fontSize': '1.2rem'},
    page_action="native",
    page_current= 0,
    page_size= 10,
    )
    return table


@callback(
   Output('promotion-graph','children'),
   Input('promotion-graph', 'id'),
)
def handleSetBoard(_):
    df_promo = pd.read_csv('data/df_promo.csv')

    graph = dcc.Graph(
        id='promo-mygraph',
        figure={
            'data': [
                go.Scatter(
                    x=df_promo['Date'],
                    y=[1] * len(df_promo['Name']),
                    mode='markers',
                    marker={'size': 10},
                    name='Promoções'
                )
            ],
            'layout': {
                'title': 'Promoções realizadas',
                'xaxis': {'title': 'Data'},
                'yaxis': {'showticklabels': False}
            }
        }
    )
    return graph