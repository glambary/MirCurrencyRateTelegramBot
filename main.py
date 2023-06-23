import os
import dotenv
import telebot

from telebot import types

from config import URL, DEPLOY
from currency_rate_handle import get_info, get_amount_of_money_to_buy

if DEPLOY:
    from background import keep_alive # for deploy
    TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
else:
    dotenv.load_dotenv(dotenv.find_dotenv())
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

buttons = {
    'info': 'Инфо',
    'number': 'Мне нужно ... белорусских рублей!',
    'link': ('Перейти на сайт. Если ты, конечно, сомневаешься во мне ☹️.', 'Перейти на сайт'),
}


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()

    markup.add(types.KeyboardButton(buttons['info']))
    markup.add(types.KeyboardButton(buttons['number']))
    markup.add(types.KeyboardButton(buttons['link'][0]))

    response_text = \
        f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b> 🤟!\n' \
        'Я - бот, для работы с курсом валют платёжной системы "Мир".'

    bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode='html',
        reply_markup=markup,
    )


@bot.message_handler(content_types=['text'])
def info(message):
    if message.text.lower() in ('привет', 'hi', 'hellow', 'здарова'):
        response_text = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>!'
        bot.reply_to(message, response_text, parse_mode='html')
    elif message.text == buttons['info']:
        response_text = get_info()
        bot.reply_to(message, response_text, parse_mode='html')
    elif message.text.startswith(buttons['link'][1]):
        bot.reply_to(message, URL, parse_mode='html')
    elif message.text == buttons['number']:
        bot.reply_to(message, 'Введите количество белорусских рублей, которое Вам необходимо.')
        bot.register_next_step_handler(message, on_number)


def on_number(message):
    try:
        n = float(message.text.strip())
    except (TypeError, ValueError):
        bot.reply_to(message, 'Вводимые данные должны быть числом. Попробуйте снова.')
        return
    bot.reply_to(
        message,
        f'Необходимое количество российских рублей {get_amount_of_money_to_buy(n):,.2f}'
    )


if DEPLOY:
    keep_alive()

bot.polling(none_stop=True)





# markup = types.ReplyKeyboardMarkup()

# markup.add(
#     types.KeyboardButton('Currency Rate', resize_keyboard=True)
# )
#


# @bot.message_handler(commands=['start'])
# def main(message):
#     rate = get_currency_rate_bel_rub()
#     bot.send_message(message.chat.id, rate)


# 'Держи ссылку на курс валют <a>https://mironline.ru/support/list/kursy_mir/?sphrase_id=99648</a>, '\
# 'если ты, конечно, сомневаешься во мне ☹️.'


# @bot.message_handler(commands=['rate'])
# def rate(message):
#     markup = types.InlineKeyboardMarkup()
#
#     markup.add(
#         types.InlineKeyboardButton(
#             'Инфо',
#             callback_data='info')
#     )
#
#     markup.add(
#         types.InlineKeyboardButton(
#             'Сколько нужно белорусских рублей?',
#             callback_data='number'
#         )
#     )
#
#     markup.add(
#         types.InlineKeyboardButton(
#             'Перейти на сайт. Если ты, конечно, сомневаешься во мне ☹️.',
#             url='https://mironline.ru/support/list/kursy_mir/?sphrase_id=99648'
#         )
#     )
#
#     bot.reply_to(message, 'Могу предложить:', reply_markup=markup)

    # btn1 = None
    # btn2 = None
    # markup.row(btn1, btn2)
    # btn4 = None
    # markup.row(btn4)
