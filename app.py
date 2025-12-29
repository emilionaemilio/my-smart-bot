import os
import telebot
from telebot import types

# إعدادات البوت الأساسية
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# إعداداتك الخاصة (تم وضع رقمك ومعرفك بنجاح)
MY_TRACKING_ID = "20353003-20" 
ADMIN_ID = 6836639902  
users_file = "users.txt" 

# وظيفة لحفظ المستخدمين الجدد في القائمة
def save_user(user_id):
    if not os.path.exists(users_file):
        with open(users_file, "w") as f: f.write("")
    with open(users_file, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(users_file, "a") as f:
            f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id) # تسجيل المستخدم لإرسال إعلانات له لاحقاً
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛒 عروض أمازون اليومية", url=f"https://www.amazon.com/gp/goldbox?tag={MY_TRACKING_ID}")
    markup.add(btn1)
    
    bot.reply_to(message, 
                 "👋 أهلاً بكِ في بوت التسوق الذكي!\n\n"
                 "🎯 أرسل لي أي رابط من أمازون وسأحوله لك لرابط خصم مباشر.", 
                 reply_markup=markup)

# --- لوحة تحكم الإذاعة (لكِ أنتِ فقط) ---
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "📢 أهلاً يا مديرة.. أكتبي الآن الرسالة التي تريدين إرسالها لكل المشتركين:")
        bot.register_next_step_handler(msg, send_to_all)
    else:
        bot.reply_to(message, "❌ عذراً، هذا الأمر مخصص لصاحبة البوت فقط.")

def send_to_all(message):
    if not os.path.exists(users_file):
        bot.send_message(ADMIN_ID, "❌ لا يوجد مستخدمين مسجلين بعد.")
        return

    with open(users_file, "r") as f:
        users = f.read().splitlines()
    
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
            continue
    bot.send_message(ADMIN_ID, f"✅ تم إرسال رسالتكِ بنجاح لـ {count} مشترك!")

# --- وظيفة تحويل الروابط (التي نجحت في التجربة) ---
@bot.message_handler(func=lambda message: "amazon" in message.text.lower() or "amzn" in message.text.lower())
def convert_link(message):
    clean_url = message.text.split("?")[0]
    affiliate_url = f"{clean_url}?tag={MY_TRACKING_ID}"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛍️ عرض المنتج والشراء الآن", url=affiliate_url))
    
    bot.reply_to(message, "✅ تم تجهيز رابط الإحالة الربحي الخاص بكِ!", reply_markup=markup)

bot.polling(none_stop=True)
