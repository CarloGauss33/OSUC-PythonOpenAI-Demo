from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola!")

# una funcion catch_all que reciba el update y el context
# y que se encargue de llamar a la funcion que corresponda
# y que retorne el mensaje al usuario



if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()