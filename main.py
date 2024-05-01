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
            name = update.message.chat.first_name
            message = update.message.text.strip()
            print(f"Message from {name}: {message}")
            response = chatComplete(message=message, name=name)
            print(f"Response: {response}")
            update.message.reply_text(response)
        # for voice messages
        elif update.message.voice:
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
                    update.message.reply_audio(whisperReply)
            else:
                os.remove(file_name)
                update.message.reply_text(
                    "Something went wrong. Please try again later."
                )
        else:
            print("Unsupported format.")
            update.message.reply_text(
                "I'm sorry, This format is not supported at the moment."
            )
    except Exception as e:
        print(e)
        update.message.reply_text("Something went wrong. Please try again later.")


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