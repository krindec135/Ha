import telebot
import os
from telebot import types
import sqlite3
import requests
import json
import datetime
import random

BOT_TOKEN = '1256263220:AAEyZ-QafCuZgvsXNlTlh58TjyWXULaNhcU'
QIWI_KEY = 'caf600b52e5e51ed7edcc357f89569a2'
ADMIN_ID = 1047585454

token = str(os.environ.get('BOT_TOKEN'))
bot = telebot.TeleBot(token)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item1 = types.KeyboardButton("📄Ответы")
item2 = types.KeyboardButton("📊Статистика")
item3 = types.KeyboardButton("🔑Советы")
item4 = types.KeyboardButton("📖Демо КИМы")
item5 = types.KeyboardButton("👤Личный кабинет")

markup.add(item1, item2, item3, item4, item5)

"""for i in range():
    conn = sqlite3.connect('id.db')
    c = conn.cursor()
    c.execute('SELECT ID FROM users')
    count_users = (c.fetchall())
    conn.commit()
    conn.close()
    print(count_users[0][0])
    print(count_users)
    print(len(count_users))
    for i in range(len(count_users)):
        #count_users[i][0]
        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute('UPDATE users SET GAMES =:bal WHERE ID =:id', {"id":count_users[i][0] , "bal": random.randint('')})
        conn.commit()
        conn.close()"""


@bot.message_handler(commands=['start'])
# conn = sqlite3.connect('id.db')
# c = conn.cursor()
# c.execute(("""INSERT INTO 'users' (ID, BALANCE, GAMES)
#                    VALUES ('%s', '%s', '%s');
#                    """) % (id, 0, 0))
# conn.commit()
# conn.close()

def start_message(message):
    print(message.chat.id)
    try:

        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute('SELECT ID FROM users WHERE ID =:id', {"id": message.chat.id})
        print(c.fetchone()[0])
        conn.commit()
        conn.close()
        bot.send_sticker(message.chat.id,
                         data='CAACAgIAAxkBAAIBfV4u6eJtknusBUZzXAABwlHOuDfaMQAC5AkAAnlc4glXpUfFRMgfKxgE')
        bot.send_message(message.chat.id,
                         '*Рады снова вас увидеть*',
                         parse_mode='Markdown', reply_markup=markup)
    except TypeError:
        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute(("""INSERT INTO 'users' (ID, BALANCE, GAMES) 
                            VALUES ('%s', '%s', '%s');
                            """) % (message.chat.id, 0, 0))
        conn.commit()
        conn.close()
        bot.send_sticker(message.chat.id,
                         data='CAACAgIAAxkBAAIBfV4u6eJtknusBUZzXAABwlHOuDfaMQAC5AkAAnlc4glXpUfFRMgfKxgE')
        bot.send_message(message.chat.id, '*Добро пожаловать в бота*\nКоторый поможет вам успешно сдать\n*ЕГЭ и ОГЭ*',
                         parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(content_types=['sticker'])
def get_docs(message):
    bot.send_message(message.chat.id, '*OK*',
                     parse_mode='Markdown', reply_markup=markup)
    print(message)


@bot.message_handler(content_types=['text'])
def ohh(message):
    payment_key = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton(text='Проверить платёж', callback_data='check')
    pay = types.InlineKeyboardButton(text='Купить ответы', callback_data='pay', url=payment(message.chat.id))
    payment_key.add(pay, check)
    if message.text == '📊Статистика':
        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute('SELECT ID FROM users')
        count_users = (len(c.fetchall()))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, f'📱*Количество людей в боте*:\n{count_users} успешно сдадут ОГЭ/ЕГЭ✅',
                         parse_mode='Markdown', reply_markup=markup)
    elif message.text == '📖Демо КИМы':
        keyboard1 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="ЕГЭ", callback_data="EGE")
        button2 = types.InlineKeyboardButton(text="ОГЭ", callback_data="OGE")
        keyboard1.add(button1)
        keyboard1.add(button2)
        bot.send_message(message.chat.id, ("📚 *ВЫБЕРИ ЭКЗАМЕН*"),
                         reply_markup=keyboard1, parse_mode='Markdown')
    elif message.text == '🔑Советы':
        bot.send_message(message.chat.id, 'https://telegra.ph/Kak-uspeshno-sdat-EGEHOGEH-sovety-ehkspertov-01-30')
    elif message.text == '📄Ответы':
        bot.send_message(message.chat.id, '''После покупки , за две недели до экзаменов 
вы будете добавлены в *специальный Telegram  канал*, 
где вы найдете *ответы* на все необходимые вам экзамены

На канале будут выкладываться ответы на *ОГЭ и ЕГЭ*

*Ответы* будут выкладываться за два дня, до каждого экзамена!''', parse_mode='Markdown', reply_markup=payment_key)
    elif message.text == '👤Личный кабинет':
        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute('SELECT BALANCE FROM users WHERE ID =:id', {"id": message.chat.id})
        che = c.fetchone()
        conn.commit()
        conn.close()
        if che[0] == 1:
            bot.send_message(message.chat.id, '*СТАТУС ПОКУПКИ ОТВЕТОВ*:\n_Куплено_', parse_mode='Markdown')
        elif che[0] == 0:
            bot.send_message(message.chat.id, '*СТАТУС ПОКУПКИ ОТВЕТОВ*:\n_Не куплено_', parse_mode='Markdown')
    elif str(message.text).startswith('/send') and message.chat.id == ADMIN_ID:
        conn = sqlite3.connect('id.db')
        c = conn.cursor()
        c.execute('SELECT ID FROM users')
        count_users = (c.fetchall())
        conn.commit()
        conn.close()
        print(count_users[0][0])
        print(count_users)
        print(len(count_users))
        for i in range(len(count_users)):
            bot.send_message(count_users[i][0], str(message.text).replace('/send', ''))


