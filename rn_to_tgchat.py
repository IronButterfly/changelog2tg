import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
URL = 'https://www.your_domain.tld/changelog'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot is up and running. Expect messages...')

def get_release_notes() -> str:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Here you must specify how to find Release Notes on the web page.
    #  For example, if Release Notes are in a <p> tag with the class 'release-notes':
    release_notes = soup.find('div', class_='js-changelog-item')

    return release_notes.text if release_notes else None

def publish_release_notes(bot: Bot, release_notes: str) -> None:
    bot.send_message(chat_id=CHAT_ID, text=release_notes)

def main() -> None:
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    last_release_notes = None

    while True:
        release_notes = get_release_notes()

        if release_notes and release_notes != last_release_notes:
            publish_release_notes(updater.bot, release_notes)
            last_release_notes = release_notes

        time.sleep(60*60)  # Checking every hour

    updater.idle()

if __name__ == '__main__':
    main()
