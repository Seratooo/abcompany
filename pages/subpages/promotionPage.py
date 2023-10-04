from dash import html, callback, Input, Output, State, dash_table
import dash_mantine_components as dmc
from datetime import datetime, timedelta, date
import pandas as pd

PromotionTab = html.Div([
          html.Div([
            dmc.Select(
              label="Tipo de Promoção",
              placeholder="Selecione uma",
              id="promo-type",
              value="Cupom",
              data=[
                  {"value": "Cupom", "label": "Cupom"},
                  {"value": "Frete grátis", "label": "Frete grátis"},
                  {"value": "Sorteios", "label": "Sorteios"},
                  {"value": "Demonstrações grátis", "label": "Demonstrações grátis"},
                  {"value": "Oferta limitada", "label": "Oferta limitada"},
                  {"value": "Compre um, ganhe outro", "label": "Compre um, ganhe outro"},
              ],
              style={"width": 200, "marginBottom": 10},
            ),
            dmc.DateRangePicker(
            id="promo-date",
            label="Periodo de Promoção",
            description="",
            minDate=date(2019, 12, 8),
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
            id='promo-desc'
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
      dmc.Button("Registar Promoção", id='create-task'),
      ], id='task-wrapper'),
PromoBoard = html.Div(id="board-promo", style={"padding":"0 15px"})

promotion = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Registar Promoção', className='PainelStyle'),
                    html.Div([
                        html.P('Aqui você poderá registar todas as promoções', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"var(--primary)", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
      
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
              dmc.TabsPanel(PromoBoard, value="board"),
          ],
          color="var(--primary)",
          orientation="vertical",
          value="promotions",
      ),
      html.Div([
         html.P(f"Promoções registadas!", className="desc-popup"),  
         html.Button('OK', id='btn-popup2', className='btn-popup')], id='popup-output2', className='popup-output'),
    ], id='tabs-wrapprer'),
])

@callback(
  Output('popup-output2','style', allow_duplicate=True),
  Output('promo-desc','value'),
  Input('create-task','n_clicks'),
  State('promo-type','value'),
  State('promo-date','value'),
  State('promo-desc','value'),
  prevent_initial_call=True,
)
def handlePromotions(n_clicks,PromoType,PromoDate,PromoDesc):
  if n_clicks is not None:
    _promo = pd.DataFrame()
    
    data_inicial = datetime.strptime(PromoDate[0], '%Y-%m-%d')
    data_final = datetime.strptime(PromoDate[1], '%Y-%m-%d')
    intervalo = timedelta(days=1)

    data_atual = data_inicial
    while data_atual <= data_final:
        new_element = {
                    'Name': f'Promoção ({PromoType})',
                    'Description': PromoDesc,
                    'Type': PromoType,
                    'Date': data_atual.strftime("%Y-%m-%d"),
                    }
        data_atual += intervalo
        _promo = pd.concat([_promo, pd.DataFrame([new_element])], ignore_index=True)
    df_promo = pd.concat((pd.read_csv('data/df_promo.csv'), _promo))
    df_promo = df_promo.drop('Unnamed: 0', axis=1)
    df_promo.to_csv('data/df_promo.csv')
    
    return {"display":"flex"}, ''
  
@callback(
   Output('popup-output2','style'),
   Input('btn-popup2','n_clicks'),
)
def handleClosePopUp(n_clicks):
   if n_clicks is not None:
      return {"display":"none"}
   
@callback(
   Output('board-promo','children'),
   Input('board-promo', 'id'),
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