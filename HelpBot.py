
import telebot
import random
from telebot import types
import sqlite3
OnWork = True
notes = {}
helpers = {}
needys = {}
status = 0
token = '5984112909:AAF4yH3zH0vJaIMWsSY8PNZQlLzFZxaMp3s'
bot = telebot.TeleBot(token)

'''
c.execute("""CREATE TABLE articles(
        id text
        problem text
        status integer
    )""")
'''


@bot.message_handler(commands=['start','help'])
def start_message(message):
    db = sqlite3.connect('usersdata.db')
    c = db.cursor()
    user_id = message.chat.id
    bot.send_message(user_id,"Привет,Это система помощников в школе.")
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Я могу помочь", callback_data="icanhelp")
    button2 = types.InlineKeyboardButton(text="Мне нужна помощь", callback_data="ineedhelp")
    keyboard.add(button1)
    keyboard.add(button2)
    note = message.from_user.id
    if note not in c.execute("SELECT id FROM articles"):
        c.execute(f"INSERT INTO articles VALUES('{note},'-',0')")
    else:
        pass
    bot.send_message(message.chat.id, "Выберите опцию!", reply_markup=keyboard)
    db.commit()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "icanhelp":
            icanhelp(call.message.chat.id)
        if call.data == "ineedhelp":
            ineedhelp(call.message.chat.id)
def ineedhelp(user_id):
    bot.send_message(user_id, "Опишите вашу проблему:")
    @bot.message_handler(content_types='text')
    def update(message):
        db = sqlite3.connect('usersdata.db')
        c = db.cursor()
        user_id = message.chat.id
        tgid = message.from_user.id
        execl1 = f'{tgid}'
        execl2 = f'{message.text}'
        print(f"INSERT INTO articles VALUES ('{execl1},{execl2},1')")
        c.execute(f"INSERT INTO articles VALUES ('{execl1},{execl2},1')")
        bot.send_message(user_id,"Мы получили ваш запрос!")
        bot.send_message(user_id,"Список ваших заявок: " )
        bot.send_message(user_id,c.execute(f"SELECT * FROM articles WHERE id={execl1} ")[1])
        aftermenu(user_id)
        db.commit()
        return
def icanhelp(user_id):
    db = sqlite3.connect('usersdata.db')
    c = db.cursor()
    bot.send_message(user_id,"Список нуждающихся:")
    endlist = []
    cnt = 0
    for ids in c.execute("SELECT id FROM articles"):
        endlist.append(f"tg://user?id={ids}")
    for problems in c.execute("SELECT problem FROM articles"):
        stroke = "<a href='{0}'> {1} </a>".format(endlist[cnt],problems)
        bot.send_message(user_id,text=stroke,parse_mode='HTML')
        cnt+1
    db.commit()
    return
def aftermenu(user_id):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="✅ Мне помогли", callback_data="deleteapply2")
    button2 = types.InlineKeyboardButton(text="❌ Отмена", callback_data="deleteapply0")
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(user_id, "Статус задания?", reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    db = sqlite3.connect('usersdata.db')
    c = db.cursor()
    if call.message:
        if call.data == "deleteapply2":
            c.execute(f"INSERT INTO articles VALUES({call.from_user.id},'{call.message}',2)")
        if call.data == "deleteapply0":
            c.execute(f"INSERT INTO articles VALUES({call.from_user.id},'{call.message}',0)")
    db.commit()
bot.polling(none_stop=True)





bot.infinity_polling()
