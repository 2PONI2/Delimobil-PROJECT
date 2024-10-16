#import config
import telebot
from telebot import types
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib3 

# ID оператора
operator_chat_id = 6422350149
user_chat_id = None  # Здесь будет храниться ID последнего пользователя

# Функция для команды /start
def start(update, context):
    reply_text = "Здравствуйте! Я бот поддержки. Чтобы связаться с оператором, напишите /support."
    update.message.reply_text(reply_text)

# Функция для команды /support
def support(update, context):
    reply_text = "Свяжитесь с оператором. Как я могу Вам помочь?"
    update.message.reply_text(reply_text)

# Функция для общения с оператором
#def message_handler(update, context):
#    user_message = update.message.text
#    operator_chat_id = 6422350149
#
#    context.bot.send_message(operator_chat_id, user_message)


# Функция для общения с оператором
def message_handler(update, context):
    user_message = update.message.text
    global user_chat_id
    user_chat_id = update.message.chat_id  # Сохраняем ID пользователя

    context.bot.send_message(operator_chat_id, user_message)

# Функция для обработки ответов оператора
def operator_reply_handler(update, context):
    if user_chat_id:
        operator_message = update.message.text
        context.bot.send_message(user_chat_id, operator_message)



# Обработчики команд
updater = Updater("8171076234:AAGbqGifwyKeBD3ugMN62PLVY2pgQkjfFoM", use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

support_handler = CommandHandler('support', support)
dispatcher.add_handler(support_handler)

message_handler = MessageHandler(Filters.text & ~Filters.command, message_handler)
dispatcher.add_handler(message_handler)

# Обработчик сообщений от оператора
operator_reply_handler = MessageHandler(Filters.text & ~Filters.command, operator_reply_handler)
dispatcher.add_handler(operator_reply_handler)

# Запускаем бота
updater.start_polling()
updater.idle()




