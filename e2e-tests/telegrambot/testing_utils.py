import subprocess

ROOT_DIR = "../.."
BACKEND_DIR = f"{ROOT_DIR}/backend/"
CHECK_MATCH_PERIOD_SECONDS = 1


async def add_crush(username: str, conversation):
    await conversation.send_message('/addcrush')
    await conversation.get_response()
    await conversation.send_message(f'@{username}')
    await conversation.get_response()


def get_backend_venv_path():
    stdout: bytes = subprocess.check_output(["bash", "-c", "pipenv --venv"],
                                            cwd=BACKEND_DIR,
                                            env={})
    return stdout.decode("utf-8").strip()
