##  chat with admin and user
from dotenv import load_dotenv
import os
from functions import *
from conversationList import *
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
ADMIN = os.environ.get('ADMIN')


def callback_query(update, context):
    bot = context.bot
    c = update.callback_query
    
        
    if c.data[:12] == 'admin_answer':
        w = select('*', 'waitlist', 'user_id={}'.format(c.data[13:]))
        if w:
            obj = select('*', 'talk', "admin_id='{}'".format(str(c.message.chat.id)))
            if not obj:
                insert('talk', [int(c.data[13:]), str(c.message.chat.id), '1'])
                delete('waitlist', 'user_id={}'.format(c.data[13:]))
                bot.delete_message(c.message.chat.id, c.message.message_id)
                bot.send_message(c.message.chat.id, 'бот связан с пользователем', reply_markup=ReplyKeyboardMarkup(keyboard=[['Закончить диалог']], resize_keyboard=True))
                bot.send_message(int(c.data[13:]), sl(int(c.data[13:]), 'bot_connected_with_admin'), reply_markup=ReplyKeyboardMarkup(keyboard=[[sl(int(c.data[13:]), 'end_chat')]], resize_keyboard=True))
            else:
                c.edit_message_text('Сначала закончите текущий чат')
        else:
            c.edit_message_text('Пользовател отметил чат')
    

def chat(update, context):
    bot = context.bot
    istyping = select('*', 'istype', 'user_id={}'.format(str(update.message.chat.id)))
    
    if not istyping:
        insert('istype', [update.message.chat.id, 'False'])

    if select('*', 'talk', "user_id={}".format(str(update.message.chat.id))):
        obj = select('*', 'talk', "user_id={}".format(str(update.message.chat.id)))
        if update.message.text == sl(update.message.chat.id, 'end_chat'):
            try:

                bot.send_message(int(obj[0]), sl(int(obj[0]), 'chat_stopped'), reply_markup=ReplyKeyboardMarkup(keyboard=[[sl(int(obj[0]), 'main menu')]], resize_keyboard=True))
                
                
                bot.send_message(obj[1], 'Чат окончен', reply_markup=ReplyKeyboardMarkup(keyboard=[['Главное админ панель']], resize_keyboard=True))

                delete('talk', "user_id={}".format(str(update.message.chat.id)))
            except:
                lopa = 0
        elif update.message.chat.id == int(ADMIN):
        
            #i_break = KeyboardButton(text='Закончить диалог')
            #mrk = ReplyKeyboardMarkup([[i_break]], resize_keyboard=True)
            #
            bot.send_message(int(obj[0]), update.message.text)
        elif update.message.chat.id == int(obj[0]):
            bot.send_message(int(obj[1]), update.message.text)
    if update.message.text == sl(update.message.chat.id, 'main menu'):
        main_menu(update, context)
        return ConversationHandler.END
    elif update.message.text == sl(update.message.chat.id, 'cancel'):
        main_menu(update, context)
        delete('waitlist', 'user_id={}'.format(str(update.message.chat.id)))
        return ConversationHandler.END
def chat_admin(update, context):
    bot = context.bot
    
    if select('*', 'talk', "admin_id='{}'".format(str(update.message.chat.id))):
        obj = select('*', 'talk', "admin_id='{}'".format(str(update.message.chat.id)))
        if update.message.text == 'Закончить диалог':
            try:

                bot.send_message(int(obj[0]), sl(int(obj[0]), 'chat_stopped'), reply_markup=ReplyKeyboardMarkup(keyboard=[[sl(int(obj[0]), 'main menu')]], resize_keyboard=True))
                
                
                bot.send_message(update.message.chat.id, 'Чат окончен', reply_markup=ReplyKeyboardMarkup(keyboard=[['Главное админ панель']], resize_keyboard=True))

                delete('talk', "admin_id='{}'".format(str(update.message.chat.id)))
            except:
                lopa = 0
        else:
            
            bot.send_message(int(obj[0]), update.message.text)
    elif update.message.text == 'Главное админ панель':
        main_menu_admin(update, context)
        return ADMIN_PANEL
         
