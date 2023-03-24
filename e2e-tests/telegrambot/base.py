import os
import subprocess
from asyncio import sleep
from contextlib import asynccontextmanager
from time import sleep as sync_sleep
from urllib.parse import urlparse

import socks
from aiounittest import AsyncTestCase
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom import Conversation


class TelegramBotTestCase(AsyncTestCase):
    ROOT_DIR = "../.."
    BACKEND_DIR = f"{ROOT_DIR}/backend/"
    CHECK_MATCH_PERIOD_SECONDS = 1

    bot_process: subprocess.Popen = None
    check_matches_process: subprocess.Popen = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.clients = [
            {
                'username': os.environ['CRUSHBACK_TELEGRAM_CLIENT1_USERNAME'],
                'api_id': int(os.environ['CRUSHBACK_TELEGRAM_CLIENT1_API_ID']),
                'api_hash': os.environ['CRUSHBACK_TELEGRAM_CLIENT1_API_HASH'],
                'session_str': os.environ['CRUSHBACK_TELEGRAM_CLIENT1_SESSION_STRING'],
            },
            {
                'username': os.environ['CRUSHBACK_TELEGRAM_CLIENT2_USERNAME'],
                'api_id': int(os.environ['CRUSHBACK_TELEGRAM_CLIENT2_API_ID']),
                'api_hash': os.environ['CRUSHBACK_TELEGRAM_CLIENT2_API_HASH'],
                'session_str': os.environ['CRUSHBACK_TELEGRAM_CLIENT2_SESSION_STRING'],
            },
        ]
        cls.api_id = int(os.environ['CRUSHBACK_TELEGRAM_CLIENT1_API_ID'])
        cls.api_hash = os.environ['CRUSHBACK_TELEGRAM_CLIENT1_API_HASH']
        cls.session_str = os.environ['CRUSHBACK_TELEGRAM_CLIENT1_SESSION_STRING']
        cls.proxy_url = os.environ.get('CRUSHBACK_TELEGRAM_PROXY_URL', None)
        cls.test_bot_username = os.environ['CRUSHBACK_TELEGRAM_BOT_USERNAME']
        cls.backend_venv_path = cls._get_backend_venv_path()
        cls._start_database()
        cls._run_backend_manage_command("migrate").communicate()
        cls.bot_process = cls._run_backend_manage_command("telegrambot")
        cls.check_matches_process = cls._run_backend_manage_command("checkmatches", "--period", str(cls.CHECK_MATCH_PERIOD_SECONDS))

    @classmethod
    def _get_backend_venv_path(cls):
        stdout: bytes = subprocess.check_output(["bash", "-c", "pipenv --venv"],
                                                cwd=cls.BACKEND_DIR,
                                                env={})
        backend_venv_path = stdout.decode("utf-8").strip()
        return backend_venv_path

    @classmethod
    def _start_database(cls):
        subprocess.Popen(["docker-compose", "up", "-d", "database"],
                         cwd=cls.ROOT_DIR).communicate()
        sync_sleep(2)  # Wait for DB to get ready

    @classmethod
    def _stop_database(cls):
        subprocess.Popen(["docker-compose", "down"],
                         cwd=cls.ROOT_DIR).communicate()

    @classmethod
    def _run_backend_manage_command(cls, *cmd: str) -> subprocess.Popen:
        env = {'CRUSHBACK_TELEGRAM_BOT_TOKEN': os.environ['CRUSHBACK_TELEGRAM_BOT_TOKEN']}
        if cls.proxy_url is not None:
            env['CRUSHBACK_TELEGRAM_PROXY_URL'] = cls.proxy_url
        return subprocess.Popen((
                                    f"{cls.backend_venv_path}/bin/python3.8",
                                    "./manage.py",
                                ) + cmd,
                                cwd=cls.BACKEND_DIR,
                                env=env)

    @classmethod
    def tearDownClass(cls):
        cls.bot_process.kill()
        cls.check_matches_process.kill()
        cls._stop_database()

    # Could not use setUp standard methods!
    # When the telegram client is created there, the client hangs on sending messages, surprisingly!
    @asynccontextmanager
    async def _create_telegram_client(self, client_number: int = 1) -> TelegramClient:
        telegram_client = TelegramClient(
            StringSession(self.clients[client_number - 1]['session_str']),
            self.clients[client_number - 1]['api_id'],
            self.clients[client_number - 1]['api_hash'],
            sequential_updates=True,
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
    async def _create_conversation(self, client_number: int = 1) -> Conversation:
        telegram_client_context_manager = self._create_telegram_client(client_number)
        telegram_client = await telegram_client_context_manager.__aenter__()
        conversation_context_manager = telegram_client.conversation(self.test_bot_username, timeout=10)
        conversation = await conversation_context_manager.__aenter__()
        await sleep(0.5)  # A hack recommended at https://shallowdepth.online/posts/2021/12/end-to-end-tests-for-telegram-bots/

        yield conversation

        await conversation_context_manager.__aexit__(None, None, None)
        await telegram_client_context_manager.__aexit__(None, None, None)
