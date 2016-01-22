#!/usr/bin/env python3.4



#########Token###########
token_id = '171085474:AAGxtfIzCyGFJQJvNkC9TlEdvwq7zIEqJ4M'
#######################################################

from telegram import Updater



def start(bot,update):
    bot.sendMessage(update.message.chat_id, text="Hi there!")

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Help? Help Yourself!")


def main():
    updater = Updater(token=token_id)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()