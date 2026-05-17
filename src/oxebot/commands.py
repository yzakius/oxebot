import httpx
import random
import time
from utils import can_talk
from telegram import Update
from telegram.ext import ContextTypes


async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "*Comandos disponíveis no OxeBot:*\n\n"
        "*/start* ou */help* - Mostra esta mensagem de ajuda\n\n"
        "*/tempo* - Mostra a temperatura atual em Recife\n\n"
        "*/cotacao* - Mostra a cotação do dólar, euro e libra\n\n"
        "*/quote* - Exibe uma citação aleatória de sabedoria\n\n"
        "*/quote_add <texto>* - Adiciona uma nova citação\n\n"
        "*Respostas automáticas:*\n"
        'O bot também responde automaticamente quando detecta: "acho", "mas", "yzakius" ou "hehe"'
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cotation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_cotation = await httpx.AsyncClient().get(
        "https://economia.awesomeapi.com.br/json/all", headers={"user-agent": "curl"}
    )
    cota = get_cotation.json()
    dolar = float(cota["USD"]["high"])
    euro = float(cota["EUR"]["high"])
    libra = float(cota["GBP"]["high"])
    await update.message.reply_text(
        f"================================= \n "
        f"O dólar está custando: R$ {dolar:.2f},\n "
        f"O euro está custando: R$ {euro:.2f}, \n "
        f"A libra está custando: R$ {libra:.2f}"
    )


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = open("assets/text/quotes.txt").read().splitlines()
    oxebot_message = random.choice(lines)
    await update.message.reply_text(
        f"=========================== \n"
        f"Momento de Sabedoria no OXE: \n"
        f"=========================== \n\n"
        f"{oxebot_message}"
    )


async def read_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.lower()
    print(f"[{message.from_user.first_name}]: {text}")

    msg_time = message.date.timestamp()
    current_time = time.time()
    msg_tolerance_time = current_time - msg_time

    if msg_tolerance_time <= 3:
        palavras = {
            "acho": "assets/text/acho.txt",
            "mas": "assets/text/general.txt",
            "yzakius": "assets/text/yzakius.txt",
            "hehe": "assets/text/risada.txt",
        }
        for palavra, arquivo in palavras.items():
            if palavra in text and can_talk():
                lines = open(arquivo).read().splitlines()
                await message.reply_text(random.choice(lines))
                break


async def quote_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Leia o MANUAL!!!!!!")
        return

    text_replaced = " ".join(context.args)
    if len(text_replaced) > 10:
        with open("assets/text/quotes.txt", "a") as quote:
            quote.write(f"\n{text_replaced}")
        await update.message.reply_text("Arquivado com sucesso ;)")
    else:
        await update.message.reply_text("Leia o MANUAL!!!!!!")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://wttr.in/Recife?format=j1", headers={"User-Agent": "curl"}
        )

    if r.status_code == 200:
        r_json = r.json()
        current_condition = r_json.get("current_condition")
        if isinstance(current_condition, list) and len(current_condition):
            temperature = current_condition[0]["temp_C"]
            weather_code = current_condition[0]["weatherCode"]
            weather_icon = weather_symbol.get(
                wwo_code.get(weather_code), weather_symbol["Unknown"]
            )
            await update.message.reply_text(
                f"A temperatura em Recife está {temperature} graus. {weather_icon}"
            )
            return

    await update.message.reply_text("Erro ao buscar informações")
