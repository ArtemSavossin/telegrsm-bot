
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import re
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)
import keyboards
import constants

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ENTERING, STATS, CHOOSING, SUBSCRIBES, TYPING_REPLY, TYPING_CHOICE = range(6)

markup = ReplyKeyboardMarkup(keyboards.main_keyboard, one_time_keyboard=True)

def login(update: Update, context: CallbackContext) -> int:
    reply_text = "Привет! Я - твой робот-помощник в работе с брокерами. Что хочешь сделать?"

    update.message.reply_text(reply_text, reply_markup=markup)

    return ENTERING

def start(update: Update, context: CallbackContext) -> int:
    reply_text = "Привет! Я - твой робот-помощник в работе с брокерами. Что хочешь сделать?"

    update.message.reply_text(reply_text, reply_markup=markup)

    return ENTERING

def balance_handler(update: Update, context: CallbackContext) -> int:

    balance = 10000 ## some logic on taking balances

    update.message.reply_text('Баланс на твоем счете' f"{balance}$", reply_markup=markup)

    return ENTERING

def help(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Тут я тебе расскажу про свои функции, но потом =)', reply_markup=markup)

    return ENTERING

def pick_model(update: Update, context: CallbackContext) -> int:
    context.user_choice = update.message.text

    models = ['m1', 'm2', 'm3'] # some logic on taking info on working models

    model_markup = keyboards.keyboard_from_arr(models)
    
    update.message.reply_text('Выбери модель, с которой хочешь работать', reply_markup=ReplyKeyboardMarkup(model_markup, one_time_keyboard=True))
    print(update.message.text.upper() == constants.CHECK_STATS)
    print(update.message.text.upper(), constants.CHECK_STATS)
    return update.message.text.upper()

def stats_handler(update: Update, context: CallbackContext) -> int:
    if re.match('^(За День|За неделю|За месяц|В целом)$', update.message.text):
        ans = 'some logic behind that ' + update.message.text
        update.message.reply_text(ans, reply_markup=markup)
        return ENTERING
    else:
        update.message.reply_text('Выбери за какой период хочешь получить статистику', reply_markup=ReplyKeyboardMarkup(keyboards.stats_keyboard, one_time_keyboard=True))

    return constants.CHECK_STATS

def shut_down_handler(update: Update, context: CallbackContext) -> int:
    ans = 'some logic behind shuting down this model: ' + update.message.text

    update.message.reply_text(ans, reply_markup=markup)
    return ENTERING

def notifications_handler(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == 'ON' or text == 'OFF':
        variants = ['m1 subscr', 'm2 subscr', 'model fucks up subs'] # some logic behind that

        update.message.reply_text('You can turn this notifications' f'${text}', reply_markup=ReplyKeyboardMarkup(keyboards.keyboard_from_arr(variants), one_time_keyboard=True))
        return SUBSCRIBES
    elif text == 'Notifications':
        variants = ['ON', 'OFF', '/help']
        update.message.reply_text('Выбери, включить или выключить уведомления', reply_markup=ReplyKeyboardMarkup(keyboards.keyboard_from_arr(variants), one_time_keyborad=True))
        return SUBSCRIBES
    else:
        update.message.reply_text('Выполнил действие', reply_markup=markup)
        return ENTERING

def done(update: Update) -> int:
    update.message.reply_text(
        "Bye!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

def main() -> None:
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater("token", persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', login)],
        states={
            ENTERING: [
                MessageHandler(
                    Filters.regex('^(Check stats)$'), pick_model
                ),
                MessageHandler(
                    Filters.regex('^(Check balance)$'), balance_handler
                ),
                MessageHandler(
                    Filters.regex('^(Notifications)$'), notifications_handler
                ),
                MessageHandler(
                    Filters.regex('^(Shutdown)$'), pick_model
                ),
                CommandHandler('help', help),
                MessageHandler(Filters.regex('^m.*$'), login),
            ],
            SUBSCRIBES: [
                CommandHandler('help', help),
                MessageHandler(Filters.regex('^O.|m.|N.*$'), notifications_handler),
            ],
            constants.SHUTDOWN : [
                MessageHandler(Filters.regex('^m.*$'), shut_down_handler),
            ],
            constants.CHECK_STATS : [
                MessageHandler(
                    Filters.regex('^(За День|За неделю|За месяц|В целом)$'), stats_handler
                ),
                MessageHandler(Filters.regex('^m.*$'), stats_handler),
            ],
            constants.NOTIFICATIONS : [
                MessageHandler(
                    Filters.regex('^(Daily|Weekly|Monthly|Overall)$'), notifications_handler
                ),
                MessageHandler(Filters.regex('^m.*$'), notifications_handler),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="my_conversation",
        persistent=True,
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
