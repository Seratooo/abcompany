import dash
from dash import Input, Output, dcc, html, callback
from subpages import resumePage, salesPage
from data import configs
from components import headerComponent, sidebarComponent, containerComponent
dash.register_page(__name__,  suppress_callback_exceptions=True)


#DATABASE
sales_train_all_df = configs.getDatabase()

#COMPOENTS
sidebar = sidebarComponent.sidebar
header = headerComponent.header
content = containerComponent.content

DashboardWrapper = html.Div([header, content], style={"width":"100%"})

layout = html.Div([dcc.Location(id='url', refresh=False), sidebar, DashboardWrapper], style={"display":"flex"})


#PAGES
ResumePage = resumePage.resume 
SalesPage = salesPage.sales 

@callback(
          Output("page-content", "children"), 
          [Input("url", "pathname"), Input("url", "search")])
def render_page_content(pathname, search):
    link = f'{pathname}{search}'
    if link == "/dashboard":
        return ResumePage
    elif  link == "/dashboard?sales":
        return SalesPage
    elif  link == "/dashboard?page-2":
        return html.P("This is the content of back page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )