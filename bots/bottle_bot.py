import json
import requests
import time
from bottle import (
    run, post, get, response, request as bottle_request
)
from config import BOT_API_URL, BOT_API_KEY



url_upd = f"{BOT_API_URL}/getUpdates"

lidas = {}

def sendMessage(chat_id, text):
    url_send = f"{BOT_API_URL}/sendMessage?chat_id={chat_id}&text={text}"
    sended = requests.get(url_send)
    print(sended)

def getUpdates():
    received = requests.get(url_upd)
    r = received.json()["result"][-1]
    print('--------------------')
    print(r)
    print('--------------------')

while True: 
    getUpdates()
    time.sleep(5)



if __name__ == '__main__':
    run(host='localhost', port=8070, debug=True)
