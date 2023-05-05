from dash import html


analyzeFiles = html.Div([
    html.Div([
            html.Div(
                html.Div([
                    html.H3('Analisar arquivos', style={"font":"1.8rem Nunito","fontWeight":"700", "color":"#fff","marginBottom":".8rem"}),
                    html.Div([
                        html.P('Analise um ficheiro contendo os seus dados ou junte varios ficheiros em um só', style={"font":"1.2rem Nunito", "color":"#fff"}),
                    ])
                ])
            )
        ], style={"display":"flex","background":"#2B454E", "justifyContent":"space-between", "alignItems":"center", "padding":"2rem"}),
    html.Div([
    html.Div([
       html.P("File 1",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("File 2",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("File 3",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("File 4",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),
       html.P("File 5",style={"font":"1.8rem Nunito","background":"#c4c4c4", "padding":"3rem"}),  
    ], style={"display":"flex", "gap":"10px", "alignItems":"center", "paddingLeft":"3rem"}),
    html.Div([
        html.P("Juntar arquivos selecionados",style={"font":"1.8rem Nunito"}),
        html.P("Mostrar dados do arquivo",style={"font":"1.8rem Nunito"})
    ], style={"background":"#c4c4c4","width":"30rem","height":"76vh"})
], style={"display":"flex", "gap":"10px", "justifyContent":"space-between","alignItems":"center", "height":"76vh", "background":"#F0F0F0"}),
])