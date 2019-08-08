import configparser
import shutil
import tempfile
import threading
import zipfile
from io import BytesIO
from os import listdir
from os.path import isfile, join

import SiteHandler
import packages.requests as requests

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


class AddonUpdater:
    def __init__(self):
        print('')

        # Read config file
        if not isfile('config.ini'):
            print('Failed to read configuration file. Are you sure there is a file called "config.ini"?\n')
            confirm_exit()

        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            self.WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
            self.INSTALLED_VERS_FILE = config['WOW ADDON UPDATER']['Installed Versions File']
            self.AUTO_CLOSE = config['WOW ADDON UPDATER']['Close Automatically When Completed']
        except Exception:
            print('Failed to parse configuration file. Are you sure it is formatted correctly?\n')
            confirm_exit()

        if not isfile(self.ADDON_LIST_FILE):
            print('Failed to read addon list file. Are you sure the file exists?\n')
            confirm_exit()

        if not isfile(self.INSTALLED_VERS_FILE):
            with open(self.INSTALLED_VERS_FILE, 'w') as newInstalledVersFile:
                newInstalledVers = configparser.ConfigParser()
                newInstalledVers['Installed Versions'] = {}
                newInstalledVers.write(newInstalledVersFile)
        return

    def update(self):
        uberlist = []
        threads = []

        with open(self.ADDON_LIST_FILE, "r") as fin:
            for line in fin:
                threads.append(threading.Thread(target=self.update_addon, args=(line, uberlist)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if self.AUTO_CLOSE == 'False':
            col_width = max(len(word) for row in uberlist for word in row) + 2  # padding
            print("".join(word.ljust(col_width) for word in ("Name", "Iversion", "Cversion")))
            for row in uberlist:
                print("".join(word.ljust(col_width) for word in row), end='\n')
            confirm_exit()

    def update_addon(self, addon, uberlist):
        current_node = []
        addon = addon.rstrip('\n')
        if not addon or addon.startswith('#'):
            return
        if '|' in addon:  # Expected input format: "mydomain.com/myzip.zip" or "mydomain.com/myzip.zip|subfolder"
            subfolder = addon.split('|')[1]
            addon = addon.split('|')[0]
        else:
            subfolder = ''
        addon_name = SiteHandler.get_addon_name(addon)
        latest_version = SiteHandler.get_current_version(addon)
        if latest_version is None:
            latest_version = 'Not Available'
        current_node.append(addon_name)
        current_node.append(latest_version)
        installed_version = self.get_installed_version(addon, subfolder)
        if not latest_version == installed_version:
            print('Installing/updating addon: ' + addon_name + ' to version: ' + latest_version + '\n')
            ziploc = SiteHandler.find_ziploc(addon)
            install_success = self.get_addon(ziploc, subfolder)
            current_node.append(self.get_installed_version(addon, subfolder))
            if install_success and (latest_version is not ''):
                self.set_installed_version(addon, subfolder, latest_version)
        else:
            print(addon_name + ' version ' + latest_version + ' is up to date.\n')
            current_node.append("Up to date")
        uberlist.append(current_node)

    def get_addon(self, ziploc, subfolder):
        if ziploc == '':
            return False
        try:
            r = requests.get(ziploc, stream=True)
            r.raise_for_status()  # Raise an exception for HTTP errors
            zipped = zipfile.ZipFile(BytesIO(r.content))
            self.extract(zipped, subfolder)
            return True
        except Exception:
            print('Failed to download or extract zip file for addon. Skipping...\n')
            return False

    def extract(self, zipped, subfolder):
        if subfolder == '':
            zipped.extractall(self.WOW_ADDON_LOCATION)
        else:  # Pull subfolder out to main level, remove original extracted folder
            try:
                with tempfile.TemporaryDirectory() as tempDirPath:
                    zipped.extractall(tempDirPath)
                    extracted_folder_path = join(tempDirPath, listdir(tempDirPath)[0])
                    subfolder_path = join(extracted_folder_path, subfolder)
                    destination_dir = join(self.WOW_ADDON_LOCATION, subfolder)
                    # Delete the existing copy, as shutil.copytree will not work if
                    # the destination directory already exists!
                    shutil.rmtree(destination_dir, ignore_errors=True)
                    shutil.copytree(subfolder_path, destination_dir)
            except Exception:
                print('Failed to get subfolder ' + subfolder)

    def get_installed_version(self, addonpage, subfolder):
        addon_name = SiteHandler.get_addon_name(addonpage)
        installed_vers = configparser.ConfigParser()
        installed_vers.read(self.INSTALLED_VERS_FILE)
        try:
            if subfolder:
                # Keep subfolder info in installed listing
                return installed_vers['Installed Versions'][addon_name + '|' + subfolder]
            else:
                return installed_vers['Installed Versions'][addon_name]
        except Exception:
            return 'version not found'

    def set_installed_version(self, addonpage, subfolder, currentVersion):
        addon_name = SiteHandler.get_addon_name(addonpage)
        installed_vers = configparser.ConfigParser()
        installed_vers.read(self.INSTALLED_VERS_FILE)
        if subfolder:
            # Keep subfolder info in installed listing
            installed_vers.set('Installed Versions', addon_name + '|' + subfolder, currentVersion)
        else:
            installed_vers.set('Installed Versions', addon_name, currentVersion)
        with open(self.INSTALLED_VERS_FILE, 'w') as installedVersFile:
            installed_vers.write(installedVersFile)


def main():
    check_version()
    AddonUpdater().update()


if __name__ == "__main__":
    # execute only if run as a script
    main()
