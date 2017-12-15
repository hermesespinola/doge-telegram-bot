from telegram.ext import Updater
updater = Updater(token='token')
dispatcher = updater.dispatcher

doge_words = ['such ', 'much ', 'very ', 'so ', 'many ', 'how ']
words = ['doge', 'bot', 'python', 'grrrrr']
max_words_len = 500

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="""I'm Da Dogebot!
    Use /doge to create an image or talk to me to learn new words""")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

from stop_words import get_stop_words
stop_words = get_stop_words('english') + get_stop_words('spanish')
def echo(bot, update):
    global words
    chat_id = update.message.chat_id
    words += list(filter(lambda w: w not in stop_words and w not in words and w not in doge_words,
            update.message.text.lower().split(' ')))
    for _ in range(len(words) - max_words_len):
        words.pop(0)
    text_caps = ' '.join(update.message.text.upper())
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

from random import shuffle, choice
def doge(bot, update, args):
    global words
    chat_id = update.message.chat_id
    args = list(filter(lambda w: w not in stop_words and w not in words and w not in doge_words,
        map(lambda w: w.lower(), args)))
    if not args:
        args = [choice(words),choice(words),choice(words),choice(words),choice(words),choice(words)]
    else:
        words += args
        for _ in range(len(words) - max_words_len):
            word.pop(0)
        shuffle(doge_words)

    for i, arg in enumerate(args):
        args[i] = doge_words[i % len(doge_words)] + args[i]
    args.append('wow')
    shuffle(args)
    photo_url = 'http://dogr.io/' + '/'.join(args) + '.png?split=false'
    bot.send_photo(chat_id=update.message.chat_id, photo=photo_url)

doge_handler = CommandHandler('doge', doge, pass_args=True)
dispatcher.add_handler(doge_handler)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print('Unauthorized')
    except BadRequest:
        print('BadRequest')
    except TimedOut:
        print('TimedOut')
    except NetworkError:
        print('NetworkError')
    except ChatMigrated as e:
        print('ChatMigrated')
    except TelegramError:
        print('TelegramError')

dispatcher.add_error_handler(error_callback)

updater.start_polling()
print('@Da_Dogebot listening...')
updater.idle()
