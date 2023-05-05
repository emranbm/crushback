import asyncio
import os
import subprocess
from typing import Optional, Dict, List

ROOT_DIR = "../.."
BACKEND_DIR = f"{ROOT_DIR}/backend/"
CHECK_MATCH_PERIOD_SECONDS = 1
EXCLUDED_SERVICES_FROM_STARTING = ["frontend", "crushback-metrics", "matchfinder"]


async def add_crush(username: str, conversation):
    await conversation.send_message('/addcrush')
    await conversation.get_response()
    await conversation.send_message(f'@{username}')
    await conversation.get_response()


_get_backend_venv_path_cached_value: Optional[str] = None


def get_backend_venv_path():
    global _get_backend_venv_path_cached_value
    if not _get_backend_venv_path_cached_value:
        stdout: bytes = subprocess.check_output(["bash", "-c", "pipenv --venv"],
                                                cwd=BACKEND_DIR,
                                                env={})
        _get_backend_venv_path_cached_value = stdout.decode("utf-8").strip()

    return _get_backend_venv_path_cached_value


def _read_dot_env(key: str) -> Optional[str]:
    with open("./.env") as env_file:
        for line in env_file:
            if line.startswith(f"{key}="):
                value = line.split('=', maxsplit=1)[1]
                value = value.strip()
                return value


def run_backend_manage_command(*cmd: str, stdin=None, additional_env: Optional[Dict[str, str]] = None) -> subprocess.Popen:
    env = {'CRUSHBACK_TELEGRAM_BOT_TOKEN': _read_dot_env('CRUSHBACK_TELEGRAM_BOT_TOKEN')}
    proxy_url = _read_dot_env('CRUSHBACK_TELEGRAM_PROXY_URL')
    if proxy_url is not None:
        env['CRUSHBACK_TELEGRAM_PROXY_URL'] = proxy_url
    if additional_env is not None:
        for k, v in additional_env.items():
            env[k] = v
    return subprocess.Popen((
                                f"{get_backend_venv_path()}/bin/python3.8",
                                "./manage.py",
                            ) + cmd,
                            cwd=BACKEND_DIR,
                            stdin=stdin,
                            env=env)


async def restart_services(additional_env: Optional[Dict[str, str]] = None) -> subprocess.Popen:
    subprocess.Popen(["docker-compose", "down"],
                     cwd=ROOT_DIR).communicate()
    docker_compose_up(additional_env)
    await asyncio.sleep(5)


def docker_compose_up(additional_env: Optional[Dict[str, str]] = None):
    out, _ = subprocess.Popen(["docker-compose", "config", "--services"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              cwd=ROOT_DIR).communicate()
    service_names = out.decode('utf-8').strip().split('\n')
    service_names = [s for s in service_names if s not in EXCLUDED_SERVICES_FROM_STARTING]
    _docker_compose_up(["-d"] + service_names, additional_env)


def _docker_compose_up(args: List[str], additional_env: Optional[Dict[str, str]] = None):
    env = os.environ.copy()
    if additional_env is not None:
        for k, v in additional_env.items():
            env[k] = v
    out, _ = subprocess.Popen(["docker-compose", "config", "--services"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              cwd=ROOT_DIR).communicate()
    subprocess.Popen(["docker-compose", "up"] + args,
                     cwd=ROOT_DIR, env=env).communicate()


def run_matchfinder(additional_env: Optional[Dict[str, str]] = None):
    _docker_compose_up(["matchfinder"], additional_env)


def attribute(*args, **kwargs):
    """Decorator that adds attributes to classes or functions
    for use with the Attribute (-a) plugin.
    """

    def wrap_ob(ob):
        for name in args:
            setattr(ob, name, True)
        for name, value in kwargs.items():
            setattr(ob, name, value)
        return ob

    return wrap_ob


def is_slow(test):
    """
    Tags a test method or class as a slow to be able to filter out from faster tests.
    """
    return attribute(speed="slow")(test)
