import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot Token এখানে দিন
TOKEN = 'আপনার_বট_টোকেন'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আপনার M3U লিস্টের টেক্সটগুলো পাঠান, আমি ফাইল বানিয়ে দিচ্ছি!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # ফাইলের নাম ঠিক করা
    file_name = "playlist.m3u"
    
    # টেক্সটটিকে ফাইলে রূপান্তর
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n") # M3U এর হেডার
        f.write(user_text)
    
    # ফাইলটি ইউজারকে পাঠানো
    with open(file_name, "rb") as f:
        await update.message.reply_document(document=f, filename=file_name, caption="আপনার M3U ফাইলটি তৈরি হয়েছে।")
    
    # কাজ শেষ হলে ফাইলটি ডিলিট করে দেয়া (পরিচ্ছন্নতার জন্য)
    os.remove(file_name)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("বট চলছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
