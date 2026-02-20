import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup for Render
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

TOKEN = '7589940160:AAHlESyClR6Igukl7HoqeMq1UgXojLJ_u30'
PASSWORD = "1199"
# অনুমোদিত ইউজারদের আইডি রাখার জন্য একটি সেট
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

    # যদি ইউজার এখনো পাসওয়ার্ড না দিয়ে থাকে
    if user_id not in authorized_users:
        if user_text == PASSWORD:
            authorized_users.add(user_id)
            # পাসওয়ার্ড মেসেজটি ডিলিট করে দেওয়া (সিকিউরিটির জন্য)
            try:
                await update.message.delete()
            except:
                pass 
            await update.message.reply_text("✅ পাসওয়ার্ড সঠিক! এখন আপনি M3U টেক্সট পাঠাতে পারেন।")
        else:
            await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
        return

    # পাসওয়ার্ড ভেরিফাইড ইউজারদের জন্য M3U প্রসেসিং
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
    keep_alive()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
