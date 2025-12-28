import os
import telebot
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛒 عروض أمازون", url="https://www.amazon.com")
    btn2 = types.InlineKeyboardButton("🎁 خصومات Temu", url="https://www.temu.com")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, "أهلاً بك! أنا جاهز لجلب الأسعار لك.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "أرسل لي رابط المنتج وسأفحصه لك.")

bot.polling(none_stop=True)
