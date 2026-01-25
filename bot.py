import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটআপ (বটে কোনো ভুল হলে যেন বোঝা যায়)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# আপনার দেওয়া বটের টোকেন
TOKEN = '7589940160:AAHlESyClR6Igukl7HoqeMq1UgXojLJ_u30'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "স্বাগতম! 👋\n\n"
        "আপনার M3U লিস্টের টেক্সটগুলো এখানে পাঠান। "
        "আমি সেগুলোকে একটি .m3u ফাইলে রূপান্তর করে দিচ্ছি।"
    )
    await update.message.reply_text(welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    file_name = "playlist.m3u"
    
    # প্রসেসিং মেসেজ
    status_msg = await update.message.reply_text("ফাইল তৈরি হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        # টেক্সটটিকে ফাইলে রূপান্তর
        with open(file_name, "w", encoding="utf-8") as f:
            # যদি টেক্সটে মেইন হেডার না থাকে তবে যোগ করবে
            if not user_text.strip().startswith("#EXTM3U"):
                f.write("#EXTM3U\n")
            f.write(user_text)
        
        # ফাইলটি পাঠানো
        with open(file_name, "rb") as f:
            await update.message.reply_document(
                document=f, 
                filename=file_name, 
                caption="✅ আপনার M3U ফাইলটি সফলভাবে তৈরি হয়েছে।"
            )
            
    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}")
    
    finally:
        # মেসেজ ডিলিট এবং টেম্পোরারি ফাইল রিমুভ
        await status_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)

def main():
    # অ্যাপ্লিকেশন তৈরি
    app = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার যুক্ত করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("বটটি এখন সচল আছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
