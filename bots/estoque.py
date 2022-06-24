import json
import requests
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def eagle_abaixo_do_minimo(farm_id, token):
    url = 'http://192.168.100.33:8008'
    url += f'/item/minimum/?farm_id={farm_id}'
    items = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    print('-------------estoque-----------------')
    print(items.json())
    print('-------------------------------------')
    '''
    {'name': 'Sal Mineral', 
    'farm': 'Demonstração - Santa Maria - RS1', 
    'min_replenish_level': 20, 
    'quantity': -1300.0}
    '''

    cotacao = items.json()[0].get('day_quote')
    data = datetime.today().strftime("%d/%m/%Y")
    msg = ''
    msg += 'Item   (mínimo)  Saldo\n'
    msg += '--------------------------------------------\n' 
    for item in items.json():
        name = item.get('name')
        minimo = item.get('min_replenish_level')
        saldo = str(item.get('quantity'))

        msg += f'{name}  ({minimo})  {saldo}\n\n'

    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/estoque: Situação dos estoque'

    return msg