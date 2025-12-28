import os
import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def get_amazon_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5"
    }
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        # محاولة البحث عن رمز السعر في أمازون
        price = soup.find("span", {"class": "a-offscreen"}).get_text()
        return price
    except Exception as e:
        return None

@bot.message_handler(func=lambda message: "amazon" in message.text.lower())
def handle_amazon(message):
    bot.reply_to(message, "⏳ لحظة واحدة.. أتفحص السعر الآن في أمازون...")
    price = get_amazon_price(message.text)
    if price:
        bot.reply_to(message, f"💰 السعر الحالي لهذا المنتج هو: {price}")
    else:
        bot.reply_to(message, "❌ عذراً، لم أستطع سحب السعر. تأكد أن الرابط صحيح أو حاول لاحقاً.")

bot.polling(none_stop=True)
