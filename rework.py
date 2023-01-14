import telebot
import random
from telebot import types
import config
import sqlite3

rand_num = random.randint(1, 50)
notes = {}
bot = telebot.TeleBot("5653414504:AAE7F-LtYygMgaagUA_J18r5oKO5-y3uPfk")

db = sqlite3.connect('spravka.db')
c = db.cursor()
'''
c.execute("""CREATE TABLE articles(
        predmet text,
        theme text,
        url text
        )""")
'''
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("📚 Справочный материал",callback_data='spravka')
    markup.add(button1)
    bot.send_message(user_id,'выберите опцию',reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'spravka':
        spravka(call.message)
@bot.message_handler(content_types=['text'])
def spravka(message):
    user_id = message.chat.id
    bot.send_message(user_id, "По какому предмету?")
    Predmet = message.text
    db = sqlite3.connect("spravka.db")
    c = db.cursor()
    c.execute(f"INSERT INTO predmet VALUES ({Predmet})")
@bot.message_handler(content_types=['text'])
def theme(message):
    user_id = message.chat.id
    bot.send_message(user_id, "По какой теме?")
    Theme = message.text
    db = sqlite3.connect("spravka.db")
    c = db.cursor()
    c.execute(f"INSERT INTO theme VALUES ({Theme})")
bot.polling()