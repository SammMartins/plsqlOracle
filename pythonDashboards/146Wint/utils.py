import pandas as pd
import pandas as pd
import datetime

# ----------------- Função para formatar números -----------------
def format_number(value, prefix = ''):
    return f'{prefix}{value:,.2f}'.replace(',', '#').replace('.', ',').replace('#', '.')

# ----------------- Função Define datas -----------------
def data_semana_ini(): # retorna data de início da semana
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week

def data_semana_fim(): # retorna data de fim da semana
    return datetime.date.today()