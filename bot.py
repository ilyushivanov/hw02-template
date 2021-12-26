import requests
from bs4 import BeautifulSoup
from telegram import Update, InputMediaPhoto, bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import qrcode

youtube_link = 'https://www.youtube.com/results?search_query='
ddg_link = 'http://duckduckgo.com/html/?q='
yahoo_link1 = 'https://images.search.yahoo.com/search/images;_ylt=AwrE1xL0fa1h.8IApg1XNyoA;_ylu' \
              '=Y29sbwNiZjEEcG9zAzEEdnRpZANGT05UVEVTVF8xBHNlYwNwaXZz?p= '
yahoo_link2 = '&fr2=piv-web&fr=yfp-t'
headers = {'user-agent': 'my-agent-0.0.1'}


def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.message.from_user.first_name}!')


def time(update: Update, context: CallbackContext):
    update.message.reply_text(f'{update.message.date}')


def qr(update: Update, context: CallbackContext):
    word = update.message.text.replace('/q ', '')
    img = qrcode.make(word)
    img.save('qr.jpg')
    photo = open('qr.jpg', 'rb')
    update.message.reply_photo(photo)


def duck(update: Update, context: CallbackContext):
    url = ddg_link + update.message.text.replace('/s ', '')
    response = requests.post(url,  headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    sidebar = soup.find(id='links')
    links1 = sidebar.find_all('a', class_='result__a')
    links2 = sidebar.find_all('a', class_='result__url')
    if links1:
        for i in range(3):
            link1 = links1[i]
            link2 = links2[i]
            url = link2.text.replace('\n                  ', '')
            text = f'<a href="https://{url}">{link1.text}</a>'
            update.message.reply_html(text)


def yahoo(update: Update, context: CallbackContext):
    url = yahoo_link1 + update.message.text.replace('/p ', '') + yahoo_link2
    response = requests.post(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sidebar = soup.find(id='results')
    links = sidebar.find_all('img', class_='')
    if links:
        for i in range(3):
            link = links[i]
            url = link['src']
            text = f'<a href="{url}">Результат №{i + 1}</a>'
            update.message.reply_html(text)


with open('token(python 08.11.21).txt') as f:
    token = f.readline()

updater = Updater(token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('time', time))
dispatcher.add_handler(CommandHandler('q', qr))
dispatcher.add_handler(CommandHandler('s', duck))
dispatcher.add_handler(CommandHandler('p', yahoo))

updater.start_polling()
updater.idle()

