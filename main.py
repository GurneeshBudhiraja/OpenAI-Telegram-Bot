import logging
import os
import requests
from dotenv import load_dotenv
from telegram import (
    Update,
)
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
)
from utils import chatComplete, whisperModel

load_dotenv()
telegramToken = os.getenv("TELEGRAM_TOKEN")


logger = logging.getLogger(__name__)


def userMessage(update: Update, context: CallbackContext):
    try:
        if update.message.text:
            update.message.reply_text("Processing your message📝...")
            name = update.message.chat.first_name
            message = update.message.text.strip()
            print(f"Message from {name}: {message}")


            response = chatComplete(message=message, name=name)
            print(f"Response: {response}")
            update.message.reply_text(response)
        # for voice messages
        elif update.message.voice:
            update.message.reply_text("Processing your voice message🎙...")
            name = update.message.chat.first_name
            voice = update.message.voice
            voice_file = voice.get_file()
            file_url = voice_file["file_path"]
            file_name = file_url.split("/")[-1]  # Extract file name from URL
            response = requests.get(file_url)
            if response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(response.content)
                    whisperReply = whisperModel(audiofile=file_name, name=name)
                    os.remove(file_name)
                    print(f"Whisper Reply: {whisperReply}")
                    update.message.reply_audio(audio=open(f"{whisperReply}", "rb"))
                    os.remove(whisperReply)
                    print("file removed successfully...")
            else:
                os.remove(file_name)
                update.message.reply_text(
                    "Something went wrong. Please try again later."
                )
        else:
            print("Unsupported format.")
            update.message.reply_animation("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2Q3cDI0ZjUwdWh6Mmx0OXB6Y2pyZ2JpNGh0dGNld2JiaGRhdjYwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YQAuKJ7wf68qBHPw6Y/giphy.gif",height=25,width=25,caption="Only text and audio input are supported. ⚠️")
    except Exception as e:
        print(e)
        update.message.reply_animation("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdThpeHJneDU5Z3pmbjRnZWd0MnFrdXVyOGFrMDA2Mmt2eXYwa2M1dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26u6bnal23NhnIoZG/giphy.gif",caption="Something went wrong. Please try again later. ❌")

def main():
    updater = Updater(telegramToken)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(MessageHandler(Filters.all, userMessage))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()