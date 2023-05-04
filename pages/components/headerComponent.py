from dash import html
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
}

header = html.Div(html.Div([
    dmc.Group(
    children=[
        dmc.Avatar("JD", color="green", radius="xl",style={"marginTop":"6px"}),
        html.P("Joe Dole", style={'fontFamily':'Nunito',"marginTop":"6px"})
    ],
    style={"display":"flex"}
    )
], style=HEADAER_STYLE))