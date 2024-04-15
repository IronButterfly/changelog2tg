import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
URL = 'https://www.ispmanager.ru/changelog'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот запущен. Ожидайте сообщений...')

def get_release_notes() -> str:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Здесь вы должны указать, как найти Release Notes на веб-странице.
    # Например, если Release Notes находятся в теге <p> с классом 'release-notes':
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

        time.sleep(60*60)  # Проверяем каждый час

    updater.idle()

if __name__ == '__main__':
    main()
