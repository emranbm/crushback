import asyncio
import os
from asyncio import sleep
from contextlib import asynccontextmanager
from subprocess import Popen

import socks
from django.test import TestCase
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom import Message, Conversation


class AddcrushTest(TestCase):
    TEST_BOT_USERNAME = "crushback_test_bot"

    bot_process: Popen = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        cls.api_id = int(os.environ['CRUSHBACK_TEST_TELEGRAM_API_ID'])
        cls.api_hash = os.environ['CRUSHBACK_TEST_TELEGRAM_API_HASH']
        cls.session_str = os.environ['CRUSHBACK_TEST_TELEGRAM_SESSION_STRING']
        cls.socks_host = os.environ.get('CRUSHBACK_TEST_TELEGRAM_SOCKS_HOST')
        cls.socks_port = os.environ.get('CRUSHBACK_TEST_TELEGRAM_SOCKS_PORT')
        cls.use_socks_proxy = bool(cls.socks_host and cls.socks_port)

        start_bot_command = [
            "./manage.py",
            "telegrambot",
            "--token",
            os.environ['CRUSHBACK_TEST_TELEGRAM_TEST_BOT_TOKEN'],
        ]
        if cls.use_socks_proxy:
            start_bot_command += [
                "--proxy",
                f"socks5://{cls.socks_host}:{cls.socks_port}",
            ]
        cls.bot_process = Popen(start_bot_command)

    @classmethod
    def tearDownClass(cls):
        cls.bot_process.kill()

    # Could not use setUp standard methods!
    # When the telegram client is created there, the client hangs on sending messages, surprisingly!
    @asynccontextmanager
    async def _create_telegram_client(self) -> TelegramClient:
        telegram_client = TelegramClient(
            StringSession(self.session_str), self.api_id, self.api_hash, sequential_updates=True
        )
        if self.use_socks_proxy:
            telegram_client.set_proxy((socks.PROXY_TYPE_SOCKS5, self.socks_host, int(self.socks_port)))
        await telegram_client.connect()
        await telegram_client.get_me()
        await telegram_client.get_dialogs()

        yield telegram_client

        await telegram_client.disconnect()
        await telegram_client.disconnected

    @asynccontextmanager
    async def _create_conversation(self) -> Conversation:
        telegram_client_context_manager = self._create_telegram_client()
        telegram_client = await telegram_client_context_manager.__aenter__()
        conversation_context_manager = telegram_client.conversation(self.TEST_BOT_USERNAME, timeout=10)
        conversation = await conversation_context_manager.__aenter__()
        await sleep(0.5)  # A hack recommended at https://shallowdepth.online/posts/2021/12/end-to-end-tests-for-telegram-bots/

        yield conversation

        await conversation_context_manager.__aexit__(None, None, None)
        await telegram_client_context_manager.__aexit__(None, None, None)

    async def test_should_reply_appropriate_message_on_addcrush_command(self):
        async with self._create_conversation() as conv:
            await conv.send_message('/addcrush')
            msg: Message = await conv.get_response()
            self.assertEqual("OK! Please send me your crush's username.\n"
                             "Or /cancel.(This is experimental and doesn't work yet!)",
                             msg.text)
