import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask সার্ভার সেটআপ (রেন্ডারকে জাগিয়ে রাখতে)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# টেলিগ্রাম বটের আগের কোড...
TOKEN = '7589940160:AAHlESyClR6Igukl7HoqeMq1UgXojLJ_u30'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("বট সচল আছে! টেক্সট পাঠান।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    file_name = "playlist.m3u"
    with open(file_name, "w", encoding="utf-8") as f:
        if not user_text.strip().startswith("#EXTM3U"):
            f.write("#EXTM3U\n")
        f.write(user_text)
    with open(file_name, "rb") as f:
        await update.message.reply_document(document=f, filename=file_name)
    os.remove(file_name)

def main():
    # জাগিয়ে রাখার ফাংশন কল
    keep_alive()
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