def payment(id):
    x = str(datetime.datetime.now()).replace(' ', 'T')
    find_point = x.find('.')
    order_time = (x[:find_point] + "+" + '00:25')
    print(order_time)
    rnd = random.randint(1, 100000)

    url = f'https://api.qiwi.com/partner/bill/v1/bills/{id}'
    payload = {"amount":
        {
            "currency": "RUB",
            "value": '1.00'
        },
        "expirationDateTime": order_time
    }
    data = json.dumps(payload)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {QIWI_KEY}'
    }
    headers_1 = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {QIWI_KEY}'
    }
    r = requests.put(url, headers=headers, data=data)
    r = json.loads(r.text)
    d = requests.get((f'https://api.qiwi.com/partner/bill/v1/bills/{id}'), headers=headers_1)
    d = json.loads(d.text)
    if d['status']['value'] == 'EXPIRED':
        """print('ok')
        headers_2 = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {QIWI_KEY}'
        }
        requests.post((f'https://api.qiwi.com/partner/bill/v1/bills/{id}/reject'),
                      headers=headers_2)"""
        r_1 = requests.put(url, headers=headers, data=data)
        r_1 = json.loads(r_1.text)
        return r_1['payUrl']
    else:
        return r['payUrl']


def check_payment(message, id):
    headers_1 = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {QIWI_KEY}'
    }
    d = requests.get((f'https://api.qiwi.com/partner/bill/v1/bills/{id}'), headers=headers_1)
    d = json.loads(d.text)
    if d['status']['value'] == 'WAITING':
        bot.send_message(message.chat.id, 'Счет пока не оплачен')
    else:
        conn = sqlite3.connect('vk-bot.db')
        c = conn.cursor()
        c.execute('UPDATE users SET BALANCE =:bal WHERE ID =:id', {"id": message.chat.id, "bal": 1})
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, 'Покупка ответов прошла успешно')


def predmet(message, mes):
    keyboard_EGE = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="география", callback_data="geo_kim")
    button2 = types.InlineKeyboardButton(text="литература", callback_data="leo_kim")
    button3 = types.InlineKeyboardButton(text="русский язык", callback_data="rus_kim")
    button4 = types.InlineKeyboardButton(text="мат.база", callback_data="matb_kim")
    button5 = types.InlineKeyboardButton(text="мат.проф", callback_data="matp_kim")
    button6 = types.InlineKeyboardButton(text="английский", callback_data="ang_kim")
    button7 = types.InlineKeyboardButton(text="французский", callback_data="fr_kim")
    button8 = types.InlineKeyboardButton(text="немецкий", callback_data="dt_kim")
    button9 = types.InlineKeyboardButton(text="испанский", callback_data="sp_kim")
    button10 = types.InlineKeyboardButton(text="китайский", callback_data="ch_kim")
    button11 = types.InlineKeyboardButton(text="биология", callback_data="bio_kim")
    button12 = types.InlineKeyboardButton(text="физика", callback_data="phy_kim")
    button13 = types.InlineKeyboardButton(text="обществознание", callback_data="soc_kim")
    button14 = types.InlineKeyboardButton(text="информатика", callback_data="inf_kim")
    button15 = types.InlineKeyboardButton(text="история", callback_data="hist_kim")
    button16 = types.InlineKeyboardButton(text="химия", callback_data="chem_kim")
    keyboard_EGE.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10,
                     button11,
                     button12, button13, button14, button15, button16)
    bot.send_message(message.chat.id, mes, reply_markup=keyboard_EGE)


def predmet_oge(message, mesa):
    keyboard_OGE = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="русский", callback_data="ru_kim")
    button2 = types.InlineKeyboardButton(text="математика", callback_data="mat_kim")
    button3 = types.InlineKeyboardButton(text="биология", callback_data="bi_kim")
    button4 = types.InlineKeyboardButton(text="обществознание", callback_data="obs_kim")
    button5 = types.InlineKeyboardButton(text="физика", callback_data="fiz_kim")
    button6 = types.InlineKeyboardButton(text="информатика", callback_data="prg_kim")
    button7 = types.InlineKeyboardButton(text="химия", callback_data="him_kim")
    button8 = types.InlineKeyboardButton(text="география", callback_data="gg_kim")
    button9 = types.InlineKeyboardButton(text="английский язык", callback_data="an_kim")
    button10 = types.InlineKeyboardButton(text="история", callback_data="ist_kim")
    button11 = types.InlineKeyboardButton(text="литература", callback_data="lit_kim")
    button12 = types.InlineKeyboardButton(text="испанский язык", callback_data="isp_kim")
    button13 = types.InlineKeyboardButton(text="французский язык", callback_data="fra_kim")
    button14 = types.InlineKeyboardButton(text="немецкий язык", callback_data="nem_kim")
    keyboard_OGE.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10,
                     button11,
                     button12, button13, button14)
    bot.send_message(message.chat.id, mesa, reply_markup=keyboard_OGE)


