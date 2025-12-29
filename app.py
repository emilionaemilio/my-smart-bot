import os
import telebot
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرف الإحالة الخاص بكِ
MY_TRACKING_ID = "20353003-20"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛒 عروض أمازون اليومية", url=f"https://www.amazon.com/gp/goldbox?tag={MY_TRACKING_ID}")
    btn2 = types.InlineKeyboardButton("📢 قناة التخفيضات", url="https://t.me/your_channel") # استبدلي برابط قناتك لاحقاً
    markup.add(btn1, btn2)
    
    bot.reply_to(message, 
                 "👋 أهلاً بكِ في بوت التسوق الذكي!\n\n"
                 "🎯 وظيفتي: تحويل أي رابط منتج ترسله إلى رابط خصم مباشر.\n"
                 "📉 قريباً: سأقوم بتنبيهك عند انخفاض سعر أي منتج ترسله.", 
                 reply_markup=markup)

@bot.message_handler(func=lambda message: "amazon" in message.text.lower() or "amzn" in message.text.lower())
def convert_link(message):
    original_url = message.text
    # تنظيف الرابط وإضافة كود الربح الخاص بكِ
    clean_url = original_url.split("?")[0] # مسح أي أكواد قديمة في الرابط
    affiliate_url = f"{clean_url}?tag={MY_TRACKING_ID}"
    
    markup = types.InlineKeyboardMarkup()
    buy_btn = types.InlineKeyboardButton("🛍️ عرض المنتج والشراء الآن", url=affiliate_url)
    markup.add(buy_btn)
    
    response = (
        "✅ تم تجهيز رابط الإحالة الخاص بكِ!\n\n"
        "💡 نصيحة: عند الدخول من هذا الرابط، ستحصل على أفضل سعر متاح حالياً."
    )
    bot.reply_to(message, response, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def default_reply(message):
    bot.reply_to(message, "من فضلك أرسل رابط منتج من أمازون لتحويله لرابط خصم.")

bot.polling(none_stop=True)
