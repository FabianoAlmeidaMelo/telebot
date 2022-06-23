import telebot
from telebot import types
import logging

from config import API_KEY
from views import (
    eagle_saldo,
    eagle_pesos
)
from config import JETBOV_TOKEN, phone_numbers
bot = telebot.TeleBot(API_KEY)

logger = telebot.logger

autenticated = {}

def cant_access(message):
    msg = 'Entre em contato com o administrador da sua Fazenda, para liberar seu acesso'
    bot.send_message(
        message.chat.id,
        msg
    )


@bot.message_handler(commands=["saldo"])
def get_saldo(message):
    farm_id = token = None
    farm_id = autenticated.get(message.from_user.id)['farm_id']
    token = autenticated.get(message.from_user.id)['token']

    if farm_id and token:
        msg = eagle_saldo(farm_id, token)
    else:
        msg: 'Não consegui identificar sua fazenda'
    bot.send_message(
        message.chat.id,
        msg
    )

@bot.message_handler(commands=["prx_pgtos"])
def get_prx_pgtos(message):
    farm_id = token = None
    farm_id = autenticated.get(message.from_user.id)['farm_id']
    token = autenticated.get(message.from_user.id)['token']

    if farm_id and token:
        msg = eagle_prx_pgtos(farm_id, token)
    else:
        msg: 'Não consegui identificar sua fazenda'
    bot.send_message(
        message.chat.id,
        msg
    )


@bot.message_handler(commands=["financeiro"])
def get_finance_options(message):
    menu = """
    {first_name}, sobre o que você quer saber:
    /saldo: Sado da conta principal
    /prx_pgtos: 10 próximos pagamentos em Aberto
    /prx_recebimentos: 10 próximos recebimentos em Aberto
    /pgtos_vencidos: Valor total dos Pagamentos vencidos em Aberto
    /recb_vencidos: Valor total dos Recebimentos vencidos em Aberto
    /inicial: Volta para o menu inicial
    Clique em uma das opções
    """.format(first_name=message.from_user.first_name)
    bot.reply_to(message, menu)

@bot.message_handler(commands=["estoque"])
def get_storage_options(message):
    menu = """
    Sobre o que você quer saber:
    /sem_saldo: Items sem saldos no estoque
    /abx_min: Items com saldo abaixo do mínimo
    /all_in: Todos items do estoque
    /inicial: Volta para o menu inicial
    Clique em uma das opções
    """
    bot.reply_to(message, menu)


@bot.message_handler(commands=["pesos"])
def get_pesos(message):
    farm_id = token = None
    farm_id = autenticated.get(message.from_user.id)['farm_id']
    token = autenticated.get(message.from_user.id)['token']

    if farm_id and token:
        msg = eagle_pesos(farm_id, token)
    else:
        msg: 'Não consegui identificar sua fazenda'
    bot.send_message(
        message.chat.id,
        msg
    )

@bot.message_handler(commands=["lotes"])
def get_lotes_options(message):
    menu = """
    Sobre o que você quer saber sobre seus Lotes:
    /pesos: Peso e cotação dos Lotes
    /ultima_pesagem: Dta da Última pesagem
    /inicial: Volta para o menu inicial
    Clique em uma das opções
    """
    bot.reply_to(message, menu)


@bot.message_handler(commands=["app"])
def get_app_options(message):
    '''
    app: pode retornar um resumo geral delas
    sem a necessidade de um novo menu
    '''
    menu = """
    Sobre o que você quer saber:
    /aprovadas: Total de atividades Aprovadas nesse mês
    /reprovaddas: Total de atividades Reprovadas nesse mês
    /pendentes: Total de atividades pendentes nesse mês
    /inicial: Volta para o menu inicial
    """
    bot.reply_to(message, menu)


@bot.message_handler(commands=["inicial"])
def get_inicial_menu(message):
    menu = """
    {first_name} aqui está o nosso menu inicial:
    /financeiro: Informações financeiras
    /estoque: Informações sobre seu estoque
    /lotes: Situação dos lotes
    /app: Atividades do aplicativo
    Clique em uma das opções
    """.format(first_name=message.from_user.first_name)
    bot.send_message(
        message.chat.id,
        menu
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    habilitado = bool(phone_numbers.get(message.contact.phone_number))
    if not autenticated.get(message.contact.user_id):
        if habilitado:
            autenticated[message.contact.user_id] = {
                'phone': message.contact.phone_number,
                'chat_id': message.contact.user_id,
                'farm_id': phone_numbers.get(message.contact.phone_number)['farm_id'],
                'token': phone_numbers.get(message.contact.phone_number)['token']
            }
        else:
            cant_access(message)
    if autenticated.get(message.contact.user_id) and habilitado:
        get_inicial_menu(message)


def autenticar(message):
    if message.contact and autenticated.get(message.from_user.id) is None:
        if phone_numbers.get(message.contact.phone_number):
            autenticated[message.contact.user_id] = {
                'phone': message.contact.phone_number,
                'chat_id': message.contact.user_id,
                'farm_id': phone_numbers.get(message.contact.phone_number)['farm_id'],
                'token': phone_numbers.get(message.contact.phone_number)['token']
            }
            return True
        else:
            cant_access(message)
            return False
    elif autenticated.get(message.from_user.id):
        return True
    else:
        return True


@bot.message_handler(func=autenticar)
def start(message):
    if autenticated.get(message.chat.id) is None:
        markup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True
        )
        button_phone = types.KeyboardButton(
            text="enviar o telefone",
            request_contact=True
        )
        markup.add(button_phone)
        bot.send_message(
            message.chat.id,
            'Seu telefone faz a autenticação',
            reply_markup=markup
        )
    elif phone_numbers.get(autenticated.get(message.from_user.id)['phone']) is None:
        msg = 'Entre em contato com o administrador da sua Fazenda, para liberar seu acesso'
        bot.send_message(
            message.chat.id,
            msg
        )

    else:
        menu = """
        Como posso te ajudar:
        /financeiro: Informações financeiras
        /estoque: Informações sobre seu estoque
        /lotes: Situação dos lotes
        /app: Atividades do aplicativo
        Clique em uma das opções
        """
        bot.send_message(
            message.chat.id,
            menu
        )

telebot.logger.setLevel(logging.DEBUG)

bot.infinity_polling()
