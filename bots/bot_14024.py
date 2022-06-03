import telebot
from telebot import types
import logging
from datetime import datetime

API_KEY = '5398007849:AAFKndDeAWI6Zyo4oBBA0e2cnTsZuxog1b0'

bot = telebot.TeleBot(API_KEY)

logger = telebot.logger

@bot.message_handler(commands=["saldo"])
def get_saldo(message):
    data = datetime.today().strftime("%d/%m/%Y")
    msg = ''
    for conta in ['Itaú', 'C6 Bank']:
        msg += f'{data} - Conta: {conta}, saldo: R$ 1520,00\n'
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
    /initial: Volta para o menu inicial
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
    /initial: Volta para o menu inicial
    Clique em uma das opções
    """
    bot.reply_to(message, menu)


@bot.message_handler(commands=["lotes"])
def get_lotes_options(message):
    menu = """
    Sobre o que você quer saber sobre seus Lotes:
    /pesos: Peso dos Lotes
    /valor: Estimativa de valor na cotação de hoje
    /initial: Volta para o menu inicial
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
    /initial: Volta para o menu inicial
    """
    bot.reply_to(message, menu)


@bot.message_handler(commands=["initial"])
def get_initial_menu(message):
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

# autentcated = {1534403426: '5512982239764'}
'''
user_id = {'telegram_user_id': '1534403426',
            'phone_number' '5512982239764',
            'first_name': 'Fabiano',
            'farm_ids': '[14024, 407]'}
'''
autentcated = {}

@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    if not autentcated.get(message.contact.user_id):
        autentcated[message.contact.user_id] = message.contact.phone_number
    if autentcated.get(message.contact.user_id):
        get_initial_menu(message)


def autenticar(message):
    if message.contact and autentcated.get(message.from_user.id) is None:
        autentcated[message.contact.user_id] = message.contact.phone_number
        return True
    elif autentcated.get(message.from_user.id):
        return True
    else:
        return True


@bot.message_handler(func=autenticar)
def start(message):
    if autentcated.get(message.chat.id) is None:
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