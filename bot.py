from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from conversationList import *
from functions import *
from dotenv import load_dotenv
import os
from texts_in_two_lang import words
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
ADMIN = os.environ.get('ADMIN')

def start(update, context):
    
    all_admins = select('*', 'admins', '')
    all_admins_ids = []
    for i in all_admins:
        all_admins_ids.append(i[0])
    if update.message.chat.id == int(ADMIN) or update.message.chat.id in all_admins_ids:
        main_menu_admin(update, context)
        return ADMIN_PANEL  
    else:
        bot = context.bot
        is_registred = select('*', 'users', 'id={}'.format(str(update.message.chat.id)))
        print(is_registred)
        if is_registred != None:
            main_menu(update, context)
        else:
            bot.send_message(update.message.chat.id, words['select_lang'][0], reply_markup=ReplyKeyboardMarkup(keyboard=[['🇺🇿UZB'], ['🇷🇺RUS']], resize_keyboard=True))
            return SET_LANG

def menu_support(update, context):
    
    bot = context.bot
    
    bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'wait'), reply_markup=ReplyKeyboardMarkup(keyboard=[[sl(update.message.chat.id, 'cancel')]], resize_keyboard=True))
    i = select('*', 'users', 'id={}'.format(str(update.message.chat.id)))

    text = i[1] + '\n' + i[2]
    c_data = 'admin_answer_'+str(i[0])
    i_answer = InlineKeyboardButton(text='Ответить', callback_data=c_data)
    
    
    mrk = InlineKeyboardMarkup([[i_answer]])
    bot.send_message(int(ADMIN), text, reply_markup=mrk)
    admins = select('fetchall', 'admins', '')
    for x in admins:
        try:
            bot.send_message(x[0], text, reply_markup=mrk)
        except:
            swswswsw = 0
    obj = select('*', 'waitlist', 'user_id={}'.format(str(update.message.chat.id)))
    if not obj:
        user = select('*', 'users', 'id={}'.format(str(update.message.chat.id)))
        insert('waitlist', [update.message.chat.id, user[1], user[2]])
    return SUPPORT


def change_bot_lang(update, context):
    bot = context.bot
    update.message.reply_text(sl(update.message.chat.id, 'click_lang'), reply_markup=ReplyKeyboardMarkup(keyboard=[['🇺🇿UZB'], ['🇷🇺RUS'], [sl(update.message.chat.id, 'back')]], resize_keyboard=True))
    return CHANGING_BOT_LANG

def changing_bot_lang(update, context):
    bot = context.bot
    text = update.message.text
    if text == sl(update.message.chat.id, 'back'):
        main_menu(update, context)
        
    else:
        change('bot_lang', "lang='{}'".format(text[-3:]), 'user_id={}'.format(str(update.message.chat.id)))
        main_menu(update, context)
    return ConversationHandler.END

def district(update, context):
    bot = context.bot
    try:
        a = update.callback_query.id
        update = update.callback_query
        is_callback = True
    except:
        is_callback = False

    obj = select('*', 'menu_districts', '')
    
    ds = [] # all distrits
    basket = []
    for i in obj:
        if not i[1] in basket:
            try:
                uzb, rus = i[1].split('//')
                lang_obj = select('*', 'bot_lang', 'user_id={}'.format(str(update.message.chat.id)))
                lang = lang_obj[1]
                if lang == 'UZB':
                    txt = uzb
                elif lang == 'RUS':
                    txt = rus
            except:
                txt = i[1]
            ds.append([InlineKeyboardButton(text=txt, callback_data=i[1])])
            basket.append(i[1])
    ds.append([InlineKeyboardButton(text=sl(update.message.chat.id, 'back'), callback_data='cancel_main_menu')])
    if is_callback:
        update.edit_message_text(sl(update.message.chat.id, 'click_district'), reply_markup=InlineKeyboardMarkup(ds))
        for i in range(1, 4):
            try:
                bot.delete_message(update.message.chat.id, update.message.message_id+i)
            except:
                edededede = 0
    
    else:
        a = bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'click_district'), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, a.message_id)
        bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'click_district'), reply_markup=InlineKeyboardMarkup(ds))
        
    
    return SELECT_DISTRICT
    
