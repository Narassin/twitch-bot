from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio
import os

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
access_token = os.getenv("TWITCH_ACCESS_TOKEN")
channel = os.getenv("CHANNEL_NAME")

print(channel)


def main():
    print("Hello from twitch-bot!")


if __name__ == "__main__":
    main()
