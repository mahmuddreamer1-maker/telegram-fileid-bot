import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# የቦትህን Token እዚህ አስገባ
BOT_TOKEN = "8559270696:AAE6uNlU0xFI1gwLqg87hmZAQWhRt3ZZoGw"

# ሎጊንግ ማስተካከል (በሰርቨር ላይ ሲሰራ ክትትል ለማድረግ)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# የ /start እና /help ትዕዛዝ ምላሽ
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **ሰላም! ወደ መደበኛው የ File ID ማገኚያ ቦት በደህና መጡ!**\n\n"
        "ማንኛውንም ፎቶ፣ ቪዲዮ፣ ኦዲዮ፣ ፋይል፣ ጂአይኤፍ (GIF) ወይም ስቲከር ይላኩሊኝ፤ "
        "እኔ ደግሞ መልሼ የፋይሉን **File ID** እሰጥዎታለሁ።\n\n"
        "📌 *IDውን ለመቅዳት (Copy ለማድረግ) የተላከውን ቁጥር አንዴ መንካት ብቻ ይበቃል!*"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# ፋይሎችን ተቀብሎ ID የሚያወጣው ዋና ተግባር
async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_id = ""
    content_type = ""

    try:
        # የፋይል አይነቶችን በዝርዝር መለየት
        if message.photo:
            file_id = message.photo[-1].file_id
            content_type = "PHOTO 📸"
        elif message.video:
            file_id = message.video.file_id
            content_type = "VIDEO 🎥"
        elif message.document:
            file_id = message.document.file_id
            content_type = "DOCUMENT 📄"
        elif message.audio:
            file_id = message.audio.file_id
            content_type = "AUDIO 🎵"
        elif message.voice:
            file_id = message.voice.file_id
            content_type = "VOICE 🎙️"
        elif message.animation:
            file_id = message.animation.file_id
            content_type = "GIF/ANIMATION 🎬"
        elif message.sticker:
            file_id = message.sticker.file_id
            content_type = "STICKER 🎭"
        elif message.video_note:
            file_id = message.video_note.file_id
            content_type = "TELEGRAM VIDEO NOTE 🔄"

        if file_id:
            response_text = (
                f"📂 **የፋይል አይነት:** `{content_type}`\n\n"
                f"🔑 **File ID:** (ለመቅዳት ይንኩት)\n"
                f"`{file_id}`"
            )
            await message.reply_text(response_text, parse_mode="Markdown")
            
    except Exception as e:
        logger.error(f"ስህተት ተከስቷል: {e}")
        await message.reply_text("⚠️ አዝናለሁ፣ የዚህን ፋይል ID ማውጣት አልቻልኩም። እባክዎ እንደገና ይሞክሩ።")

# ተጠቃሚው ፋይል ሳይሆን ተራ ጽሑፍ (Text) ሲልክ የሚመልሰው
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error_msg = "⚠️ **እባክዎ ጽሑፍ ሳይሆን ፋይል ይላኩሊኝ!** (ፎቶ፣ ቪዲዮ፣ ዶክመንት፣ ስቲከር...)"
    await update.message.reply_text(error_msg, parse_mode="Markdown")

def main():
    # ቦቱን መገንባት
    application = Application.builder().token(BOT_TOKEN).build()

    # የትዕዛዝ (Commands) አያያዝ
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", start_command))

    # የፋይሎች ማጣሪያ (Filters)
    file_filter = (
        filters.PHOTO | filters.VIDEO | filters.Document.ALL | 
        filters.AUDIO | filters.VOICE | filters.ANIMATION | filters.Sticker.ALL
    )
    application.add_handler(MessageHandler(file_filter, handle_files))

    # ተጠቃሚው ፋይል ሳይሆን ጽሑፍ ብቻ ሲልክ የሚይዝ ማጣሪያ
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("እንከን የለሽ ቦት ስራ ጀምሯል...")
    application.run_polling()

if __name__ == '__main__':
    main()