def select_district(update, context):

    bot = context.bot
    c = update.callback_query
    
    if c.data == 'cancel_main_menu':
        
        bot.delete_message(c.message.chat.id, c.message.message_id)
        main_menu(update, context)
        return ConversationHandler.END

    else:
        obj = select('*', 'sort', 'user_id={}'.format(str(c.message.chat.id)))
        if obj:
            sort_by = obj[1]
        else:
            insert('sort', [c.message.chat.id, 'asc'])
            sort_by = 'asc'
        obj = select_order_by('*', 'menu_districts', "district='{}'".format(c.data), "price {}".format(sort_by))
        
        ls = [] # all locations
        for i in obj:
            try:
                uzb, rus = i[4].split('//')
                lang_obj = select('*', 'bot_lang', 'user_id={}'.format(str(c.message.chat.id)))
                lang = lang_obj[1]
                if lang == 'UZB':
                    txt = uzb
                elif lang == 'RUS':
                    txt = rus

            except:
                txt = i[4]
            if len(ls) <= 8:
                ls.append([InlineKeyboardButton(text=txt, callback_data='ln_{}_{}'.format(c.data, i[4]))])
            else:
                ls.append([InlineKeyboardButton(text='1', callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_2'.format(c.data))])
                break
        sort_obj = sort_by_text(c.message.chat.id)
        ls.append([InlineKeyboardButton(text=sort_obj[0], callback_data= c.data +'_'+sort_obj[1])])
        ls.append([InlineKeyboardButton(text=sl(c.message.chat.id, 'back'), callback_data='cancel_select_district')])
        c.edit_message_text(sl(c.message.chat.id, 'select_location'), reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_LOCATION

def select_location(update, context):
    bot = context.bot
    c = update.callback_query
    if 'sort_by_' in c.data:
        data,s,b,value = str(c.data).split('_')
        change('sort', "by='{}'".format(value), 'user_id={}'.format(str(c.message.chat.id)))
        update.callback_query.data = data
        select_district(update, context)
        return SELECT_LOCATION
    if 'next_' in c.data:
        # repeat select district functoion, 
        data, ttt, n = c.data.split('_') # ttt is unneccessary n is page_n
        s = select('*', 'sort', "user_id={}".format(str(c.message.chat.id)))
        sort_by = s[1]
        obj = select_order_by('*', 'menu_districts', "district='{}'".format(data), "price {}".format(sort_by))
        ls = [] # all locations
        
        breaknvalues = (int(n) - 1) * 9
        
        for i in obj[breaknvalues:]:
            if len(ls) <= 8:
                try:
                    uzb, rus = i[4].split('//')
                    lang_obj = select('*', 'bot_lang', 'user_id={}'.format(str(c.message.chat.id)))
                    lang = lang_obj[1]
                    if lang == 'UZB':
                        txt = uzb
                    elif lang == 'RUS':
                        txt = rus
                except:
                    txt = i[4]

                ls.append([InlineKeyboardButton(text=txt, callback_data='ln_{}_{}'.format(data, i[4]))])
            else:
                nn = str(int(n)+1)
                pn = str(int(n)-1)
                if pn == '0':
                    ls.append([InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_{}'.format(data, nn))])
                else:
                    ls.append([InlineKeyboardButton(text='<<<', callback_data='{}_previous_{}'.format(data, pn)), InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_{}'.format(data, nn))])

                break
        else:
            pn = str(int(n)-1)
            if pn != '0':
                ls.append([InlineKeyboardButton(text='<<<', callback_data='{}_previous_{}'.format(data, pn)), InlineKeyboardButton(text=n, callback_data='index')])
        ls.append([InlineKeyboardButton(text=sl(c.message.chat.id, 'back'), callback_data='cancel_select_district')])
        c.edit_message_text(sl(c.message.chat.id, 'select_location'), reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_LOCATION
    elif 'previous_' in c.data:
        # repeat select district functoion, 
        data, ttt, n = c.data.split('_') # ttt is unneccessary n is page_n
        s = select('*', 'sort', "user_id={}".format(str(c.message.chat.id)))
        sort_by = s[1]
        obj = select_order_by('*', 'menu_districts', "district='{}'".format(data), "price {}".format(sort_by))
        ls = [] # all locations
        
        breaknvalues = (int(n) - 1) * 9
        
        for i in obj[breaknvalues:]:
            if len(ls) <= 8:
                try:
                    uzb, rus = i[4].split('//')
                    lang_obj = select('*', 'bot_lang', 'user_id={}'.format(str(c.message.chat.id)))
                    lang = lang_obj[1]
                    if lang == 'UZB':
                        txt = uzb
                    elif lang == 'RUS':
                        txt = rus
                except:
                    txt = i[4]

                ls.append([InlineKeyboardButton(text=txt, callback_data='ln_{}_{}'.format(data, i[4]))])
            else:
                nn = str(int(n)+1)
                pn = str(int(n)-1)
                if pn == '0':
                    ls.append([InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_{}'.format(data, nn))])
                    sort_obj = sort_by_text(c.message.chat.id)
                    ls.append([InlineKeyboardButton(text=sort_obj[0], callback_data= data +'_'+sort_obj[1])])
                else:
                    ls.append([InlineKeyboardButton(text='<<<', callback_data='{}_previous_{}'.format(data, pn)), InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_{}'.format(data, nn))])

                break
        else:
            pn = str(int(n)-1)
            if pn != '0':
                ls.append([InlineKeyboardButton(text='<<<', callback_data='{}_previous_{}'.format(data, nn)), InlineKeyboardButton(text=n, callback_data='index')])
        ls.append([InlineKeyboardButton(text=sl(c.message.chat.id, 'back'), callback_data='cancel_select_district')])
        c.edit_message_text(sl(c.message.chat.id, 'select_location'), reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_LOCATION


    elif c.data == 'main menu':
        bot.delete_message(c.message.chat.id, c.message.message_id)
        main_menu(update, context)
        return ConversationHandler.END
    elif c.data == 'cancel_select_district':
        district(update, context)
        return SELECT_DISTRICT
    elif c.data == 'index':
        qwqwqwqwnqw = 0  # do nothing
    else:
        id = c.message.chat.id
        tx, ds, ln = c.data.split('_')  # tx is us neccassary its only text 'ln'   ds is district ln is location
        obj = select('*', 'menu_districts', "district='{}' and location='{}'".format(ds, ln))
        del_mess = select('*', 'del_message', 'user_id={}'.format(str(c.message.chat.id)))
        if del_mess:
            for i in range(4):
                try:
                    bot.delete_message(c.message.chat.id, int(del_mess[1])+i)
                except:
                    dededed = 0
            delete('del_message', 'user_id={}'.format(str(c.message.chat.id)))
        try:
            a = bot.send_location(id, float(obj[2]), float(obj[3]))
            
            insert('del_message', [c.message.chat.id, str(a.message_id)])
            bot.send_photo(id, obj[5])
            i_main_menu = InlineKeyboardButton(text=sl(c.message.chat.id, 'main menu'), callback_data='main menu')
            try:
                uzb, rus = obj[6].split('//')
                lang_obj = select('*', 'bot_lang', 'user_id={}'.format(str(c.message.chat.id)))
                lang = lang_obj[1]
                if lang == 'UZB':
                    txt = uzb
                elif lang == 'RUS':
                    txt = rus
            except:
                txt = obj[6]                
            bot.send_message(id, txt)
            bot.send_message(id, sl(c.message.chat.id, 'price')+obj[7], reply_markup=InlineKeyboardMarkup([[i_main_menu]]))
        except:
            dedhiedh = 0
        




