import sqlite3
from telegram import ReplyKeyboardMarkup, KeyboardButton
from texts_in_two_lang import words
from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
DATA_DB = os.environ.get('DATA_BASE')
superadmin = int(os.environ.get('ADMIN'))
# short texts
def main_menu(update, context):

    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        dedded = 12
        
    
    bot = context.bot
    bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'main menu'), reply_markup=ReplyKeyboardMarkup(keyboard=[[sl(update.message.chat.id, 'support')], [sl(update.message.chat.id, 'change_lang')], [sl(update.message.chat.id, 'select_district')]], resize_keyboard=True))
def main_menu_admin(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        dedded = 12
        
    
    bot = context.bot
    if update.message.chat.id == superadmin:
        bot.send_message(update.message.chat.id, 'Админ панель', reply_markup=ReplyKeyboardMarkup(keyboard=[['Добавить район'], ['Удалить район'], ['Админы', 'Абоненты']], resize_keyboard=True))
    else:
        bot.send_message(update.message.chat.id, 'Админ панель', reply_markup=ReplyKeyboardMarkup(keyboard=[['Добавить район', 'Удалить район'], ['Абоненты']], resize_keyboard=True))




### for database

def select(column, table, where):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    if column == 'fetchall':
        col = '*'
    else:
        col = column
    if where:
        c.execute("SELECT {} FROM {} WHERE {}".format(col, table, where))

        if column == 'fetchall':
            return c.fetchall()
        else:    
            return c.fetchone()
    else:
        c.execute("SELECT {} FROM {}".format(col, table))
        return c.fetchall()

def select_order_by(column, table, where, order_by):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute("SELECT {} FROM {} WHERE {} ORDER BY {} ".format(column, table, where, order_by))
    return c.fetchall()



def insert(table, values):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    values_str = ''
    for i in values[1::]:
        values_str += ", '{}'".format(i)
    c.execute("INSERT INTO {} VALUES ({}{}) ".format(table, str(values[0]), values_str))
    conn.commit()

    return 0


def change(table, setx, where):    # exapmle  for set > > name='xii' , for where id=11111
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()    
    c.execute("""UPDATE {} SET {} WHERE {} """.format(table, setx, where))
    conn.commit() 
 

def delete(table, where):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()   
    c.execute("DELETE FROM {} WHERE {} ".format(table, where))
    conn.commit()




# selecting a language
def sl(id, text):
    obj = select('*', 'bot_lang', 'user_id={}'.format(str(id)))
    lang = obj[1]
    if lang == 'UZB':
        n = 0
    elif lang == 'RUS':
        n = 1
    r_text = words[text][n]
    return r_text


def issuperadmin(id):
    
    if id == int(superadmin):
        return True
    else:
        return False

def sort_by_text(id):
    obj = select('*', 'sort', 'user_id={}'.format(str(id)))
    if obj[1] == 'asc':
        return [sl(id, 'to min'), 'sort_by_desc']
    if obj[1] == 'desc':
        return [sl(id, 'to max'), 'sort_by_asc']