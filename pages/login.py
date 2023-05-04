import dash
from dash import Dash, html,register_page, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import abcompany

dash.register_page(__name__)

layout = html.Div([
    abcompany.LoginComponent(id='LoginComponent'),
]) 

