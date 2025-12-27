import os
import telebot
from flask import Flask

# جلب التوكن من إعدادات Koyeb
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@server.route("/")
def webhook():
    return "البوت يعمل!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أنا بوتك وقد بدأت العمل بنجاح.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "استلمت رسالتك: " + message.text)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
