from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from conversationList import *
from functions import *
from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
DATA_DB = os.environ.get('DATA_BASE')
superadmin = int(os.environ.get('ADMIN'))


def admin_panel(update, context):
    bot=context.bot
    if update.message.text == 'Добавить район':
        districts = select('*', 'menu_districts', '')
        keyboards = [['Назад']]
        k = []
        for i in districts:
            if not i[1] in k:
                keyboards.append([i[1]])
                k.append(i[1])
        update.message.reply_text('Введите название района на двух языках:\n\nP.s Узбекский // русский', reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True))
        return SEND_DISTRICT
    elif update.message.text == 'Удалить район':
        update.message.reply_text('Вы уверены, удаление данных', reply_markup=ReplyKeyboardMarkup(keyboard=[['Да', 'Назад']], resize_keyboard=True))
        return DELETE_DISTRICT
    elif update.message.text == 'Админы' and update.message.chat.id == superadmin:

        if issuperadmin(update.message.chat.id):
            conn = sqlite3.connect(DATA_DB)
            c = conn.cursor()

            c.execute("SELECT * FROM admins ")
            admin_list = ''
            n = 1
            for i in c.fetchall():
                admin_list += str(n) + '.'
                for x in i:
                    
                    admin_list += '       ' + str(x)
                admin_list += '\n'
            
                n += 1
            if admin_list == '':
                admin_list = 'Админы нет'
                update.message.reply_text(admin_list, reply_markup=ReplyKeyboardMarkup(keyboard=[['добавить'], ['Назад']], resize_keyboard=True))
            else:
                update.message.reply_text(admin_list, reply_markup=ReplyKeyboardMarkup(keyboard=[['добавить', 'удалять'], ['Назад']], resize_keyboard=True))
            conn.commit()
            conn.close()
            return ADD_REMOVE_ADMIN
    elif update.message.text == 'Абоненты':
        date, time = str(update.message.date).split(' ')
        print(date)
        all_subscribes = len(select('*', 'users', ''))
        t_j = select('*', 'joined_today', "date='{}'".format(date))
        if t_j:
            today_joined = t_j[0]
        else:
            today_joined = 0
        update.message.reply_text('Все пользователи: {}👥\nЗарегистрировано сегодня: {}👤'.format(str(all_subscribes), str(today_joined)))

