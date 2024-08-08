# Importa bibliotecas necessárias
from io import BytesIO
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import base64
from reportlab.pdfgen import canvas
from typing import Final
import streamlit as st

# Importa a funções úteis 
from utils_pdf import regua, reticula, df_Exemplo

def flash_pdf(df):
    if df.empty:
        return "Nenhum dado para exibir"

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Se for um DataFrame, converta para lista de listas
    if hasattr(df, 'values'):
        data = [df.columns.tolist()] + df.values.tolist()

    # Cria a tabela
    table = Table(data)

    # Define o estilo da tabela
    cor_1: Final = colors.HexColor("#070717")  # Azul escuro
    cor_2: Final = colors.HexColor("#ffffff")  # Branco
    cor_3: Final = colors.HexColor("#073c55")  # Azul claro 
    positivo: Final = colors.HexColor("#35DB69")  # Verde
    negativo: Final = colors.HexColor("#DB3835")  # Vermelho

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), cor_1),
        ('TEXTCOLOR', (0, 0), (-1, 0), cor_2),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), cor_2),
        ('GRID', (0, 0), (-1, -1), 1, cor_3),
    ])

    # Índice da coluna "status"
    status_col_idx = 8  

    # Estilizando as células da coluna "status" com base nos valores
    for i, row in enumerate(data[1:], start=1):  # Começa do 1 para ignorar o cabeçalho
        if row[status_col_idx] == "↑↑↑":
            style.add('BACKGROUND', (status_col_idx, i), (status_col_idx, i), positivo)
        elif row[status_col_idx] == "↓↓↓":
            style.add('BACKGROUND', (status_col_idx, i), (status_col_idx, i), negativo)

    table.setStyle(style)

    # Adiciona a tabela ao PDF
    elements = [table]
    pdf.build(elements)

    # Desenha a régua e a retícula no mesmo PDF
    buffer.seek(0)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    regua(c, "Horizontal")
    reticula(c)
    c.showPage()
    c.save()

    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<br><a class="download" href="data:application/pdf;base64,{b64}" download="TabelaPDF.pdf">BAIXAR</a>'
    return href