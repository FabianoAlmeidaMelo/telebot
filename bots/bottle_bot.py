import json
import requests
import time
from bottle import (
    run, post, get, response, request as bottle_request
)
from config import BOT_API_URL, BOT_API_KEY



url_upd = f"{BOT_API_URL}/getUpdates"

lidas = {155701671: True, 155701672: True} #155701692,

cadastrados = {
    1284373359: '5512997164534',
    # 1534403426: '5512982239764'
}

phone_numbers = {
    '5512982239764': True,
    '5512997164534': True
}


def _sendMessage(chat_id, text):
    '''
    para enviar qualquer mensagem para um user que
    você possua o chat_id
    por exemplo:
    - um alerta de que um lote chegou no peso de venda
    - um item de estoque ficou abaixo do mínimo, ou zerou no estoque
    '''
    url = "{BOT_API_URL}/sendMessage?chat_id={chat_id}&text={text}".format(
        BOT_API_URL=BOT_API_URL,
        chat_id=chat_id,
        text=text
    )

    sended = requests.get(url)
    print(sended)


def reply_message(item):
    print('-----*-----')
    try:
        chat_id = item["message"]["chat"]["id"]
        user_id = item["message"]["from"]["id"]
        user_name = item["message"]["from"].get("username", user_id)
        headers = {'content-Type': 'application/json'}

        data = {
            "chat_id": "1534403426",
            "text": 'Preciso do seu número para autenticar',
            "reply_markup": 
                {"keyboard": [
                    [{"text": "Compartilhar_Telefone"}],
                    [{"text": "Download_video"}]
                ],
                "resize_keyboard": True,
                "one_time_keyboard": True}
            }

        url = "{BOT_API_URL}/sendMessage".format(
            BOT_API_URL=BOT_API_URL

        )
        r = requests.post(url, json=data)
        
        print('___sended___')
        print(r)
        print('*********___sended___***********')
        return r

    except Exception as e:
        print(e)

def send_button_tel_number(chat_id):
    url = "{BOT_API_URL}/sendMessage".format(
        BOT_API_URL=BOT_API_URL

    )
 
    payload = {
        'chat_id': chat_id,
        'text': "Envie seu número",
                'reply_markup': {'keyboard': [
                [
                    {'text': 'Enviar', 'request_contact': True},
                    {'text': 'Cacelar'}
                ]
            ]
        }
    }

    requests.post(url, json=payload)
 
def check_authorized(chat_id):
    if cadastrados.get(chat_id) is None:
        send_button_tel_number(chat_id)
    return True

def sendMessage(item):

    chat_id = item["message"]["chat"]["id"]
    user_id = item["message"]["from"]["id"]
    user_name = item["message"]["from"].get("username", user_id)
    text = item["message"]["text"]

    url_send = "{BOT_API_URL}/sendMessage?chat_id={chat_id}&text={text}".format(
        BOT_API_URL=BOT_API_URL,
        chat_id=chat_id,
        text=text
    )

    sended = requests.get(url_send)
    print(sended)

def getUpdates():
    received = requests.get(url_upd)
    data = received.json()
    for item in data["result"]:
        new_id = int(item["update_id"])
        print(new_id)

        print('**')
        print(item)
        print("**")

        chat_id = item["message"]["from"]["id"]

        authorized = check_authorized(chat_id)

        if authorized and item["message"].get("contact"):
            if cadastrados.get(chat_id) == item["message"]["contact"]:
                authorized = True
            else:
                authorized = False
                if lidas.get(new_id) is None:
                    msg = 'Não identifiquei o seu usuário como autorizado, '
                    msg += 'Peça ao administrador da Fazenda para te habilitar'
                    _sendMessage(chat_id, msg)
                    lidas[new_id] = True
        if authorized:

            if new_id > 155701692:
                if lidas.get(new_id) is None:
                    try:
                        print('--------------------')
                        print(item)
                        print('--------------------')
                        sendMessage(item)
                        # reply_message(item)

                        lidas[new_id] = True

                    except Exception as e:
                        raise e

while True: 
    getUpdates()
    time.sleep(2)

if __name__ == '__main__':
    run(host='localhost', port=8070, debug=True)
