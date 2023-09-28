from dash import html

CONTENT_STYLE = {
    "height":"100vh",
    "overflow":"scroll",
    'zIndex': 2,
    'position': 'relative',
    "backgroundColor": "#f5f5f6",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)