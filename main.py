
import os
import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# --- FLASK SERVER FOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render ആവശ്യപ്പെടുന്ന പോർട്ട്‌ ബിൻഡ് ചെയ്യുന്നു
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIC ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Render-ൽ നമ്മൾ നൽകിയ BOT_TOKEN ഇവിടെ എടുക്കുന്നു
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ഹലോ! സിനിമയുടെ പേരോ ലിങ്കോ അയച്ചു തരൂ...")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        return
    
    msg = await update.message.reply_text("വീഡിയോ പ്രോസസ്സ് ചെയ്യുന്നു... ദയവായി കാത്തിരിക്കൂ.")
    
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
        await update.message.reply_text(f"ക്ഷമിക്കണം, ഒരു എറർ സംഭവിച്ചു: {e}")

async def main():
    # Flask സെർവർ സ്റ്റാർട്ട് ചെയ്യുന്നു
    keep_alive()
    
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("Bot is running...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    # ബോട്ട് എപ്പോഴും റൺ ചെയ്യാൻ
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
