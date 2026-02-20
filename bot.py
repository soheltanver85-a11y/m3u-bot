import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# এখানে আমরা সরাসরি কোডে টোকেন না লিখে GitHub Environment Variable ব্যবহার করছি
TOKEN = os.environ.get('BOT_TOKEN')
PASSWORD = "1199"
authorized_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text("আপনি অলরেডি অনুমোদিত। আপনার M3U টেক্সট পাঠান।")
    else:
        await update.message.reply_text("স্বাগতম! এই বটটি ব্যবহার করতে পাসওয়ার্ড দিন।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in authorized_users:
        if user_text == PASSWORD:
            authorized_users.add(user_id)
            try:
                await update.message.delete()
            except:
                pass 
            await update.message.reply_text("✅ পাসওয়ার্ড সঠিক! এখন আপনি M3U টেক্সট পাঠাতে পারেন।")
        else:
            await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
        return

    file_name = f"playlist_{user_id}.m3u"
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            if not user_text.strip().startswith("#EXTM3U"):
                f.write("#EXTM3U\n")
            f.write(user_text)
        
        with open(file_name, "rb") as f:
            await update.message.reply_document(document=f, filename="playlist.m3u", caption="আপনার ফাইল তৈরি হয়েছে।")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

def main():
    if not TOKEN:
        logging.error("No BOT_TOKEN found in environment variables!")
        return
    keep_alive()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
