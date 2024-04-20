import plotly.express as px
from dataset import df1, df2
from utils import data_semana_ini, data_semana_fim

start_of_week = data_semana_ini()
end_of_week = data_semana_fim()
df = df2(start_of_week, end_of_week)

grafico_vend_sup = px.line(
    df,
    x = df.columns[1],
    y = df.columns[2], 
    title = "Vendas RCA's na semana atual",
    markers = True,
    range_y = (0, df1(start_of_week, end_of_week)[2].max()),
    color = df.columns[0],
    line_dash = df.columns[0]
)