import json
import requests
from datetime import datetime
from config import JETBOV_TOKEN
url = 'http://192.168.100.33:8008'


def eagle_saldo(farm_id):
    global url # 32086
    url += f'/transaction/?farm_id={farm_id}'
    saldo = requests.get(url, headers={'Authorization': f'Bearer {JETBOV_TOKEN}'})
    print('-----------------------------')
    print(saldo.json()[0])
    print('-----------------------------')
    data = datetime.today().strftime("%d/%m/%Y")
    msg = ''
    for conta in ['Itaú', 'C6 Bank']:
        msg += f'{data} - Conta: {conta}, saldo: R$ 1520,00 {saldo}\n'

    return str(saldo.json()[0])

