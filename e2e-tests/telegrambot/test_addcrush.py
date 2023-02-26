import os
import subprocess
from asyncio import sleep
from contextlib import asynccontextmanager
from subprocess import Popen
from urllib.parse import urlparse

import socks
from aiounittest import AsyncTestCase
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom import Message, Conversation


class AddcrushTest(AsyncTestCase):
    BACKEND_PATH = "../../backend/"

    bot_process: Popen = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.api_id = int(os.environ['CRUSHBACK_TEST_TELEGRAM_API_ID'])
        cls.api_hash = os.environ['CRUSHBACK_TEST_TELEGRAM_API_HASH']
        cls.session_str = os.environ['CRUSHBACK_TEST_TELEGRAM_SESSION_STRING']
        cls.proxy_url = os.environ.get('CRUSHBACK_TELEGRAM_PROXY_URL', None)
        cls.test_bot_username = os.environ['CRUSHBACK_TELEGRAM_BOT_USERNAME']
        cls.bot_process = cls._run_bot_process()

    @classmethod
    def _run_bot_process(cls):
        stdout: bytes = subprocess.check_output(["bash", "-c", "pipenv --venv"],
                                                cwd=cls.BACKEND_PATH,
                                                env={})
        backend_venv_path = stdout.decode("utf-8").strip()
        env = {'CRUSHBACK_TELEGRAM_BOT_TOKEN': os.environ['CRUSHBACK_TELEGRAM_BOT_TOKEN']}
        if cls.proxy_url is not None:
            env['CRUSHBACK_TELEGRAM_PROXY_URL'] = cls.proxy_url
        return Popen([
            f"{backend_venv_path}/bin/python3.8",
            "./manage.py",
            "telegrambot",
        ],
            cwd=cls.BACKEND_PATH,
            env=env)

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
        if self.proxy_url is not None:
            u = urlparse(self.proxy_url)
            assert u.scheme == "socks5", "Expected to use socks5 proxy; change if it's not the case."
            telegram_client.set_proxy((socks.PROXY_TYPE_SOCKS5, u.hostname, u.port or 80))
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
        conversation_context_manager = telegram_client.conversation(self.test_bot_username, timeout=10)
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
            await conv.send_message('/cancel')
