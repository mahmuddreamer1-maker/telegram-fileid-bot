import os
from threading import Thread
from flask import Flask
import telebot

# 1. Render እንዲያልፈን የምትረዳ ትንሽ የ Flask ድረ-ገጽ ማታለያ
app = Flask('')

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_web_server():
    # Render የሚሰጠውን የፖርት ቁጥር በራሱ ያገኛል
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. የአንተ የቦት ኮድ
BOT_TOKEN = "8559270696:AAE6uNlU0xFI1gwLqg87hmZAQWhRt3ZZoGw"  # ትክክለኛውን ቶክንህን እዚህ አስገባ
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ የፋይል ID ማውጫ ቦት ነኝ። እባክዎ ፎቶ ወይም ቪዲዮ ይላኩሉኝ።")

@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'voice'])
def get_file_id(message):
    file_id = ""
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
    elif message.content_type == 'voice':
        file_id = message.voice.file_id

    response_text = f"<code>{file_id}</code>\n\n👆 ለመቅዳት (Copy) ለማድረግ ጽሑፉን ይንኩት።"
    bot.reply_to(message, response_text, parse_mode="HTML")

# 3. ሁለቱንም በአንድ ላይ ማስነሻ
if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    
    print("ቦቱ መስራት ጀምሯል...")
    bot.infinity_polling()
