from os.path import isfile

import requests

from updater.manager.addon_manager import AddonManager

CHANGELOG_URL = 'https://raw.githubusercontent.com/grrttedwards/wow-addon-updater/master/changelog.txt'
CHANGELOG_FILE = 'changelog.txt'
NEW_UPDATE_MESSAGE = 'A new update is available! Check it out at https://github.com/grrttedwards/wow-addon-updater !'


def confirm_exit():
    input('\nPress the Enter key to exit')
    exit(0)


def check_version():
    if isfile(CHANGELOG_FILE):
        downloaded_changelog = requests.get(CHANGELOG_URL).text
        with open(CHANGELOG_FILE, mode='r') as f:
            current_changelog = f.read()
        if downloaded_changelog != current_changelog:
            print(NEW_UPDATE_MESSAGE)


def main():
    check_version()
    AddonManager().update_all()


if __name__ == "__main__":
    # execute only if run as a script
    main()
