from dash import html, dcc, callback, Output, Input, State
import plotly.express as px
from api.chartsAPI import TemplateChart
from api.clientApp import GetAllCollectionNames, GetCollectionByName
import plotly.graph_objects as go
import dash_mantine_components as dmc
import pandas as pd
import base64
import plotly.io as pio
from report.reports import convert_html_to_pdf

global report_html
report_html = ''
template = TemplateChart
width = 600
height = 600
global figures

DatasetsNames = GetAllCollectionNames()
PanelMultiSelectOptions = [DatasetsNames[0]]
resume = html.Div([
    
    dcc.Download(id="download-resume"),
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    dcc.Store(id='dataset-names-storage', storage_type='local'),
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Painel de Resumo', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Fontes selecionadas para análise:', style={"font":"1.2rem Nunito", "color":"#fff"}),
                        dmc.MultiSelect(
                        label="",
                        placeholder="Select all you like!",
                        id="panel-dataset-multi-select",
                        value=PanelMultiSelectOptions,
                        data=[
                            {"value": "react", "label": "React"},
                            {"value": "ng", "label": "data 2015-2020"},
                            {"value": "svelte", "label": "Svelte"},
                            {"value": "vue", "label": "data 2020 - 2022"},
                        ],
                        style={"width": 400, "marginBottom": 10,"fontSize":"1.2rem"},
                        ),
                    ])
                ])
            ),
            html.Div(
            dmc.Button("Gerar relatório", style={"background":"#fff", "color":"#000","font":"3.2rem Nunito","marginTop":"1.2rem"}, id="generate-report"),
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    
    dcc.Loading(children=[
        html.Div(id='report-output-resume', className='report_output'),
            html.Div(
                [
                    html.Div([
                        html.Div([dcc.Graph(id='graph1', className='dbc')],style={"width":"31.5%"}),
                        html.Div([dcc.Graph(id='graph2', className='dbc')], style={"width":"31.5%"}),
                        html.Div([dcc.Graph(id='graph3', className='dbc')], style={"width":"31.5%"}),
                    ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
                    html.Div([
                        html.Div([dcc.Graph(id='graph4', className='dbc')], style={"width":"53%"}),
                        html.Div([dcc.Graph(id='graph5', className='dbc')], style={"width":"42%"}),
                    ], style={"display":"flex","gap":"10px","justifyContent":"center","background":"#F0F0F0", "padding":"10px 0"}),
                ]
                , style={"width":"100%","height":"65vh", "min-Height":"55vh"})
            ], color="#2B454E", type="dot", fullscreen=False,),
])


@callback(Output("graph1", "figure"),
          Output("graph2", "figure"),
          Output("graph3", "figure"),
          Output("graph4", "figure"),
          Output("graph5", "figure"),
          Input("panel-dataset-multi-select", "value")
          )
def select_value(value):
    global figures
    figures = []
    sales_train_all_df = getColections(value)
    fig1 = go.Figure() 

    Y = len(sales_train_all_df['Year'].unique())
    suffix = ''
    if Y > 0:
        suffix= " Ano(s)"
    else:
        Y = int(sales_train_all_df['Month'].max())
        suffix= " Meses"

    fig1.add_trace(go.Indicator(
            title = {"text": f"<span style='font-size:150%'>Período de Análise </span><br><br><span>{sales_train_all_df['Year'].min()} à {sales_train_all_df['Year'].max()}</span>"},
            value = (Y),
            number = {'suffix': suffix}
    ))

    df2_dataframe = sales_train_all_df
    df2_dataframe[['Date', 'Sales']].rename(columns = {'Date': 'date', 'Sales':'sales'})


    df2 = df2_dataframe.groupby(['Date'])['Sales'].sum().reset_index()
    df2.sort_values(ascending=False, inplace=True, by='Sales')

    Year = len(sales_train_all_df['Year'].unique())

    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(mode='number+delta',
            title = {"text": f"<span style='font-size:150%'>Maior N% de Vendas Diárias <br> em {Year} ano(s)</span><br><span style='font-size:70%'> em relação a média</span><br>"},
            value = df2['Sales'].iloc[0],
            number = {'suffix': " Vendas"},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df2['Sales'].mean()}
    ))


    df3 = df2_dataframe.groupby(['Date'])['Customers'].sum().reset_index()
    df3.sort_values(ascending=True, inplace=True, by='Customers')

    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(mode='number+delta',
            title = {"text": f"<span style='font-size:150%'>Menor N% de Clientes Diários <br> em {Year} ano(s)</span><br><span style='font-size:70%'> em relação a média</span><br>"},
            value = df3['Customers'].iloc[0],
            number = {'suffix': " Clientes"},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df3['Customers'].mean()}
    ))


    df4 = sales_train_all_df[sales_train_all_df.columns[1:6]].head(10)
    df4.drop('Unnamed: 0', axis=1, inplace=True)
    
    fig4 = go.Figure()
    fig4.add_trace(
        go.Table(
            header=dict(
                values=df4.columns,
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df4[k].tolist() for k in df4.columns[0:,]],
                align = "left")
        ))

    fig4.update_layout(
        showlegend=False,
        title_text="Amostra dos dados a serem analisados",
    )


    df5 = sales_train_all_df.groupby('Month')['Sales'].sum().reset_index()

    fig5 = px.pie(df5, values='Sales', names='Month', title='Distribuição das receitas por mês')
    
    figures.insert(0, fig1)
    figures.insert(1, fig2)
    figures.insert(2, fig3) 
    figures.insert(3, fig4)
    figures.insert(4, fig5)

    fig1.update_layout(height=230)
    fig2.update_layout(height=230)
    fig3.update_layout(height=230)
    fig4.update_layout(height=430)
    fig5.update_layout(height=430)
    return fig1, fig2, fig3, fig4, fig5


