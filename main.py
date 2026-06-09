import os
import asyncio
import random
# import sleep
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand

load_dotenv()
# CONSTANTS
APP_ID = os.getenv("TWITCH_CLIENT_ID")
APP_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = os.getenv("CHANNEL_NAME")


print(TARGET_CHANNEL)

async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')

async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\n'
          f'  Type: {sub.sub_plan}\n'
          f'  Message: {sub.sub_message}')

# Random Lurk
async def lurk_command(cmd: ChatCommand):
    chance = random.randint(0,4)

    if chance == 0:
        await cmd.reply(f'{cmd.user.name} managed to find the Archive Loungue and is now chilling narass1Lurk  ')
    elif chance == 1:
        await cmd.reply(f'{cmd.user.name} accidentally wandered into the Archive training hall and is now battling a horde of training zombies narass1NYUU ')
    elif chance == 2:
        await cmd.reply(f'{cmd.user.name} is lost in the Archive Hall of Mirrors, they will be back once they find the exit! narass1Lurk ')
    elif chance == 3:
        await cmd.reply(f'{cmd.user.name} was called by the Archive Galactic Federation. Oh boy, all the best mate narass1Ohnyu ')
    elif chance == 4:
        await cmd.reply(f'{cmd.user.name} is lurking in the shadows... They will be back soon! Maybe? narass1Lurk ')


    
# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('reply', test_command)
    chat.register_command('lurk', lurk_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


asyncio.run(run())