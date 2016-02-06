#!/usr/bin/env python3.4



#########Token###########
token_id = '171085474:AAGxtfIzCyGFJQJvNkC9TlEdvwq7zIEqJ4M'
#######################################################

# https://github.com/python-telegram-bot/python-telegram-bot
# http://python-telegram-bot.readthedocs.org/en/latest/


######
#
# Make it dynamic. Should be able to handle multiple rooms. Each room will have a pending room and a live room.
#
# Features:
#    - Handle multiple rooms, including waiting rooms and actual rooms, and a universal admin room (and private chats).
#    - Send periodic alarms to the admin room reminding them if people are waiting for verification.
#    - Alert the admin room when someone submits a verification request.
#
# Command Ideas:
#
#    /verify <user> <room> - ADMIN ONLY. verifies the named user. if no user is provided, shows you who all is pending verification (with picture). should only show to admins (in admin chat or in private chat)
#                * should be able to tell which room the person wants to be verified in.
#                * should store users name, status (verified), date verified, who verified them, and what room they are verified for.
#    /unverify <user> <room> - ADMIN ONLY. remove verification status for a user.
#
#    /letmein    - When in a pending room, bot will check to see if the requesting user is verified and then automatically invite them into the actual room.
#
#    /verified <room|admin|user> - ADMIN ONLY. With no parameters, will show a list of everyone who has been verified, what rooms they are verified in, and who verified them.
#            * Given a room name, shows all the same info but only for a specific room.
#            * Given an admin name, shows all the people that admin has verified.
#            * Given a user, shows all the rooms that user is verified in.
#
#    /addadmin <name> - ADMIN ONLY. Create a new admin.
#    /removeadmin <name> - ADMIN ONLY. Remove an admin.
#    /showadmins    - ADMIN ONLY. show everyone who is an admin.
#

#    update.message.from_user
#    update.message.from_user.username
#    update.message.from_user.type
#    update.message.from_user.first_name
#    update.message.from_user.last_name

#    update.message.chat
#    update.message.chat.type
#    update.message.chat.title

#    update.message.date

import telegram
import time
import random
from pprint import pprint

pending = []
verified = []

##########################################################################################################

#####################################################
## DATABASE TABLES
#####################################################
##
##    rooms            - Defines the room name, the waiting room for it, and whether its the admin room or not.
##        id
##        room_name
##        waiting_room
##        isAdminRoom
##
##
##    roomAdmins        - Based on a room id and user id, defines all people who are admins for a given room.
##        id
##        room_id
##        users_id
##
##    users            - defines common info for a user, across all rooms (photo, name, is_admin)
##        id
##        user_name
##        photo
##        is_admin
##
##    user_status        - for each room, specifies a users status in it.
##        id
##        user_id
##        room_id
##        status (verified, pending, unverified, banned)
##        admin_id
##        status_date

## dp.addTelegramRegexHandler('^$', empty_message)
## if update.message.new_chat_participant.username == BOTNAME: <-- determines if someone joined!


#####
## Database Functions
#####
def db_getAdmins(room=None):    # Query the database for all of the admins, optionally provide just the admins for the provided room.
    if room is None:
        # select user_name from users where is_admin = True
        return ("thewalkingzed","raeltik")
    else:
        # select u.user_name from users as u, rooms as r, roomAdmins as a where u.is_admin and r.room_name=room and r.id = a.room_id and a.users_id = u.id
        return ("thewalkingzed","raeltik","randomRoomAdmin")

def db_getRoomId(room):
    # select id from rooms where room_name == room
    return 1

def db_getRoomIdByWaitingRoom(room):
    # select id from rooms where waiting_room == room
    return 1

def db_getUserId(user_name):
    # select id from users where user_name = user_name
    return 1

def db_createUser(name,photo=None,admin=False):
    # insert into users, whatever goes here...
    return True


def db_setVerified(user,room,date,admin):    # Set the user to verified in the defined room.
    # Verify that the user actually exists, and the admin actually exists, and the room actually exists...
    r_id = db_getRoomId(room)
    u_id = db_getUserId(user)
    a_id = db_getUserId(admin)
    # insert into user_status user_id = u_id, room_id = r_id, admin_id = a_id, status_date=date, status="verified"
    bot.sendMessage(update.message.chat_id, text="%s has been verified in %s by %s"%(user,room,admin))
    return True

def db_getRoomFromPending(pending_name): # Query the room list to match the name of the pending room to the name of the actual room.
    # Return room name as string if found, otherwise return None.
    return "ActualRoomName"


