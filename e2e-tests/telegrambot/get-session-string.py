# Run this script to get the session string of a desired telegram client instance.

from urllib.parse import urlparse

import socks
from dotenv import dotenv_values
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Your API ID: "))
api_hash = input("Your API hash: ")

proxy_url = dotenv_values()['CRUSHBACK_TELEGRAM_PROXY_URL']
u = urlparse(proxy_url)
with TelegramClient(StringSession(), api_id, api_hash, proxy=(socks.PROXY_TYPE_SOCKS5, u.hostname, u.port or 80)) as client:
    print("Session string:", client.session.save())
