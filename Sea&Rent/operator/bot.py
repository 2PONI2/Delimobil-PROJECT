import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

bot_token = 'YOUR_BOT_TOKEN'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот оператор, чем могу помочь?")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()