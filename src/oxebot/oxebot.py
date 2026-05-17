from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands import send_help, quote, read_words, quote_add, weather, cotation
from decouple import config


app = ApplicationBuilder().token(config("telegram_key")).build()

app.add_handler(CommandHandler(["start", "help"], send_help))
app.add_handler(CommandHandler("cotacao", cotation))
app.add_handler(CommandHandler("quote", quote))
app.add_handler(CommandHandler("quote_add", quote_add))
app.add_handler(CommandHandler("tempo", weather))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, read_words))

if __name__ == "__main__":
    print("Bot rodando...")
    app.run_polling()
