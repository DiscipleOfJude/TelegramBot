#!/usr/bin/env python3.4



#########Token###########
token_id = '171085474:AAGxtfIzCyGFJQJvNkC9TlEdvwq7zIEqJ4M'
#######################################################

from telegram import Updater
import random


def start(bot,update):
    bot.sendMessage(update.message.chat_id, text="Hi there!")

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Help? Help Yourself!")

def verifyme(bot, update):
    code = random.randrange(10000,99999)
    bot.sendMessage(update.message.chat_id, text="So you want to verify? Great! That's how you get into our main" +
                    "room!\n What we need from you is a picture, but not just any picture. It needs to be of you," +
                    "your partner(s), and show you holding something with the following things visible.\n 1) Your "+
                    "usernames.\n 2) The current date\n 3) The following code {}".format(code) +
                    "Make sure you picture contains those three things, there are no exceptions." +
                    "\n\n  The Admins of this room will check your photo, and may ask you further questions.\n " +
                    "The Admins will never PM you, if you are PM'ed from anyone in this holding room they are not" +
                    " an admin, nor are they verified. Do not trust them." +
                    "\n\n\n WE RESERVE THE RIGHT TO REFUSE ENTERANCE FROM OUR MAIN ROOM")

def main():
    updater = Updater(token=token_id)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('verifyme', verifyme)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()