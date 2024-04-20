from dataset import df1, df2
import pandas as pd
from dataset import df1, df2
import pandas as pd
import datetime

# ----------------- Função para formatar números -----------------
def format_number(value, prefix = ''):
    return f'{prefix}{value:,.2f}'.replace(',', '#').replace('.', ',').replace('#', '.')

# ----------------- Função Define datas -----------------
def data_semana_ini(): # retorna data de início da semana
    ini = datetime.date.today()
    return ini - datetime.timedelta(days=ini.weekday())
def data_semana_fim(): # retorna data de fim da semana
    hoje = datetime.date.today()
    return hoje + datetime.timedelta(days=6 - hoje.weekday())


