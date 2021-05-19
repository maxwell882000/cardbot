from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from conversationList import *
from bot import *
from registration import *
from support import *
from admin import *
from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')



updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher


start = ConversationHandler(
    entry_points = [CommandHandler('start', start), MessageHandler(Filters.text(['Главное админ панель']), start)],
    states = {
        SEND_NAME: [MessageHandler(Filters.text, send_name)],
        SEND_NUMBER: [MessageHandler(Filters.all, phone_number)],   # for writing phone number , registr
        SEND_DATE_BIRTHDAY: [MessageHandler(Filters.text, date_birthday)],
        SET_LANG: [MessageHandler(Filters.text(['🇺🇿UZB', '🇷🇺RUS']), set_lang)],
        # for admins
        
        ADMIN_PANEL: [MessageHandler(Filters.text(['Добавить район', 'Удалить район', 'Админы', 'Абоненты']), admin_panel)],
        SEND_DISTRICT: [MessageHandler(Filters.text, send_district)],
        SEND_LOCATION: [MessageHandler(Filters.location, send_location)],
        SEND_LOCATION_TITLE: [MessageHandler(Filters.text, send_location_title)],
        SEND_PHOTO: [MessageHandler(Filters.photo, send_photo)],
        SEND_TEXT: [MessageHandler(Filters.text, send_text)],
        SEND_PRICE: [MessageHandler(Filters.text, send_price)],
        DELETE_DISTRICT: [MessageHandler(Filters.text(['Да', 'Назад']), delete_district)],
        SELECT_DEL_DISTRICT: [CallbackQueryHandler(select_del_district)],
        SELECT_DEL_LOCATION: [CallbackQueryHandler(select_del_location)],

        ADD_REMOVE_ADMIN: [MessageHandler(Filters.text, add_remove_admin)],
        CREATE_ADMIN: [MessageHandler(Filters.forwarded, create_admin)],
        DELETE_ADMIN: [MessageHandler(Filters.text, delete_admin)]

    },
    fallbacks = [CommandHandler('start', start)]
)


support_chat = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(words['support']), menu_support)],
    states = {
        SUPPORT: [MessageHandler(Filters.text, chat)]
    },
    fallbacks = []
)



change_lang = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(words['change_lang']), change_bot_lang)],
    states = {
        CHANGING_BOT_LANG: [MessageHandler(Filters.text(['🇺🇿UZB', '🇷🇺RUS', 'Назад', 'Ortga']), changing_bot_lang)]
    },
    fallbacks = []#[MessageHandler(Filters.text(['next']), ready_to_start_chat)]
)


menu_districts = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(words['select_district']), district)],
    states = {
        SELECT_DISTRICT: [CallbackQueryHandler(select_district)],
        SELECT_LOCATION: [CallbackQueryHandler(select_location)]
    },
    fallbacks=[]
)


dp.add_handler(start)
dp.add_handler(support_chat)
dp.add_handler(menu_districts)
dp.add_handler(change_lang)
dp.add_handler(CallbackQueryHandler(callback_query))
dp.add_handler(MessageHandler(Filters.text, chat_admin))


updater.start_webhook(listen='127.0.0.1',
                      port=10090,
                      url_path=TOKEN)
    

updater.bot.set_webhook('https://cardbot.elite-house.uz/{}'.format(TOKEN))