from dash import html


pastPredictions = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Previsões anteriores', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Aqui você poderá visualizar todas as previsões já realizadas', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    html.Div([
       html.P("2017/05",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("2018/24",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("2019/17",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("2020/15",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("2021/08",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),  
    ], style={"display":"flex", "gap":"10px", "alignItems":"center", "paddingLeft":"3rem"}),
    html.Div([
        html.P("Algumas informações",style={"font":"1.8rem Nunito"}),
        html.P("Mostrar dados do arquivo",style={"font":"1.8rem Nunito"})
    ], style={"background":"#c4c4c4","width":"30rem","height":"76vh"})
], style={"display":"flex", "gap":"10px", "justifyContent":"space-between","alignItems":"center", "height":"76vh", "background":"#F0F0F0"}),
])