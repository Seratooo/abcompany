from dash import html
import dash_mantine_components as dmc
from datetime import datetime, timedelta, date


PromotionTab = html.Div([
          html.Div([
            dmc.Select(
              label="Tipo de Promoção",
              placeholder="Selecione uma",
              id="task-select",
              value="ng",
              data=[
                  {"value": "ng", "label": "Angular"},
                  {"value": "svelte", "label": "Svelte"},
              ],
              style={"width": 200, "marginBottom": 10},
            ),
            dmc.DateRangePicker(
            id="date-range-picker",
            label="Perido de Promoção",
            description="",
            minDate=date(2020, 8, 5),
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
            style={"width": 354},
            ),
            #dmc.TextInput(label="Nome da Tarefa", id='task-name'),
      ], className='name-wrapper'),

      html.Div([
           dmc.Textarea(
            label="Descrição",
            placeholder="...",
            autosize=True,
            minRows=2,
            id='desc-task'
        ),
      ], className='desc-wrapper'),

       html.Div([
        # dmc.Select(
        #     label="Equipa Inserida",
        #     placeholder="Selecione uma",
        #     id="team-select",
        #     value="ng",
        #     data=[
        #         {"value": "ng", "label": "Angular"},
        #         {"value": "svelte", "label": "Svelte"},
        #     ],
        #     style={"width": 200, "marginBottom": 10},
        # ),
      ], className='data-wrapper'),
      dmc.Button("Criar Promoção", id='create-task'),
      ], id='task-wrapper'),


promotion = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Registar Promoção', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Aqui você poderá registar todas as promoções', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
      
    html.Div([
      dmc.Tabs(
        [
              dmc.TabsList(
                  [
                      dmc.Tab("Registar Promoções", value="promotions"),
                      dmc.Tab("Quadro", value="board"),
                  ]
              ),
              dmc.TabsPanel(PromotionTab, value="promotions"),
              dmc.TabsPanel("Messages tab content", value="board"),
          ],
          color="#2B454E",
          orientation="vertical",
          value="promotions",
      ),
    ], id='tabs-wrapprer'),
])