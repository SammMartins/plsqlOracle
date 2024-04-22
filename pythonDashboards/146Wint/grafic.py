import plotly.express as px
from dataset import df1, df2
from utils import data_semana_ini, data_semana_fim, format_number

start_of_week = data_semana_ini()
end_of_week = data_semana_fim()
df = df2(start_of_week, end_of_week)

if df.empty:
    print("DataFrame está vazio. Não é possível criar o gráfico.")
else:
    grafico_vend_sup = px.bar(
        df,
        x = df.columns[1],
        y = df.columns[2], 
        title = "VENDAS POR RCA NA SEMANA ATUAL",
        range_y = (0, df[2].max()),
        color = df.columns[2],
        color_continuous_scale = ["red", "yellow", "green"]
    )

    grafico_vend_sup.update_traces(
        text = df[df.columns[2]].apply(lambda x: format_number(x, 'R$')),
        textposition = 'inside',
        textfont = dict(color='black')
    )

    grafico_top_rca = px.bar(
        df.head(5),
        x = df.columns[1],
        y = df.columns[2], 
        title = "TOP 5 RCA DA SEMANA ATUAL",
        range_y = (0, df[2].max()),
        color = df.columns[2]
    )

    grafico_top_rca.update_traces(
        text = df[df.columns[2]].apply(lambda x: format_number(x, 'R$')),
        textposition = 'inside',
        textfont = dict(color='black')
    )