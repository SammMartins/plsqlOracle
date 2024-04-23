from turtle import color
import plotly.express as px
from dataset import df1, df2
from utils import data_semana_ini, data_semana_fim, format_number

start_of_week = data_semana_ini()
end_of_week = data_semana_fim()
df = df2(start_of_week, end_of_week)

if df.empty:
    print("DataFrame está vazio. Não é possível criar o gráfico.")
else:
    alvo = df[2].mean() # Média de vendas

    # ------------------------- GRÁFICO VENDA POR RCA -------------------------
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
        textfont = dict(color='black', family='Arial Black'),
        name = 'Linha tracejada é a média de vendas dos RCA'
    )

    grafico_vend_sup.add_shape(
        type='line',
        line=dict(dash='dash', color='white'),
        y0=alvo,
        y1=alvo,
        x0=0,
        x1=1,
        xref='paper',
        yref='y'
    )


    # ------------------------- GRÁFICO TOP VENDA POR RCA -------------------------
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
        textfont = dict(color='black', family='Arial Black')
    )

    df_2 = df[df[df.columns[0]] == 2]
    df_8 = df[df[df.columns[0]] == 8]


    # ------------------------- GRÁFICO VENDA POR RCA TIME SUL -------------------------    
    grafico_top_rca2 = px.bar(
        df_2,
        x = df.columns[1],
        y = df.columns[2], 
        title = "VENDAS POR RCA NA SEMANA ATUAL - SUL",
        range_y = (0, df[2].max()),
        color = df.columns[2],
        color_continuous_scale = ["red", "yellow", "green"]
    )

    grafico_top_rca2.update_traces(
        text = df_2[df_2.columns[2]].apply(lambda x: format_number(x, 'R$')),
        textposition = 'inside',
        textfont = dict(color='black', family='Arial Black')
    )

    grafico_top_rca2.add_shape(
        type='line',
        line=dict(dash='dash', color='white'),
        y0=alvo,
        y1=alvo,
        x0=0,
        x1=1,
        xref='paper',
        yref='y'
    )

    # ------------------------- GRÁFICO VENDA POR RCA TIME SERTÃO -------------------------
    grafico_top_rca8 = px.bar(
        df_8,
        x = df.columns[1],
        y = df.columns[2], 
        title = "VENDAS POR RCA NA SEMANA ATUAL - SERTÃO",
        range_y = (0, df[2].max()),
        color = df.columns[2],
        color_continuous_scale = ["red", "yellow", "green"]
    )

    grafico_top_rca8.update_traces(
        text = df_8[df_8.columns[2]].apply(lambda x: format_number(x, 'R$')),
        textposition = 'inside',
        textfont = dict(color='black', family='Arial Black')
    )

    grafico_top_rca8.add_shape(
        type='line',
        line=dict(dash='dash', color='white'),
        y0=alvo,
        y1=alvo,
        x0=0,
        x1=1,
        xref='paper',
        yref='y'
    )