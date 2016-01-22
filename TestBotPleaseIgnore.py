#!/usr/bin/env python3.4



#########Token###########
token_id = '171085474:AAGxtfIzCyGFJQJvNkC9TlEdvwq7zIEqJ4M'
#######################################################

from telegram import Updater
import telegram
import random


def start(bot,update):
    bot.sendMessage(update.message.chat_id, text="Hi there!")

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Help? Help Yourself!")

def verifyme(bot, update):
    code = random.randrange(10000,99999)
    bot.sendMessage(update.message.chat_id, text="So you want to verify? Great! That's how you get into our main" +
                    "room!\n\nWhat we need from you is a picture, but not just any picture. It needs to be of you," +
                    "your partner(s), and  has to show you holding something with the following things visible.\n\n"+
                    "1) Your usernames\n2) The current date\n3) The following code {} ".format(code) +
                    "\n\nMake sure you picture contains those three things, there are no exceptions!".upper() +
                    "\n\nThe Admins of this room will check your photo, and may ask you further questions.\n" +
                    "\nThe Admins will never PM you, if you are PM'ed from anyone in this holding room they are not" +
                    " an admin, nor are they verified. Do not trust them." +
                    "\n\n\n WE RESERVE THE RIGHT TO REFUSE ENTRANCE FROM OUR MAIN ROOM")

def verifypic(bot, update):
    last_file_id = update.message.file_id
    print(last_file_id)
    bot.sendPhoto(chat_id=chat_id, photo=last_file_id)

def main():
    updater = Updater(token=token_id)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('verifyme', verifyme)
    dispatcher.addTelegramCommandHandler('verifypic', verifypic)
    updater.start_polling()
    updater.idle()
    dispatcher.addTypeHandler()

if __name__ == '__main__':
    main()