import dash
from dash import Dash, html,register_page
import abcompany

dash.register_page(__name__)

layout = html.Div([
    abcompany.LoginComponent(id='LoginComponent'),
], id="loginPage", style={"position":"relative", "zIndex":"2"}) 

