import random
import telebot
import requests
from decouple import config

bot = telebot.TeleBot(config('telegram_key'))


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.reply_to(message, 'Estamos em  🚧')


@bot.message_handler(commands=['tempo'])
def wetaher(message):
    get_weather = requests.get(
        'http://wttr.in/Recife?format=j1', headers={'user-agen': 'curl'}
    )
    weather = get_weather.json()
    temperature = weather['current_condition'][0]['temp_C']
    weather_code = weather['current_condition'][0]['weatherCode']
    if weather_code == '176':
        weather_code = '🌧'
    elif weather_code == '227':
        weather_code = '⛄'
    elif weather_code == '116':
        weather_code = '⛅'
    else:
        weather_code = '🤔'
    bot.reply_to(
        message, f'A temperatura em Recife está '
                 f'{temperature} graus. {weather_code}'
    )


@bot.message_handler(commands=['cotacao'])
def cotation(message):
    get_cotation = requests.get(
        'https://economia.awesomeapi.com.br/json/all',
        headers={'user-agen': 'curl'}
    )
    cota = get_cotation.json()
    dolar = float(cota['USD']['high'])
    euro = float(cota['EUR']['high'])
    libra = float(cota['GBP']['high'])
    bot.reply_to(
        message, f'================================= \n '
                 f'O dólar está custando: R$ {dolar:.2f},\n '
                 f'O euro está custando: R$ {euro:.2f}, \n '
                 f'A libra está custando: R$ {libra:.2f}'
    )


@bot.message_handler(content_types=['text'])
def read_words(message):
    text = message.text.lower()
    print(f'[{message.from_user.first_name}]: {text}')
    chat_id = message.chat.id
    if 'acho' in text:
        bot.send_message(chat_id, 'Você acha ou tem certeza?')
    elif 'mas' in text:
        lines = open('general.txt').read().splitlines()
        oxebot_message = random.choice(lines)
        bot.send_message(chat_id, oxebot_message)
    elif 'yzakius' in text:
        lines = open('yzakius.txt').read().splitlines()
        oxebot_message = random.choice(lines)
        bot.send_message(chat_id, oxebot_message)
    elif 'hehe' in text:
        bot.send_message(chat_id, 'Putz. Olha só essa risada kkk')


bot.polling()

# while True:
#    pass
#    time.sleep(1)