@callback(Output('panel-dataset-multi-select', component_property='value'),
          Output('panel-dataset-multi-select', component_property='data'),
                Input('interval_db', component_property='n_intervals'),
              )
def SetDataValuesOnCompont(interval_db):
    value = PanelMultiSelectOptions
    return value, DatasetValues()[1]

def DatasetValues():
    data = []
    for name in DatasetsNames:
        data.append({"value": f"{name}", "label": f"{name.split('-')[0]}"})
    return DatasetsNames, data

@callback(
    Output('dataset-names-storage', 'data', allow_duplicate=True),
    Input("panel-dataset-multi-select", "value"),
    prevent_initial_call=True
)
def save_param_panelOption(value):
    global PanelMultiSelectOptions
    PanelMultiSelectOptions = value
    return PanelMultiSelectOptions

def getColections(Names):
    df_PD = pd.DataFrame()
    for name in Names:
        df_PD =pd.concat((df_PD, pd.DataFrame(GetCollectionByName(name))))
    
    df_PD['Year'] = pd.DatetimeIndex(df_PD['Date']).year
    df_PD['Month'] = pd.DatetimeIndex(df_PD['Date']).month
    df_PD['Day'] = pd.DatetimeIndex(df_PD['Date']).day
    return df_PD

@callback(
    Output('report-output-resume','children'),
    Output('report-output-resume', 'style', allow_duplicate=True),
    Input('generate-report','n_clicks'),
    prevent_initial_call=True
)
def generate_report(n_clicks):
    descriptionData = []
    captionData = []

    descriptionData.insert(0,'this is a description of data in graph number 1')
    captionData.insert(0, 'Período de Análise dos Dados')

    descriptionData.insert(1, 'this is a description of data in graph number 2')
    captionData.insert(1,'Maior Número de Vendas Diárias')

    descriptionData.insert(2, 'this is a description of data in graph number 2')
    captionData.insert(2,'Maior Número de Clientes Diários')

    descriptionData.insert(3, 'this is a description of data in graph number 2')
    captionData.insert(3,'Amostra dos dados a serem analisados')

    descriptionData.insert(4, 'this is a description of data in graph number 2')
    captionData.insert(4,'Distribuição de receitas por mês')
    
    images = [base64.b64encode(pio.to_image(figure, format='png', width=width, height=height)).decode('utf-8') for figure in figures]
    
    global report_html
    report_html = ''
    for index, image in enumerate(images):
        _ = template
        _ = _.format(image=image, caption=captionData[index], description=descriptionData[index], width=width, height=height)
        report_html += _

    if n_clicks is not None:
        return [
            html.Div([
                html.Div('Download', id="dowload-report"),
                html.Div('Fechar', id='close-report'),
            ], className="wrapper-btn-report"),
            html.Iframe(srcDoc=report_html, width='100%', height='100%')
            ], {'display': 'block'}
    else:
        return '', {'display': 'none'}
    
@callback(
    Output('report-output-resume', 'style'),
    Input('close-report','n_clicks'),
)
def close_report(n_clicks):
    if n_clicks is not None:
       return {'display': 'none'}
    else:
        return {'display': 'block'}
    
@callback(
    Output('download-resume', 'data'),
    Input('dowload-report','n_clicks'),
)
def dowload_report(n_clicks):
    if n_clicks is not None:
        convert_html_to_pdf(report_html,'report_html.pdf')
        return dcc.send_file(
        "./report_html.pdf", "resume_report.pdf")
