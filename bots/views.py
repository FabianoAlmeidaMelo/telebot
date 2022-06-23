import json
import requests
import locale
from datetime import datetime

url = 'http://192.168.100.33:8008'
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#financeiro
def eagle_saldo(farm_id, token):
    global url
    url += f'/transaction/balance/?farm_id={farm_id}'
    contas = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    print('-----------`o/------------------')
    print(contas.json())
    print('-----------------------------')
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
    global url
    url += f'/transaction/?farm_id={farm_id}'
    saldo = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    print('--------****----------------')
    print(saldo.json()[0])
    print('-----------------------------')
    data = datetime.today().strftime("%d/%m/%Y")

    return str(saldo.json()[0])

#lotes
def eagle_pesos(farm_id, token):
    global url
    url += f'/herd/?farm_id={farm_id}'
    lotes = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    print('--------****----------------')
    print(lotes.json())
    print('-----------------------------')

    cotacao = lotes.json()[0].get('day_quote')
    data = datetime.today().strftime("%d/%m/%Y")
    msg = f'@ BOI ESALQ/BMF ({data}):  R$ {cotacao}\n\n'
    msg += 'Nome   (Nr animais)  peso total   Cotação\n'
    msg += '--------------------------------------------\n' 
    for lote in lotes.json():
        name = lote.get('name')
        animais = str(lote.get('animalCount'))
        peso = lote.get('total_weight')
        valor = round(lote.get('quote'), 2)
        valor = locale.currency(valor, grouping=True, symbol=None)
        valor = f'R$ {valor}'
        msg += f'{name}  ({animais})\n {peso}Kg {valor}\n\n'

    return msg