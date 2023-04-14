from config import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from telegram.ext.filters import BaseFilter
from brain import ChatbotManager

chat_manager = ChatbotManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola!")

async def message_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    gpt_response = chat_manager.ask(message)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=gpt_response)


if __name__ == '__main__':
    print('Starting bot...')
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters=BaseFilter(), callback=message_callback)

    application.add_handler(message_handler)
    application.add_handler(start_handler)
    application.run_polling()