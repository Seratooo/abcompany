from dash import html
import dash_mantine_components as dmc
from datetime import datetime, timedelta, date


TaskTab = html.Div([
          html.Div([
            dmc.Select(
              label="Tipo de tarefa",
              placeholder="Selecione uma",
              id="task-select",
              value="ng",
              data=[
                  {"value": "ng", "label": "Angular"},
                  {"value": "svelte", "label": "Svelte"},
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
            label="Perido de Execução",
            description="",
            minDate=date(2020, 8, 5),
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
            style={"width": 330},
        ),
        dmc.Select(
            label="Equipa Inserida",
            placeholder="Selecione uma",
            id="team-select",
            value="ng",
            data=[
                {"value": "ng", "label": "Angular"},
                {"value": "svelte", "label": "Svelte"},
            ],
            style={"width": 200, "marginBottom": 10},
        ),
      ], className='data-wrapper'),
      dmc.Button("Criar Tarefa", id='create-task'),
      ], id='task-wrapper'),


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
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
      
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
              dmc.TabsPanel("Messages tab content", value="board"),
          ],
          color="#2B454E",
          orientation="vertical",
          value="tasks",
      ),
    ], id='tabs-wrapprer'),
])