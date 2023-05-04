from dash import html

CONTENT_STYLE = {
    "height":"100vh",
    "overflow":"scroll",
    'zIndex': 2,
    'position': 'relative',
}

content = html.Div(id="page-content", style=CONTENT_STYLE)