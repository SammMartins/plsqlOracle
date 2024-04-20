def format_number(value, prefix = ''):
    return f'{prefix}{value:,.2f}'.replace(',', '#').replace('.', ',').replace('#', '.')