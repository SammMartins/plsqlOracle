import pandas as pd
import pandas as pd
import datetime
import pandas as pd
import base64
from io import BytesIO

# ----------------- Função para formatar números -----------------
def format_number(value):
    return 'R${:,.0f}'.format(value).replace(",", "v").replace(".", ",").replace("v", ".")

# ----------------- Função Define datas -----------------
def data_semana_ini(): # retorna data de início da semana
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week

def data_semana_fim(): # retorna data de fim da semana
    return datetime.date.today()

# ---------------- Função para criar um link de download da tabela ----------------
def getTableXls(df):
    """Gera um link permitindo que os dados de um DataFrame sejam baixados
    no formato de arquivo xls, torna-o em um objeto de string base64 e devolve um link de download.
    """
    to_excel = BytesIO()
    df.to_excel(to_excel, index=False)  # removido o argumento encoding
    to_excel.seek(0)
    b64 = base64.b64encode(to_excel.read()).decode()  # algumas conversões de strings <-> bytes necessárias aqui
    href = f'<br><a class="download" href="data:application/vnd.ms-excel;base64,{b64}" download="TabelaExcel.xls">BAIXAR</a>'
    return href
