import subprocess
import sys
from time import sleep
from typing import List

import testing_utils

bot_process: subprocess.Popen
new_matches_finder_process: subprocess.Popen
match_informer_process: subprocess.Popen
proxy_url: str


def main():
    extra_args = []
    if len(sys.argv) > 1:
        extra_args = sys.argv[1:]

    setup_test_environment()
    # noinspection PyBroadException
    try:
        run_tests(extra_args)
    except BaseException:
        print_test_environment_docker_compose_log()
        teardown_test_environment()
        exit(1)
    else:
        teardown_test_environment()


def setup_test_environment():
    testing_utils.docker_compose_up()
    sleep(5)


def print_test_environment_docker_compose_log():
    print("---------------------")
    print("Docker-compose services logs:")
    subprocess.Popen(["docker-compose", "logs"],
                     cwd=testing_utils.ROOT_DIR).communicate()


def run_tests(extra_args: List[str]):
    cmd = ['pipenv', 'run', 'nose2'] + extra_args
    process = subprocess.Popen(cmd)
    process.communicate()
    if process.returncode != 0:
        raise Exception("Tests failed.")


def teardown_test_environment():
    print("Tearing down test environment ...")
    subprocess.Popen(["docker-compose", "down"],
                     cwd=testing_utils.ROOT_DIR).communicate()


def _start_database():
    subprocess.Popen(["docker-compose", "up", "-d", "database"],
                     cwd=testing_utils.ROOT_DIR).communicate()
    sleep(2)  # Wait for DB to get ready


def _stop_database():
    subprocess.Popen(["docker-compose", "down"],
                     cwd=testing_utils.ROOT_DIR).communicate()


if __name__ == '__main__':
    main()
