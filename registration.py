from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from conversationList import *
from functions import *


def set_lang(update, context):
    bot = context.bot
    lang = update.message.text[-3:]  #  user choice one language
    insert('bot_lang', [update.message.chat.id, lang])
    mrk = ReplyKeyboardRemove(remove_keyboard=True)
    bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'send_name'), reply_markup=mrk)
    return SEND_NAME


def send_name(update, context):
    bot = context.bot
    name = update.message.text   # users name that sent
    insert('users', [update.message.chat.id, name, '+998', '00.00.0000'])
    i_contact = KeyboardButton(text=sl(update.message.chat.id, 'button_send_phone_number'), request_contact=True)
    bot.send_message(update.message.chat.id, sl(update.message.chat.id, 'send_phone_number'), reply_markup=ReplyKeyboardMarkup([[i_contact]], resize_keyboard=True))

    return SEND_NUMBER


def phone_number(update, context):
    bot = context.bot
    if update.message.contact == None or not update.message.contact:
        phone_number = update.message.text  # users phone number which is sent   /// when user dont press button "send contact"
    else:
        phone_number = update.message.contact.phone_number   ## // when press the button
    
    change('users', "phone_number='{}'".format(phone_number), "id={}".format(str(update.message.chat.id)))
    #bot.send_message(update.message.chat.id, 'Отправьте дату рождения в формате дд.мм.гггг')
    main_menu(update, context)
    j_t = select('*', 'joined_today', '')
    date, time = str(update.message.date).split(' ')
    print(date)
    if j_t:
        if date == j_t[0][1]:
            change('joined_today', 'how_much={}'.format(str(j_t[0][0]+1)), "date='{}'".format(date))
            print('changed1')
        else:
            change('joined_today', "how_much=1", "date='{}'".format(j_t[0][1]))
            change('joined_today', "date='{}'".format(date), "date='{}'".format(j_t[0][1]))
            print('changed2')
    else:
        insert('joined_today', [1, date])
    return ConversationHandler.END #SEND_DATE_BIRTHDAY


def date_birthday(update, context):
    bot = context.bot
    date = update.message.text  # users date birth which is sent
    try:
        d, m , y = date.split('.')
        if (len(d) == 2 or len(d) == 1) and (len(m) == 2 or len(m) == 1) and len(y) == 4:
            change('users', "date_birthday='{}'".format(date), "id={}".format(str(update.message.chat.id)))
            main_menu(update, context)

            return ConversationHandler.END
        else:
            bot.send_message(update.message.chat.id, 'Неправилно!\nОтправьте дату рождения в формате дд.мм.гггг')
            return SEND_DATE_BIRTHDAY
    except:
        bot.send_message(update.message.chat.id, 'Неправилно!\nОтправьте дату рождения в формате дд.мм.гггг')
        return SEND_DATE_BIRTHDAY
