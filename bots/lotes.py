import json
import requests
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def eagle_pesos(farm_id, token):
    url = 'http://192.168.100.33:8008'
    url += f'/herd/?farm_id={farm_id}'
    lotes = requests.get(url, headers={'Authorization': f'Bearer {token}'})

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

    msg += '/inicial: Volta para o menu inicial\n'
    msg += '/lotes: Situação dos lotes'

    return msg