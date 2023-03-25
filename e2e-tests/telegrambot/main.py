import subprocess
from time import sleep
from typing import Optional

import testing_utils

backend_venv_path: str
bot_process: subprocess.Popen
new_matches_finder_process: subprocess.Popen
match_informer_process: subprocess.Popen
proxy_url: str


def main():
    setup_test_environment()
    # noinspection PyBroadException
    try:
        run_tests()
        NameError
    except BaseException:
        teardown_test_environment()
    else:
        teardown_test_environment()


def setup_test_environment():
    global proxy_url
    proxy_url = _read_dot_env('CRUSHBACK_TELEGRAM_PROXY_URL')
    global backend_venv_path
    backend_venv_path = testing_utils.get_backend_venv_path()
    _start_database()
    _run_backend_manage_command("migrate").communicate()
    global bot_process
    global new_matches_finder_process
    global match_informer_process
    bot_process = _run_backend_manage_command("telegrambot")
    new_matches_finder_process = _run_backend_manage_command("findnewmatches", "--period", str(testing_utils.CHECK_MATCH_PERIOD_SECONDS))
    match_informer_process = _run_backend_manage_command("informmatches", "--period", str(testing_utils.CHECK_MATCH_PERIOD_SECONDS))


def run_tests():
    subprocess.Popen(['pipenv', 'run', 'python', '-m', 'unittest']).communicate()


def teardown_test_environment():
    bot_process.kill()
    new_matches_finder_process.kill()
    match_informer_process.kill()
    _stop_database()


def _start_database():
    subprocess.Popen(["docker-compose", "up", "-d", "database"],
                     cwd=testing_utils.ROOT_DIR).communicate()
    sleep(2)  # Wait for DB to get ready


def _stop_database():
    subprocess.Popen(["docker-compose", "down"],
                     cwd=testing_utils.ROOT_DIR).communicate()


def _clear_database():
    clear_script = subprocess.Popen(["echo",
                                     "from main.models import Crush, User, MatchedRecord;"
                                     "MatchedRecord.objects.all().delete();"
                                     "Crush.objects.all().delete();"
                                     "User.objects.all().delete();"
                                     ], stdout=subprocess.PIPE)
    _run_backend_manage_command("shell", stdin=clear_script.stdout).communicate()
    clear_script.communicate()


def _run_backend_manage_command(*cmd: str, stdin=None) -> subprocess.Popen:
    env = {'CRUSHBACK_TELEGRAM_BOT_TOKEN': _read_dot_env('CRUSHBACK_TELEGRAM_BOT_TOKEN')}
    if proxy_url is not None:
        env['CRUSHBACK_TELEGRAM_PROXY_URL'] = proxy_url
    return subprocess.Popen((
                                f"{backend_venv_path}/bin/python3.8",
                                "./manage.py",
                            ) + cmd,
                            cwd=testing_utils.BACKEND_DIR,
                            stdin=stdin,
                            env=env)


def _read_dot_env(key: str) -> Optional[str]:
    with open("./.env") as env_file:
        for line in env_file:
            if line.startswith(f"{key}="):
                value = line.split('=', maxsplit=1)[1]
                value = value.strip()
                return value


if __name__ == '__main__':
    main()
