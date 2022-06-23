import json
import requests
import locale
from datetime import datetime

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

    return msg

#financeiro
def eagle_prx_pgtos(farm_id, token):
    url = 'http://192.168.100.33:8008'
    url += f'/transaction/?farm_id={farm_id}'
    saldo = requests.get(url, headers={'Authorization': f'Bearer {token}'})

    data = datetime.today().strftime("%d/%m/%Y")

    return str(saldo.json()[0])
