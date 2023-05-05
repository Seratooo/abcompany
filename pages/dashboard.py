import dash
from dash import Input, Output, dcc, html, callback
from subpages import resumePage, salesPage, uploadPage, analyzeFilesPage, forecastPage, pastPredictionsPages
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
UploadPage = uploadPage.upload
AnalyzeFilePage = analyzeFilesPage.analyzeFiles
ForecastPage = forecastPage.forecast
PastPredictionsPage = pastPredictionsPages.pastPredictions

@callback(
          Output("page-content", "children"), 
          [Input("url", "pathname"), Input("url", "search")])
def render_page_content(pathname, search):
    link = f'{pathname}{search}'
    if link == "/dashboard":
        return ResumePage
    elif  link == "/dashboard?sales":
        return SalesPage
    elif  link == "/dashboard?uploadFile":
        return UploadPage
    elif  link == "/dashboard?analyzeFile":
        return AnalyzeFilePage
    elif  link == "/dashboard?forecast":
        return ForecastPage
    elif  link == "/dashboard?pastPredictions":
        return PastPredictionsPage
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )