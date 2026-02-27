import os
import yt_dlp
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your Token
TOKEN = '8620685344:AAElYVhUeeLzkg7grAH4V68l_0k2AMZTlo0'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ഹായ്! ഇൻസ്റ്റാഗ്രാം അല്ലെങ്കിൽ ടിക് ടോക് ലിങ്ക് അയച്ചു തരൂ, ഞാൻ വീഡിയോ ഡൗൺലോഡ് ചെയ്തു തരാം. 📥')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        return
    msg = await update.message.reply_text('വീഡിയോ റെഡിയാക്കുന്നു... ദയവായി കാത്തിരിക്കൂ ⏳')
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        await msg.delete()
        os.remove('video.mp4') 
    except Exception as e:
        await update.message.reply_text('ക്ഷമിക്കണം, ഈ ലിങ്ക് ഡൗൺലോഡ് ചെയ്യാൻ പറ്റിയില്ല. ❌')

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    async with app:
        await app.initialize()
        await app.start()
        print("Bot is running...")
        await app.updater.start_polling(drop_pending_updates=True)
        # Keep the bot running
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
