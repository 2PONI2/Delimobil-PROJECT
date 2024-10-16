import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram.ext import CallbackContext
import sqlite3

# Включение журналирования
logging.basicConfig(level=logging.INFO)

# Токен для бота
TOKEN = '8171076234:AAGbqGifwyKeBD3ugMN62PLVY2pgQkjfFoM'

# ID оператора поддержки
OPERATOR_CHAT_ID = 6422350149

# ID последнего пользователя
LAST_USER_CHAT_ID = 1019243445

# Функция для получения вопросов из базы данных
def get_faq_questions():
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM faq")
    questions = cursor.fetchall()
    conn.close()
    return questions

# Функция для получения ответа на вопрос по его ID
def get_faq_answer(question_id):
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM faq WHERE id = ?", (question_id,))
    answer = cursor.fetchone()
    conn.close()
    return answer[0] if answer else "Ответ не найден."

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Помощь человека", callback_data='human_help'),
         InlineKeyboardButton("FAQ", callback_data='faq')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Добро пожаловать в бот поддержки!', reply_markup=reply_markup)
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'human_help':
        await human_help(update, context)
    elif query.data == 'faq':
        await faq(update, context)
    elif query.data.startswith('faq_'):
        question_id = int(query.data.split('_')[1])
        answer = get_faq_answer(question_id)
        await query.message.reply_text(answer)

async def human_help(update: Update, context: CallbackContext):
    global LAST_USER_CHAT_ID
    LAST_USER_CHAT_ID = update.effective_chat.id
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Вы запросили помощь человека. Пожалуйста, опишите вашу проблему.")

async def faq(update: Update, context: CallbackContext):
    questions = get_faq_questions()
    if not questions:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="К сожалению, FAQ пока пуст.")
        return

    keyboard = [[InlineKeyboardButton(q[1], callback_data=f'faq_{q[0]}')] for q in questions]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Что вас интересует? Выберите вопрос из списка:",
                                   reply_markup=reply_markup)

async def message_handler(update: Update, context: CallbackContext):
    user_message = update.message.text
    if user_message == 'Помощь человека':
        await human_help(update, context)
    elif user_message == 'FAQ':
        await faq(update, context)
    else:
        await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=f'Пользователь {update.effective_user.username} написал: {user_message}')
        global LAST_USER_CHAT_ID
        LAST_USER_CHAT_ID = update.effective_chat.id

async def operator_reply_handler(update: Update, context: CallbackContext):
    if LAST_USER_CHAT_ID:
        operator_message = update.message.text
        await context.bot.send_message(chat_id=LAST_USER_CHAT_ID, text=f'Оператор написал: {operator_message}')

async def operator_reply_command(update: Update, context: CallbackContext):
    if update.effective_chat.id == OPERATOR_CHAT_ID:
        reply_message = update.message.text.split(' ', 1)[1]
        await context.bot.send_message(chat_id=LAST_USER_CHAT_ID, text=f'Оператор написал: {reply_message}')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(OPERATOR_CHAT_ID), operator_reply_handler))
    application.add_handler(CommandHandler('reply', operator_reply_command))

    application.run_polling()

if __name__ == '__main__':
    main()