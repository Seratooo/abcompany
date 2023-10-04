from dash import html, callback, Input, Output, State, dash_table
import dash_mantine_components as dmc
from datetime import datetime, timedelta, date
import pandas as pd

TaskTab = html.Div([
          html.Div([
            dmc.Select(
              label="Tipo de tarefa",
              placeholder="Selecione uma",
              id="task-select",
              value="Gestão de Produtos",
              data=[
                  {"value": "Gestão de Produtos", "label": "Gestão de Produtos"},
                  {"value": "Automatização de Processos", "label": "Automatização de Processos"},
                  {"value": "Marketing Digital", "label": "Marketing Digital"},
                  {"value": "Análise de Dados", "label": "Análise de Dados"},
              ],
              style={"width": 200, "marginBottom": 10},
            ),
            dmc.TextInput(label="Nome da Tarefa", id='task-name'),
      ], className='name-wrapper'),

      html.Div([
           dmc.Textarea(
            label="Descrição da tarefa",
            placeholder="...",
            autosize=True,
            minRows=2,
            id='desc-task'
        ),
      ], className='desc-wrapper'),

       html.Div([
          dmc.DateRangePicker(
            id="date-range-picker",
            label="Periodo de Execução",
            description="",
            minDate=date(2019, 12, 8),
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
            style={"width": 330},
        ),
        dmc.Select(
            label="Equipa Inserida",
            placeholder="Selecione uma",
            id="team-select",
            value="Dynamic",
            data=[
                {"value": "LaPermission", "label": "LaPermission"},
                {"value": "Bravos-M16", "label": "Bravos-M16"},
                {"value": "Dynamic", "label": "Dynamic"},
                {"value": "Ngola", "label": "Ngola"},
            ],
            style={"width": 200, "marginBottom": 10},
        ),
      ], className='data-wrapper'),
      dmc.Button("Registar Tarefa", id='create-task'),
      ], id='task-wrapper'),
TaskBoard = html.Div(id="board-table", style={"padding":"0 15px"})

tasks = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Registar Tarefas', className='PainelStyle'),
                    html.Div([
                        html.P('Aqui você poderá registar todas as tarefas', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"var(--primary)", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
      
    html.Div([
      dmc.Tabs(
        [
              dmc.TabsList(
                  [
                      dmc.Tab("Registar Tarefas", value="tasks"),
                      dmc.Tab("Quadro", value="board"),
                  ]
              ),
              dmc.TabsPanel(TaskTab, value="tasks"),
              dmc.TabsPanel(TaskBoard, value="board"),
          ],
          color="var(--primary)",
          orientation="vertical",
          value="tasks",
      ),
      html.Div([
         html.P(f"Tarefas registadas!", className="desc-popup"),  
         html.Button('OK', id='btn-popup', className='btn-popup')], id='popup-output', className='popup-output'),
    ], id='tabs-wrapprer'),
])

@callback(
  Output('popup-output','style', allow_duplicate=True),
  Output('task-name','value'),
  Output('desc-task','value'),
  Input('create-task','n_clicks'),
  State('task-select','value'),
  State('task-name','value'),
  State('desc-task','value'),
  State('date-range-picker','value'),
  State('team-select','value'),
  prevent_initial_call=True,
)
def handleCreateTask(n_clicks, taskType, taskName, taskDesc, taskDate, taskTeam):
  if n_clicks is not None:
    
    _task = pd.DataFrame()
    
    data_inicial = datetime.strptime(taskDate[0], '%Y-%m-%d')
    data_final = datetime.strptime(taskDate[1], '%Y-%m-%d')
    intervalo = timedelta(days=1)

    data_atual = data_inicial
    while data_atual <= data_final:
        new_element = {
                    'Name': f'Tarefa: {taskName} (Team: {taskTeam})',
                    'Description': taskDesc,
                    'Type': taskType,
                    'Team': taskTeam,
                    'Date': data_atual.strftime("%Y-%m-%d"),
                    }
        data_atual += intervalo
        _task = pd.concat([_task, pd.DataFrame([new_element])], ignore_index=True)
    df_task = pd.concat((pd.read_csv('data/df_task.csv'), _task))
    df_task = df_task.drop('Unnamed: 0', axis=1)
    df_task.to_csv('data/df_task.csv')
    
    return {"display":"flex"}, '',''


@callback(
   Output('popup-output','style'),
   Input('btn-popup','n_clicks'),
)
def handleClosePopUp(n_clicks):
   if n_clicks is not None:
      return {"display":"none"}
   

@callback(
   Output('board-table','children'),
   Input('board-table', 'id'),
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