def oplata(message, mes):
    payment_key = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton(text='Проверить платёж', callback_data='check')
    pay = types.InlineKeyboardButton(text='Купить ответы', callback_data='pay')
    payment_key.add(pay, check)


def download(message, url):
    download_keyboard = types.InlineKeyboardMarkup()
    bt_download = types.InlineKeyboardButton(text='📥-СКАЧАТЬ-📥', url=url)
    download_keyboard.add(bt_download)
    bot.send_message(message.chat.id, 'ССЫЛКА НА СКАЧИВАНИЕ', reply_markup=download_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message = call.message
    if call.message:
        if call.data == 'EGE':
            predmet(call.message, '🔖Выбери предмет')
        elif call.data == 'geo_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1578583442/gg_ege_2020.zip')
        elif call.data == 'leo_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485845/li_ege_2020.zip')
        elif call.data == 'rus_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485569/ru_ege_2020.zip')
        elif call.data == 'matb_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573547346/ma_ege_2020.zip')
        elif call.data == 'matp_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573547346/ma_ege_2020.zip')
        elif call.data == 'ang_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1579160880/aya_ege_2020.zip')
        elif call.data == 'fr_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1579794284/fya_ege_2020.zip')
        elif call.data == 'dt_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1579160914/nya_ege_2020.zip')
        elif call.data == 'sp_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1579160951/iya_ege_2020.zip')
        elif call.data == 'ch_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1580229163/kya_ege_2020.zip')
        elif call.data == 'bio_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485735/bi_ege_2020.zip')
        elif call.data == 'phy_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485652/fi_ege_2020.zip')
        elif call.data == 'soc_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573821333/ob_ege_2020.zip')
        elif call.data == 'inf_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485712/inf_ege_2020.zip')
        elif call.data == 'hist_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573485764/is_ege_2020.zip')
        elif call.data == 'chem_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1574437234/hi_ege_2020.zip')
        elif call.data == 'OGE':
            predmet_oge(call.message, '🔖Выбери предмет')
        elif call.data == 'ru_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573571419/ru_oge_2020.zip')
        elif call.data == 'mat_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573564676/ma_oge_2020.zip')
        elif call.data == 'bi_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573564407/bi_oge_2020.zip')
        elif call.data == 'obs_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1574080073/ob_oge_2020.zip')
        elif call.data == 'fiz_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573571339/fi_oge_2020.zip')
        elif call.data == 'prg_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1577460770/inf_oge_2020.zip')
        elif call.data == 'him_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1577111379/hi_oge_2020.zip')
        elif call.data == 'gg_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1577446156/gg_oge_2020.zip')
        elif call.data == 'an_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1580223157/aya_oge_2020.zip')
        elif call.data == 'ist_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573571476/is_oge_2020.zip')
        elif call.data == 'lit_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1573553976/li_oge_2020.zip')
        elif call.data == 'isp_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1580223210/iya_oge_2020.zip')
        elif call.data == 'fra_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1580223195/fya_oge_2020.zip')
        elif call.data == 'nem_kim':
            download(call.message, 'http://www.fipi.ru/sites/default/files/document/1580223181/nya_oge_2020.zip')
        elif call.data == 'check':
            headers_1 = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {QIWI_KEY}'
            }
            d = requests.get((f'https://api.qiwi.com/partner/bill/v1/bills/{message.chat.id}'), headers=headers_1)
            d = json.loads(d.text)
            if d['status']['value'] == 'WAITING':
                bot.send_message(message.chat.id, 'Счет пока не оплачен 😔\nПопробуй проверить платеж чуть позже')
            elif d['status']['value'] == 'PAID':
                print()
                conn = sqlite3.connect('id.db')
                c = conn.cursor()
                c.execute('UPDATE users SET BALANCE =:bal WHERE ID =:id', {"id": message.chat.id, "bal": 1})
                conn.commit()
                conn.close()
                bot.send_message(message.chat.id, '*Покупка ответов прошла успешно*!', parse_mode='Markdown')
            elif d['status']['value'] == 'EXPIRED':
                print('ok')
                headers_2 = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {QIWI_KEY}'
                }
                requests.post((f'https://api.qiwi.com/partner/bill/v1/bills/{message.chat.id}/reject'),
                              headers=headers_2)
                bot.send_message(message.chat.id, 'Счет пока не оплачен 😔\nПопробуй проверить платеж чуть позже')


while True:
    bot.polling(none_stop=True)
