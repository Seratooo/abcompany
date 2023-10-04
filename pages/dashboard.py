import dash
from dash import Input, Output, dcc, html, callback, State
from subpages import resumePage, salesPage, uploadPage, analyzeFilesPage, forecastPage, pastPredictionsPages, externalFactorsPage, AEDPage, tasksPage, promotionPage, internalFactorsPage
from components import headerComponent, sidebarComponent, containerComponent
dash.register_page(__name__,  suppress_callback_exceptions=True)


#COMPOENTS
sidebar = sidebarComponent.sidebar
header = headerComponent.header
content = containerComponent.content

DashboardWrapper = html.Div([header, content], style={"width":"100%"})

layout = html.Div([
    dcc.Location(id='url2', refresh=True),
    dcc.Location(id='url', refresh=False), 
    sidebar, 
    DashboardWrapper
], style={"display":"flex"})


#PAGES
ResumePage = resumePage.resume 
SalesPage = salesPage.sales 
UploadPage = uploadPage.upload
AnalyzeFilePage = analyzeFilesPage.analyzeFiles
ForecastPage = forecastPage.forecast
PastPredictionsPage = pastPredictionsPages.pastPredictions
ExternalFactorsPage = externalFactorsPage.externalFactorsPage
InternalFactorsPage = internalFactorsPage.internalFactorsPage
AEDPage = AEDPage.AED
TaskSPage = tasksPage.tasks
PromtionPage = promotionPage.promotion

@callback(
    Output('url2','pathname', allow_duplicate=True),
    Input('url2','url'),
    State('User', 'data'),
    prevent_initial_call='initial_duplicate'
)
def isUserLog(_, data):
    if data == {}:
        return '/login'

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
    elif  link == "/dashboard?externalFactors":
        return ExternalFactorsPage
    elif  link == "/dashboard?internalFactors":
        return InternalFactorsPage
    elif  link == "/dashboard?AED":
        return AEDPage
    elif  link == "/dashboard?tasks":
        return TaskSPage
    elif  link == "/dashboard?promotions":
        return PromtionPage
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )