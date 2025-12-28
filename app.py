import os
import telebot
from telebot import types

# جلب التوكن من إعدادات Koyeb
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # إنشاء أزرار تفاعلية تحت الرسالة
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛒 عروض أمازون اليوم", url="https://www.amazon.com")
    btn2 = types.InlineKeyboardButton("🎁 خصومات Temu الحصرية", url="https://www.temu.com")
    btn3 = types.InlineKeyboardButton("📢 قناة التنبيهات", url="https://t.me/your_channel") # استبدليها برابط قناتك
    markup.add(btn1, btn2, btn3)
    
    welcome_msg = (
        "👋 أهلاً بك في 'روبوتي الذكي' للأسعار!\n\n"
        "✅ أرسل لي أي رابط منتج وسأقوم بمراقبته لك.\n"
        "✅ سأخبرك فور نزول السعر.\n"
        "✅ سأعطيك كوبونات خصم حصرية."
    )
    bot.reply_to(message, welcome_msg, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_links(message):
    text = message.text.lower()
    
    # الرد التلقائي عند إرسال رابط (هنا سنضع نظام الربح لاحقاً)
    if "amazon" in text or "temu" in text or "ebay" in text:
        bot.reply_to(message, "⚙️ جاري فحص الرابط واستخراج أفضل سعر لك... سأوافيك بالتحديث خلال لحظات!")
        # هنا سنضيف لاحقاً نظام "تحويل الرابط" ليكون برابط الإحالة الخاص بكِ
    else:
        bot.reply_to(message, "أرسل لي رابطاً من (Amazon, eBay, Temu) لأتمكن من مساعدتك في مراقبة السعر.")

bot.polling(none_stop=True)
