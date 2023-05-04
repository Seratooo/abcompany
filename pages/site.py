import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='This is our Dashboard page'),

    html.Div(children='''
        This is our dasboard page content.
    '''),

])