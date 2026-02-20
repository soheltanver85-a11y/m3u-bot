import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup (সার্ভার সচল রাখার জন্য)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Logging কনফিগারেশন
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# GitHub Secrets থেকে নিরাপদে টোকেন সংগ্রহ
TOKEN = os.environ.get('BOT_TOKEN')
PASSWORD = "1199"
authorized_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text("আপনি ইতিমধ্যে অনুমোদিত। আপনার M3U টেক্সট পাঠান।")
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

    # M3U ফাইল জেনারেট করা
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
        logging.error("বট টোকেন পাওয়া যায়নি। GitHub Secrets চেক করুন।")
        return

    keep_alive() # Flask সার্ভার চালু
    
    # বট অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(TOKEN).build()
    
    # কমান্ড এবং মেসেজ হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("বট চালু হচ্ছে...")
    # Conflict এরর এড়াতে drop_pending_updates=True ব্যবহার করা হয়েছে
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
