import argparse
import logging
import sys

import requests

from updater.manager.addon_manager import AddonManager

VERSION_FILE = 'VERSION'
LATEST_VERSION_URL = 'https://github.com/grrttedwards/wow-addon-updater/releases/latest'


class NoTracebackStreamHandler(logging.StreamHandler):
    def handle(self, record):
        info, cache = record.exc_info, record.exc_text
        record.exc_info, record.exc_text = None, None
        try:
            super().handle(record)
        finally:
            record.exc_info = info
            record.exc_text = cache


# configure logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.NOTSET)  # root logger needs to have the lowest level

sh = NoTracebackStreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter('%(message)s'))
sh.addFilter(lambda record: record)
root_logger.addHandler(sh)

fh = logging.FileHandler('addon-updater.log', mode='w', encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)-5s] [%(thread)d] [%(name)s] %(message)s'))
root_logger.addHandler(fh)

logger = logging.getLogger(__name__)


def confirm_exit():
    input("\nPress the Enter key to exit")
    exit(0)


def get_update_message(current_version, latest_version):
    separator = '~' * len(LATEST_VERSION_URL)
    msg = f"A new update ({latest_version}) is available! You have ({current_version}).".center(len(LATEST_VERSION_URL))

    lines = ['\n', separator, msg, LATEST_VERSION_URL, separator]

    return '\n'.join(lines)


def check_version():
    try:
        with open(VERSION_FILE, mode='r') as f:
            current_version = f.read().strip('\n')
        logger.debug(f"Current version: {current_version}")
        # follow the latest release URL and it redirects and returns a URL like
        # https://github.com/grrttedwards/wow-addon-updater/releases/tag/v1.5.1
        latest_version = requests.get(LATEST_VERSION_URL).url.split('/')[-1]
        if current_version != latest_version:
            logger.info(get_update_message(current_version, latest_version))
    except Exception as e:
        logger.exception("Something went wrong finding the latest app version! "
                         "Please report this on GitHub and check for a new release.")


def main():
    parser = argparse.ArgumentParser(description='Update your WoW addons.')
    parser.add_argument('-c', '--config', nargs='?', default='config.ini', type=str, metavar='FILE',
                        help='the file to be used for configuration')
    args = parser.parse_args()

    try:
        AddonManager(args.config).update_all()
    except:
        logger.exception("Something bad happened. Please check the logs.")

    check_version()


if __name__ == "__main__":
    # execute only if run as a script
    main()
