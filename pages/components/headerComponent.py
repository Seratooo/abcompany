from dash import html, callback, Input, Output, State, dcc
import dash_mantine_components as dmc


HEADAER_STYLE = {
    "background":"#fcfcfc",
    "padding":"7.5px 50px",
    "fontSize":"3.8rem",
    "width":"100%",
    "display":"flex",
    "justifyContent":"right",
    "alignItems":"center",
    "borderBottom":"1px solid #2B454E",
    "cursor":"pointer",
}

header = html.Div(
    [
        dcc.Location(id='url3', refresh=True),
        html.Div(id='data-output-header'),
        html.Div([
            dmc.Group(
            children=[
                dmc.Avatar("", color="green", radius="xl",style={"marginTop":"6px", "cursor":"pointer"}, id='initials'),
                html.P("", style={'fontFamily':'Nunito',"marginTop":"6px", "cursor":"pointer"}, id='avatar-text')
            ],
            style={"display":"flex"}
            )
        ], style=HEADAER_STYLE, id='header-menu')
    ]
)

@callback(
    Output('avatar-text', 'children'),
    Output('initials','children'),
    Input('avatar-text','avatar-text'),
    State('User', 'data'),
)
def setAvatar(_, data):
    return data.get('name'), get_initials(data.get('name'))


def get_initials(nome_completo):
    if nome_completo:
        palavras = nome_completo.split()
        iniciais = [palavra[0] for palavra in palavras]
        iniciais_formatadas = ''.join(iniciais)
        return iniciais_formatadas
    

@callback(
    Output('data-output-header','children'),
    Input('header-menu','n_clicks'),
    State('User', 'data'),
)
def setPopUp(n_clicks, data):
    if n_clicks is not None:
        return [
            html.Div([
                html.P(f"Nome: {data.get('name')}", className="desc-popup1"), 
                html.P(f"Email: {data.get('email')}", className="desc-popup1"), 
            ], id="Wrapper-popup"), 
            
            html.Div([
                html.Button('OK', id='btn-popup1'),
                html.Button('Sair', id='btn-sair-popup1')
            ], style={"display":"flex", "gap":"10px"}),
            ]



@callback(Output('data-output-header', 'className', allow_duplicate=True),
          Input('btn-popup1','n_clicks'),
          State('data-output-header', 'className'),
          prevent_initial_call='initial_duplicate'
          )
def loadPopUp(n_clicks, className):
    if n_clicks is not None and className == 'active':
        return ''
    else:
        return 'active'
    

@callback(Output('data-output-header', 'className'),
          Input('header-menu','n_clicks'),
          )
def loadPopUp(n_clicks):
    if n_clicks is not None:
        return 'active'
    else:
        return ''
    


@callback(Output('User', 'data', allow_duplicate=True),
          Output('url3','pathname'),
          Input('btn-sair-popup1','n_clicks'),
          State('User', 'data'),
          State('url3','pathname'),
          prevent_initial_call='initial_duplicate'
          )
def closeSession(n_clicks, data, pathname):
    if n_clicks is not None:
        return {}, '/login'
    else:
        return data, pathname
