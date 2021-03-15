import random
import telepot
import time
import requests
# import json
 
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print(f'Comando recebido: {command}')
    if "exemplo1" in command:
        lines = open('general.txt').read().splitlines()
        mensagem = random.choice(lines)
        bot.sendMessage(chat_id, mensagem)
    elif "exemplo2" in command:
        bot.sendMessage(chat_id, "Você escreveu exemplo2")
    elif command == "/tempo":
        get_weather = requests.get(
            "http://wttr.in/Recife?format=j1", headers={"user-agen": "curl"}
            )
        weather = get_weather.json()
        temperature = weather['current_condition'][0]['temp_C']
        weather_code = weather['current_condition'][0]['weatherCode']
        if weather_code == "176":
            weather_code = "🌧"
        bot.sendMessage(
            chat_id, f"A temperatura em Recife está {temperature} graus. {weather_code}"
            )

bot = telepot.Bot(config("telegram_key"))
bot.message_loop(handle)
print('Ahhhhhhhhhhhhh!!!')
while True:
    pass
    time.sleep(1)
