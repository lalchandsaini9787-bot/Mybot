import os
from flask import Flask
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_flask).start()

# Render ke Environment Variable se lega, safe rahega
TOKEN = os.environ.get("TOKEN")
CHANNEL1 = "@darkmrinmoy03"
CHANNEL2 = "@darkmrinmoy04"  # @ lagana zaruri hai
YOUR_FILE_LINK = "https://www.mediafire.com/file/9detslhonjp275h/FOX+ONE+V7.apk/file"

bot = telebot.TeleBot(TOKEN)

def join_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel 1 Join Karo", url=f"https://t.me/{CHANNEL1.replace('@','')}"))
    markup.add(InlineKeyboardButton("📢 Channel 2 Join Karo", url=f"https://t.me/{CHANNEL2.replace('@','')}"))
    markup.add(InlineKeyboardButton("✅ I Have Joined", callback_data="check"))
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Channel join karo 👇", reply_markup=join_markup())

@bot.callback_query_handler(func=lambda c: c.data=="check")
def check(c):
    try:
        s1 = bot.get_chat_member(CHANNEL1, c.from_user.id).status
        s2 = bot.get_chat_member(CHANNEL2, c.from_user.id).status
        if s1 in ['member','administrator','creator'] and s2 in ['member','administrator','creator']:
            # Yaha galti thi, ab theek hai
            bot.send_message(c.message.chat.id, f"✅ Thanks for Joining!\n\nFile Here:\n{YOUR_FILE_LINK}")
        else:
            bot.answer_callback_query(c.id, "❌ Channel join karo", show_alert=True)
    except Exception as e:
        print(e)
        bot.answer_callback_query(c.id, "Bot ko dono channel me Admin banao!", show_alert=True)

bot.infinity_polling(skip_pending=True)
