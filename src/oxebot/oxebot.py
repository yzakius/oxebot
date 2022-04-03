import random
import telebot
import requests
import time
from decouple import config

bot = telebot.TeleBot(config('telegram_key'))


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.reply_to(message, 'Estamos em  🚧')


@bot.message_handler(commands=['tempo'])
def weather(message):
    wwo_code = {
        "113": "Sunny",
        "116": "PartlyCloudy",
        "119": "Cloudy",
        "122": "VeryCloudy",
        "143": "Fog",
        "176": "LightShowers",
        "179": "LightSleetShowers",
        "182": "LightSleet",
        "185": "LightSleet",
        "200": "ThunderyShowers",
        "227": "LightSnow",
        "230": "HeavySnow",
        "248": "Fog",
        "260": "Fog",
        "263": "LightShowers",
        "266": "LightRain",
        "281": "LightSleet",
        "284": "LightSleet",
        "293": "LightRain",
        "296": "LightRain",
        "299": "HeavyShowers",
        "302": "HeavyRain",
        "305": "HeavyShowers",
        "308": "HeavyRain",
        "311": "LightSleet",
        "314": "LightSleet",
        "317": "LightSleet",
        "320": "LightSnow",
        "323": "LightSnowShowers",
        "326": "LightSnowShowers",
        "329": "HeavySnow",
        "332": "HeavySnow",
        "335": "HeavySnowShowers",
        "338": "HeavySnow",
        "350": "LightSleet",
        "353": "LightShowers",
        "356": "HeavyShowers",
        "359": "HeavyRain",
        "362": "LightSleetShowers",
        "365": "LightSleetShowers",
        "368": "LightSnowShowers",
        "371": "HeavySnowShowers",
        "374": "LightSleetShowers",
        "377": "LightSleet",
        "386": "ThunderyShowers",
        "389": "ThunderyHeavyRain",
        "392": "ThunderySnowShowers",
        "395": "HeavySnowShowers",
    }
    weather_symbol = {
        "Unknown": "✨",
        "Cloudy": "☁️",
        "Fog": "🌫",
        "HeavyRain": "🌧",
        "HeavyShowers": "🌧",
        "HeavySnow": "❄️",
        "HeavySnowShowers": "❄️",
        "LightRain": "🌦",
        "LightShowers": "🌦",
        "LightSleet": "🌧",
        "LightSleetShowers": "🌧",
        "LightSnow": "🌨",
        "LightSnowShowers": "🌨",
        "PartlyCloudy": "⛅️",
        "Sunny": "☀️",
        "ThunderyHeavyRain": "🌩",
        "ThunderyShowers": "⛈",
        "ThunderySnowShowers": "⛈",
        "VeryCloudy": "☁️",
    }

    r = requests.get(
        'https://wttr.in/Recife?format=j1', headers={'User-Agent': 'curl'}
    )

    if r.status_code == 200:
        r_json = r.json()
        current_condition = r_json.get('current_condition')

        if isinstance(current_condition, list) and len(current_condition):
            temperature = current_condition[0]['temp_C']
            weather_code = current_condition[0]['weatherCode']

            weather_icon = weather_symbol.get(
                wwo_code.get(weather_code),
                weather_symbol['Unknown']
            )

            bot.reply_to(
                message, 'A temperatura em Recife está '
                         f'{temperature} graus. {weather_icon}'
            )

            return

    bot.reply_to(message, 'Erro ao buscar informações')


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


@bot.message_handler(commands=['quote_add'])
def quote_add(message):
    text = message.text
    chat_id = message.chat.id
    if len(text) > 10:
        text_replaced = text.replace('/quote_add ', '')
        quote = open('assets/text/quotes.txt', 'a')
        quote.write(f'\n{text_replaced}')
        quote.close()
        bot.send_message(chat_id, 'Arquivado com sucesso ;)')
    else:
        bot.send_message(chat_id, 'Leia o MANUAL!!!!!!')


@bot.message_handler(commands=['quote'])
def quote(message):
    chat_id = message.chat.id
    lines = open('assets/text/quotes.txt').read().splitlines()
    oxebot_message = random.choice(lines)
    bot.send_message(
        chat_id,
        f'=========================== \n'
        f'Momento de Sabedoria no OXE: \n'
        f'=========================== \n\n'
        f'{oxebot_message}'
    )


@bot.message_handler(content_types=['text'])
def read_words(message):
    text = message.text.lower()
    print(f'[{message.from_user.first_name}]: {text}')
    msg_time = message.date
    current_time = int(time.time())
    msg_tolerance_time = current_time - msg_time
    if msg_tolerance_time <= 3:
        chat_id = message.chat.id
        if 'acho' in text:
            lines = open('assets/text/acho.txt').read().splitlines()
            oxebot_message = random.choice(lines)
            bot.send_message(chat_id, oxebot_message)
        elif "mas" in text:
            lines = open('assets/text/general.txt').read().splitlines()
            oxebot_message = random.choice(lines)
            bot.send_message(chat_id, oxebot_message)
        elif 'yzakius' in text:
            lines = open('assets/text/yzakius.txt').read().splitlines()
            oxebot_message = random.choice(lines)
            bot.send_message(chat_id, oxebot_message)
        elif 'hehe' in text:
            lines = open('assets/text/risada.txt').read().splitlines()
            oxebot_message = random.choice(lines)
            bot.send_message(chat_id, oxebot_message)


bot.polling()