def add_remove_admin(update, context):
    text = update.message.text
    if text == 'добавить':
        update.message.reply_text('Отправьте переадресованное сообщение нового администратора', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return CREATE_ADMIN
    if text == 'удалять':
        update.message.reply_text('пожалуйста, введите ID администратора', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return DELETE_ADMIN
    elif text == 'Назад':
    
        if issuperadmin(update.message.chat.id):
            main_menu_admin(update, context)
        else:
            main_menu_admin(update, context)
        return ADMIN_PANEL



def create_admin(update, context):
    if update.message.forward_from == None:
        update.message.reply_text('этот пользователь отключил пересылку сообщений. Мы просим бота временно отключить эту функцию, чтобы стать администратором\nПосле исправления настроек отправьте новое переадресованное сообщение:')
        return CREATE_ADMIN
    
    else:
        
        obj = update.message.forward_from
        if not obj.username == None:
            username = '@'+obj.username
        else:
            username = ''
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("INSERT INTO admins VALUES ({}, '{}', '{}')".format(int(obj.id), obj.first_name, username))
        
        conn.commit()
        conn.close()
        main_menu_admin(update, context)
        return ADMIN_PANEL



def delete_admin(update, context):
    bot = context.bot
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM admins WHERE id={} ".format(int(update.message.text)))
        try:
            bot.send_message(int(update.message.text), 'Удалили вас из списка админов\n\nНажмите /start', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            
        except:
            deded = 0
        conn.commit()
        conn.close()
        main_menu_admin(update, context)
        return ADMIN_PANEL
    except:
        update.message.reply_text('Ошибка, напишите правильно')
        
        conn.commit()
        conn.close()
        return DELETE_ADMIN







def send_district(update, context):
    bot = context.bot
    text = update.message.text
    if text == 'Назад':
        main_menu_admin(update, context)
        return ADMIN_PANEL
    else:
           
        insert('menu_districts', [update.message.chat.id, text, '0', '0', 'xxx', 'AAA', 'xxx', '0'])
        update.message.reply_text('Отправьте локация', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SEND_LOCATION


def send_location(update, context):
    bot = context.bot
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    change('menu_districts', "latitude='{}'".format(latitude), "user_id={} and text='xxx'".format(str(update.message.chat.id)))
    change('menu_districts', "longitude='{}'".format(longitude), "user_id={} and text='xxx'".format(str(update.message.chat.id)))
    update.message.reply_text('Отправьте названия локации на двух языках:\n\nP.s Узбекский // русский')
    return SEND_LOCATION_TITLE


def send_location_title(update, context):
    bot = context.bot
    location = update.message.text
    change('menu_districts', "location='{}'".format(location), "user_id={} and text='xxx'".format(str(update.message.chat.id)))
    update.message.reply_text('Отправьте фотография')
    return SEND_PHOTO


def send_photo(update, context):
    bot = context.bot
    file_id = update.message.photo[0].file_id
    change('menu_districts', "photo='{}'".format(file_id), "user_id={} and text='xxx'".format(str(update.message.chat.id)))
    update.message.reply_text('Отправьте текст на двух языках:\n\nP.s Узбекский // русский')
    return SEND_TEXT

def send_text(update, context):
    text = update.message.text
    change('menu_districts', "text='{}'".format(text), "user_id={} and text='xxx'".format(str(update.message.chat.id)))
    update.message.reply_text('Отправьте цену')
    return SEND_PRICE
    

def send_price(update, context):
    text = str(update.message.text)
    change('menu_districts', "price='{}'".format(text), "user_id={} and price='0'".format(str(update.message.chat.id)))
    main_menu_admin(update, context)
    return ADMIN_PANEL
def delete_district(update, context):
    
    bot = context.bot
    try:
        a = update.callback_query.id
        update = update.callback_query
        is_callback = True
    except:
        is_callback = False
        if update.message.text == 'Назад':
            main_menu_admin(update, context)
            return ADMIN_PANEL

    obj = select('*', 'menu_districts', '')
    
    ds = [] # all distrits
    basket = []
    for i in obj:
        if not i[1] in basket:
            ds.append([InlineKeyboardButton(text=i[1], callback_data=i[1])])
            basket.append(i[1])
    ds.append([InlineKeyboardButton(text='Назад', callback_data='cancel_main_menu')])
    if is_callback:
        update.edit_message_text('Выберите район👇:', reply_markup=InlineKeyboardMarkup(ds))

    
    else:
        a = bot.send_message(update.message.chat.id, 'Выберите район👇:', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, a.message_id)
        bot.send_message(update.message.chat.id, 'Выберите район👇:', reply_markup=InlineKeyboardMarkup(ds))
        
    
    return SELECT_DEL_DISTRICT


def select_del_district(update, context):

    bot = context.bot
    c = update.callback_query
    
    if c.data == 'cancel_main_menu':
        
        bot.delete_message(c.message.chat.id, c.message.message_id)
        
        main_menu_admin(update, context)
        return ADMIN_PANEL

    else:
        obj = select('fetchall', 'menu_districts', "district='{}'".format(c.data))
        
        ls = [] # all locations
        for i in obj:
            
            if len(ls) <= 8:
                ls.append([InlineKeyboardButton(text=i[4], callback_data='ln_{}_{}'.format(c.data, i[4]))])
            else:
                ls.append([InlineKeyboardButton(text='1', callback_data='index'), InlineKeyboardButton(text='>>>', callback_data='{}_next_2'.format(c.data))])
                break
        ls.append([InlineKeyboardButton(text='Назад', callback_data='cancel_select_district')])
        c.edit_message_text('Выберите место', reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_DEL_LOCATION

def select_del_location(update, context):
    bot = context.bot
    c = update.callback_query
    if 'next_' in c.data:
        # repeat select district functoion, 
        data, ttt, n = c.data.split('_') # ttt is unneccessary n is page_n
        obj = select('fetchall', 'menu_districts', "district='{}'".format(data))
        ls = [] # all locations
        
        breaknvalues = (int(n) - 1) * 9
        
        for i in obj[breaknvalues:]:
            if len(ls) <= 8:
                ls.append([InlineKeyboardButton(text=i[4], callback_data='ln_{}_{}'.format(data, i[4]))])
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
        ls.append([InlineKeyboardButton(text='Назад', callback_data='cancel_select_district')])
        c.edit_message_text('Выберите место', reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_DEL_LOCATION
    elif 'previous_' in c.data:
        # repeat select district functoion, 
        data, ttt, n = c.data.split('_') # ttt is unneccessary n is page_n
        obj = select('fetchall', 'menu_districts', "district='{}'".format(data))
        ls = [] # all locations
        
        breaknvalues = (int(n) - 1) * 9
        
        for i in obj[breaknvalues:]:
            if len(ls) <= 8:
                ls.append([InlineKeyboardButton(text=i[4], callback_data='ln_{}_{}'.format(data, i[4]))])
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
                ls.append([InlineKeyboardButton(text='<<<', callback_data='{}_previous_{}'.format(data, nn)), InlineKeyboardButton(text=n, callback_data='index')])
        ls.append([InlineKeyboardButton(text='Назад', callback_data='cancel_select_district')])
        c.edit_message_text('Выберите место', reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_DEL_LOCATION


    elif c.data == 'main menu':
        bot.delete_message(c.message.chat.id, c.message.message_id)
        main_menu_admin(update, context)
        return ADMIN_PANEL
    elif c.data == 'cancel_select_district':
        delete_district(update, context)
        return SELECT_DEL_DISTRICT
    elif c.data == 'index':
        qwqwqwqwnqw = 0  # do nothing
    else:
        id = c.message.chat.id
        tx, ds, ln = c.data.split('_')  # tx is us neccassary its only text 'ln'   ds is district ln is location
        obj = select('*', 'menu_districts', "district='{}' and location='{}'".format(ds, ln))
        try:
            delete('menu_districts', "district='{}' and location='{}'".format(ds, ln))
        except:
            wdswdwdw = 0
        c.edit_message_text('Успешно удалено')
        main_menu_admin(update, context)
        return ADMIN_PANEL




def cancel(update, context):
    bot = context.bot
    c = update.callback_query 
    if update.callback_query.data == 'next':
        c.edit_message_text('Нажмите /start для перезапустить бот')
        return ConversationHandler.END