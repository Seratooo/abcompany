import dash
from dash import Dash, html,register_page,dcc, callback, Input, Output, State 
import abcompany
import dash_mantine_components as dmc

from api.clientApp import isAuthenticatedUser

dash.register_page(__name__)

layout = html.Div([
        html.Div(id='validate-login'),
        dcc.Loading(children=[dcc.Location(id='url')], color="#2B454E", type="dot", fullscreen=True,),
        html.Section([
            html.P('ABCompany'),
            html.Section([
                # html.Div([
                #         html.P('Novo usuário?'),
                #         html.Div('Entrar')
                #     ]
                #  )
            ])

        ], id="first-section"),



        html.Section([
            html.Div([

            ], className='first-wrapper'),
            html.Div([
               html.H3('Que bom você aqui!'),
               html.P('ABC, a sua plataforma para análise dos dados'),
               html.Div([
                   html.Span([
                       dcc.Input(placeholder="Digite o seu email", type="email", id="input-name")
                   ], className='span-input-name'),
                   html.Span([
                       dcc.Input(placeholder="Digite a sua senha", type="password", id="input-password")
                   ], className='span-input-password')
               ],className='div1'),
               html.Div([
                 html.Div('Entrar', id='BtnLogin'),
                 html.Div('Esqueceu a Senha?', id='BtnPassword')
               ],className='div2'),
            ], className='second-wrapper'),
        ], id="second-section"),
], id="loginPage") 


@callback(Output('validate-login', 'className'),
          Input('BtnLogin','n_clicks'),
          State('input-name','value'),
          State('input-password','value'),
          )
def loadPopUp(n_clicks,  name, password):
    if n_clicks is not None:
        if name is None or password is None or isAuthenticatedUser(name,password)[0] == False:
            return 'on'
    else:
        return ''
        

@callback(Output('validate-login', 'className', allow_duplicate=True),
          Input('btn-popup','n_clicks'),
          State('validate-login', 'className'),
          prevent_initial_call='initial_duplicate'
          )
def loadPopUp(n_clicks, className):
    if n_clicks is not None and className == 'on':
        return ''
    else:
        return 'on'

@callback(
    Output('validate-login','children'),
    Input('BtnLogin','n_clicks'),
    State('input-name','value'),
    State('input-password','value'),
)
def verifyFilds(n_clicks, name, password):
    if n_clicks is not None:
        if name is None:
            return [ html.P('Insira um email! ', className="desc-popup"), html.Button('OK', id='btn-popup')]
        elif password is None:
            return [ html.P('Insira uma palavra passe!', className="desc-popup"), html.Button('OK', id='btn-popup')]
        elif isAuthenticatedUser(name,password)[0] == False:
            return [ html.P('Verifique as credencias!', className="desc-popup"), html.Button('OK', id='btn-popup')]
              

@callback(
    Output("url", "pathname"), 
    Input('BtnLogin','n_clicks'),
    State('input-name','value'),
    State('input-password','value'),
)
def verifyUser(n_clicks, name, password):
    if n_clicks is not None:
        if name and password:
            if isAuthenticatedUser(name,password)[0]:
                return '/dashboard'
            else:  
                return 

@callback(
    Output('User', 'data'), 
    Input('BtnLogin','n_clicks'),
    State('input-name','value'),
    State('input-password','value'),
)
def saveUser(n_clicks, name, password):
    if n_clicks:
       result = isAuthenticatedUser(name,password)
       if result[0] == True:
            user = {
                'name': result[1].get('name'),
                'email': result[1].get('email'),
                'collection': result[1].get('collection')
            }
            return user