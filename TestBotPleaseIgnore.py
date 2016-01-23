#!/usr/bin/env python3.4



#########Token###########
token_id = '171085474:AAGxtfIzCyGFJQJvNkC9TlEdvwq7zIEqJ4M'
#######################################################

import telegram
import time
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
   # time.sleep(5)
   # for x in range(1,5):
   #     print(x)
   #     time.sleep(5)
   # last_id = update.message.photo.file_id
   # message = update.message
   # print(message)
   # time.sleep(10)
   # message = update.message
   # print(message)
   # time.sleep(10)
   # message = update.message
   # print(message)
   # print(last_id)
   telegram.ForceReply(force_reply=True)
   bot.sendMessage(update.message.chat_id, text="Please attach your picture as a reply to this message, and I will " +
                   "attempt to send it to the admins.")



    #bot.sendPhoto(chat_id=chat_id, photo=last_file_id)

def main():
    updater = telegram.Updater(token=token_id)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('verifyme', verifyme)
    dispatcher.addTelegramCommandHandler('verifypic', verifypic)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()