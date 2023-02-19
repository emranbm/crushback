import socks
from telethon import TelegramClient
from telethon.sessions import StringSession

SOCKS_HOST = '127.0.0.1'
SOCKS_PORT = 9000

if __name__ == "__main__":
    api_id = int(input("API ID: "))
    api_hash = input("API hash: ")
    with TelegramClient(StringSession(),
                        api_id,
                        api_hash,
                        proxy=(socks.PROXY_TYPE_SOCKS5, SOCKS_HOST, SOCKS_PORT)) as client:
        print("Session string:", client.session.save())
