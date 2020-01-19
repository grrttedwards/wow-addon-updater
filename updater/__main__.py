import argparse

import requests

from updater.manager.addon_manager import AddonManager

VERSION_FILE = 'VERSION'
LATEST_VERSION_URL = 'https://github.com/grrttedwards/wow-addon-updater/releases/latest'


def confirm_exit():
    input("\nPress the Enter key to exit")
    exit(0)


def get_update_message(version):
    separator = '~' * len(LATEST_VERSION_URL)
    message = f"A new update ({version}) is available! Check it out at".center(len(LATEST_VERSION_URL))

    lines = ['\n', separator, message, LATEST_VERSION_URL, separator]

    return '\n'.join(lines)


def check_version():
    try:
        with open(VERSION_FILE, mode='r') as f:
            current_version = f.read().strip('\n')
        # follow the latest release URL and it redirects and returns a URL like
        # https://github.com/grrttedwards/wow-addon-updater/releases/tag/v1.5.1
        latest_version = requests.get(LATEST_VERSION_URL).url.split('/')[-1]
        if current_version != latest_version:
            print(get_update_message(latest_version))
    except Exception as e:
        print("Something went wrong finding the latest app version! "
              "Please report this on GitHub and check for a new release.")


def main():
    parser = argparse.ArgumentParser(description='Update your WoW addons.')
    parser.add_argument('-c', '--config', nargs='?', default='config.ini', type=str, metavar='FILE',
                        help='the file to be used for configuration')
    args = parser.parse_args()

    AddonManager(args.config).update_all()

    check_version()


if __name__ == "__main__":
    # execute only if run as a script
    main()