def db_getPendingVerifications(room=None):    # Return a list of people waiting for verification. If room is not None, then only return for people in that room.
    return [("randomuser","picture_id","room1"),("randomperv","picture_id2","room1")]


#####
## Utility Functions
#####
def isAdminRoom(room):    # Return true if the room the request was sent from is the Admin room.
    return False

def isAdmin(user, room=None):    # If user is an admin, return true. Else, return false.
    if user in db_getAdmins(room):    return True
    return False

def isWaitingRoom(room):    # Return true if this is a waiting room, doesn't matter WHICH waiting room.
    room_id = db_getRoomIdByWaitingRoom(room)
    if room_id != None:    return True
    else:    return False

def getRoomFromPending(pending_name): # Given the name of a pending/waiting room, return the name of the actual chat room.
    return db_getRoomFromPending(pending_name)

#####
## Commands
#####


#    /verify <user> - ADMIN ONLY. verifies the named user. if no user is provided, shows you who all is pending verification (with picture). should only show to admins (in admin chat or in private chat)
#                * should be able to tell which room the person wants to be verified in.
#                * should store users name, status (verified), date verified, who verified them, and what room they are verified for.
def verify(bot, update, args):
    admin = update.message.from_user.username

    if not isAdmin(admin):
        bot.sendMessage(update.message.chat_id, text="Sorry, you are not an authorized administrator.")
        return False

    if len(args)>0:    # user provided, verify them. ##### REPLACE THIS WITH A SIMPLE TRY/EXCEPT! except IndexError:
        new_user = args[0]
        if len(args)>1: waiting_room = args[1]
        elif isAdminRoom(update.message.chat.title) or update.message.chat.type=="private":
            bot.sendMessage(update.message.chat_id, text="I need to know which room to verify this user for.")
            return False
        else:
            waiting_room = update.message.chat.title
        room=getRoomFromPending(waiting_room)
        if room == None:
            bot.sendMessage(update.message.chat_id, text="Sorry, I do not currently manage any rooms with %s as the waiting room."%waiting_room)
            return False

        if not isAdmin(admin,room):    # Found the room, but is this admin allowed to verify for it?
            bot.sendMessage(update.message.chat_id, text="Sorry, you are not an administrator authorized to verify people in %s."%room)
            return False

        db_setVerified(user,room,update.message.date,admin)
        bot.sendMessage(update.message.chat_id, text="Congrats, %s has been verified to move to %s."%(user,room))
        return True

    else:
        current_room = update.message.chat.title
        if isWaitingRoom(current_room):
            pending = db_getPendingVerifications(current_room)
        elif isAdminRoom(current_room) or update.message.chat.type=="private":
            pending = db_getPendingVerifications()

        for x in pending:
            bot.sendPhoto(update.message.chat_id, x[1], caption="%s requests access from %s"%(x[0],x[2]))

    return True

def unverify(bot, update, args):    # Change the
    if not isAdmin(update.message.from_user.username):
        bot.sendMessage(update.message.chat_id, text="Sorry, you are not an authorized administrator.")
    return False



#####################################################

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
   reply_markup = telegram.ForceReply(force_reply=True)
   bot.sendMessage(update.message.chat_id, text="Please attach your picture as a reply to this message, and I will " +
                   "attempt to send it to the admins.",reply_markup=reply_markup)


def pic_forwarder(bot, update):
    print("caught something")
    if update.message.photo[0].file_id:
        print("found a pic")
        verify_pic  = (update.message.photo[0].file_id)
        print(verify_pic)
        print(update.message['chat']['username'])
        pending.append((update.message['chat']['username'],update.message.photo[0]))
    else:
        print("didn't find a picture :/")
        updates = update.message
        print(updates)


'''
def verify(bot, update, args):
    print("The following people want to be verified:")
    if len(args) > 0:
        print("Ok, let's verify %s"%args[0])
    else:
        for x in pending:
            print(x)
            bot.sendPhoto(update.message.chat_id,photo=x[1].file_id,caption=x[0])
'''


def main():
    updater = telegram.Updater(token=token_id)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('verifyme', verifyme)
    dispatcher.addTelegramCommandHandler('verifypic', verifypic)
    dispatcher.addTelegramCommandHandler('verify', verify)
    dispatcher.addTelegramMessageHandler(pic_forwarder)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
Status API Training Shop Blog About Pricing
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
