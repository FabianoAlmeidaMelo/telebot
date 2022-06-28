import json
import requests
import locale
from datetime import datetime
from prettytable import PrettyTable

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def eagle_saldo(farm_id, token):
    url = 'http://192.168.100.33:8008'
    url += f'/transaction/balance/?farm_id={farm_id}'
    contas = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    data = datetime.today().strftime("%d/%m/%Y")

    msg = f'{data}\n'
    msg += 'Conta   saldo\n'
    msg += '--------------------------------------------\n' 
    for conta in contas.json():
        name = conta.get('account_name')
        valor = round(conta.get('balance'), 2)
        valor = locale.currency(valor, grouping=True, symbol=None)
        valor = f'R$ {valor}'
        msg += f'{name}  {valor}\n\n'
    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/financeiro: Informações financeiras'
    return msg

def _eagle_prx_pgtos(farm_id, token):
    # url = 'http://192.168.100.33:8008'
    # url += f'/transaction/balance/?farm_id={farm_id}'
    # contas = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    data = datetime.today().strftime("%d/%m/%Y")
    refs = [
        ('ração', 'R$ 2.000,00', '27/06/2022'),
        ('Manut. trator','R$ 1.500,00', '01/07/2022'),
        ('Veterinário', 'R$ 7.500,00', '10/07/2022'),
        ('Financiamento', 'R$ 10.500,00', '11/07/2022')
    ]

    msg = f'{data}\n'
    msg += 'Referência:   Próximos (Pagamentos) data\n'
    msg += '--------------------------------------------\n' 
    for r in refs:
        ref = r[0]
        valor = r[1]
        data = r[2]
        msg += f'{ref}  ({valor}) {data}\n\n'
    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/financeiro: Informações financeiras'
    return msg

def eagle_prx_pgtos(farm_id, token):
    table = PrettyTable()
    data = datetime.today().strftime("%d/%m/%Y")
    refs = [
        ('ração', 'R$ 2.000,00', '27/06/2022'),
        ('Manut. trator','R$ 1.500,00', '01/07/2022'),
        ('Veterinário', 'R$ 7.500,00', '10/07/2022'),
        ('Financiamento', 'R$ 10.500,00', '11/07/2022')
    ]
    table.field_names = ["Referência", "Próximos Pagamentos", "data"]

    msg = f'{data}\n'

    for r in refs:
        table.add_row(r)


    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/financeiro: Informações financeiras'
    return table

def eagle_prx_recebimentos(farm_id, token):
    # url = 'http://192.168.100.33:8008'
    # url += f'/transaction/balance/?farm_id={farm_id}'
    # contas = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    data = datetime.today().strftime("%d/%m/%Y")

    refs = [
        ('Venda 021', 'R$ 20.000,00', '09/07/2022'),
        ('Venda Silagem','R$ 3.8500,00', '13/07/2022'),
        ('Venda Angus 326', 'R$ 75.500,00', '30/07/2022')
    ]

    msg = f'{data}\n'
    msg += 'Referência:   Próximos (Recebimentos) data\n'
    msg += '--------------------------------------------\n' 
    for r in refs:
        ref = r[0]
        valor = r[1]
        data = r[2]
        msg += f'{ref}  ({valor}) {data}\n\n'
    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/financeiro: Informações financeiras'
    return msg
