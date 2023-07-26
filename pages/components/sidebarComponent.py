from dash import Input, Output, html, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc

def get_icon(icon):
    return DashIconify(icon=icon, height=16)


SIDEBAR_STYLE = {
    "position": "relative",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "backgroundColor": "#fcfcfc",
    "height":"100vh",
}

sidebar = html.Div(
    [
        
        html.Div([
            html.H2("ABCompany", style={'fontSize':'1.8rem','fontFamily':'Nunito','color':'#2B454E', 'fontWeight':'700', 'marginTop':'5px'}),
            dmc.Burger(id="burger-button", opened=False, color='#000'),
        ], style={
                  'padding':'1rem', 
                  'display':'flex',
                  'justifyContent':'Space-between',
                   'boxShadow': 'rgba(0, 0, 0, 0.05) -3px 3px 5px',
                   "paddingLeft":"17px",
                   "paddingTop":"15px",
                   "borderBottom":"1px solid #2B454E",
        }),
        html.P(
            "Menu", style={'fontFamily':'Nunito','fontWeight':'700', 'fontSize':'1.2rem', 'padding':'17px'}
        ),
        dbc.Nav(
            [
                dmc.NavLink(
                    label="Dashboard",
                    icon=get_icon(icon="bi:house-door-fill"),
                    childrenOffset=28,
                    opened=False,
                    variant="subtle",
                    children=[
                        dmc.NavLink(label="Resumo", style={'color':'rgb(98 98 98)'}, href="/dashboard"),
                        dmc.NavLink(label="Vendas", style={'color':'rgb(98 98 98)'}, href="/dashboard?sales"),
                        #dmc.NavLink(label="Ganhos", style={'color':'rgb(98 98 98)'}, href="/dashboard?page-2"),
                        #dmc.NavLink(label="Obstáculos", style={'color':'rgb(98 98 98)'}),
                    ],
                ),
                dmc.NavLink(
                    label="Dados",
                    icon=get_icon(icon="material-symbols:data-exploration"),
                    childrenOffset=28,
                    opened=False,
                    variant="subtle",
                    children=[
                        dmc.NavLink(label="Carregar ficheiro", style={'color':'rgb(98 98 98)'}, href="/dashboard?uploadFile"),
                        dmc.NavLink(label="Meus ficheiros", style={'color':'rgb(98 98 98)'}, href="/dashboard?analyzeFile"),
                    ],
                ),
                dmc.NavLink(
                    label="AED",
                    icon=get_icon(icon="gis:statistic-map"),
                    childrenOffset=28,
                    variant="subtle",
                    href="/dashboard?AED"
                ),
                dmc.NavLink(
                    label="Fatores",
                    icon=get_icon(icon="material-symbols:fact-check"),
                    childrenOffset=28,
                    opened=False,
                    variant="subtle",
                    children=[
                        dmc.NavLink(label="Externos", style={'color':'rgb(98 98 98)'}, href="/dashboard?externalFactors"),
                        dmc.NavLink(label="Internos", style={'color':'rgb(98 98 98)'},)
                    ],
                ),
                dmc.NavLink(
                    label="Previsão",
                    icon=get_icon(icon="carbon:forecast-lightning"),
                    childrenOffset=28,
                    opened=False,
                    variant="subtle",
                    children=[
                        dmc.NavLink(label="Nova previsão", style={'color':'rgb(98 98 98)'}, href="/dashboard?forecast"),
                        dmc.NavLink(label="Consultar", style={'color':'rgb(98 98 98)'}, href="/dashboard?pastPredictions"),
                    ],
                ),
                dmc.NavLink(
                    label="Relatórios",
                    icon=get_icon(icon="mdi:report-areaspline"),
                    childrenOffset=28,
                    variant="subtle",
                ),
                dmc.NavLink(
                    label="Registos",
                    icon=get_icon(icon="mingcute:task-2-fill"),
                    childrenOffset=28,
                    opened=False,
                    variant="subtle",
                    styles={"icon":{"postion": 'absolute'}},
                    children=[
                        dmc.NavLink(label="Registar Tarefas", style={'color':'rgb(98 98 98)'}, href="/dashboard?tasks"),
                        dmc.NavLink(label="Registar Promoções", style={'color':'rgb(98 98 98)'}, href="/dashboard?promotions"),
                       # dmc.NavLink(label="Limpar o Quadro", style={'color':'rgb(98 98 98)'}),
                    ],
                ),
            ],
            vertical=True,
            pills=True,
            style={"paddingLeft":"10px"}
        ),
    ],
    style=SIDEBAR_STYLE,
    id='sidebar-dashboard',
)


@callback(Output("sidebar-dashboard", "style"), Input("burger-button", "opened"))
def open(opened):
    SIDEBAR_STYLE_CLOSE = {
    "position": "relative",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "backgroundColor": "#fcfcfc",
    "transition": 'all .5s',
    "height":"100vh",
    }
    
    SIDEBAR_STYLE_OPEN = {
    "position": "relative",
    "top": 0,
    "left":'0px',
    "bottom": 0,
    "width": "8rem",
    "backgroundColor": "#fcfcfc",
    "transition": 'all .5s',
    "height":"100vh",
    }
    if opened == False:
        return SIDEBAR_STYLE_CLOSE
    elif opened == True:
        return SIDEBAR_STYLE_OPEN