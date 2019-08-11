import packages.requests as requests
import re


# Site splitter

def find_zip_url(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return curse(convert_old_curse_url(addonpage))
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return curse(addonpage)

    # Curse Project
    elif addonpage.startswith('https://wow.curseforge.com/projects/'):
        if addonpage.endswith('/files'):
            # Remove /files from the end of the URL, since it gets added later
            return curse_project(addonpage[:-6])
        else:
            return curse_project(addonpage)

    # WowAce Project
    elif addonpage.startswith('https://www.wowace.com/projects/'):
        if addonpage.endswith('/files'):
            # Remove /files from the end of the URL, since it gets added later
            return wow_ace_project(addonpage[:-6])
        else:
            return wow_ace_project(addonpage)

    # Tukui
    elif addonpage.startswith('https://git.tukui.org/'):
        return tukui(addonpage)

    # Wowinterface
    elif addonpage.startswith('https://www.wowinterface.com/'):
        return wowinterface(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


def get_latest_version(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return get_curse_version(convert_old_curse_url(addonpage))
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return get_curse_version(addonpage)

    # Curse Project
    elif addonpage.startswith('https://wow.curseforge.com/projects/'):
        return get_curse_project_version(addonpage)

    # WowAce Project
    elif addonpage.startswith('https://www.wowace.com/projects/'):
        return get_wow_ace_project_version(addonpage)

    # Tukui
    elif addonpage.startswith('https://git.tukui.org/'):
        return get_tukui_version(addonpage)

    # Wowinterface
    elif addonpage.startswith('https://www.wowinterface.com/'):
        return get_wowinterface_version(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


def get_addon_name(addon_url):
    addon_name = addon_url.replace('https://mods.curse.com/addons/wow/', '')
    addon_name = addon_name.replace('https://www.curseforge.com/wow/addons/', '')
    addon_name = addon_name.replace('https://wow.curseforge.com/projects/', '')
    addon_name = addon_name.replace('https://www.wowinterface.com/downloads/', '')
    addon_name = addon_name.replace('https://www.wowace.com/projects/', '')
    addon_name = addon_name.replace('https://git.tukui.org/', '')
    if addon_name.endswith('/files'):
        addon_name = addon_name[:-6]
    return addon_name


# Curse

def curse(addonpage):
    if '/datastore' in addonpage:
        return curse_datastore(addonpage)
    try:
        page = requests.get(addonpage + '/download')
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        # Will be the index of the first char of the url
        index_of_ziploc = content_string.find('PublicProjectDownload.countdown') + 33
        end_quote = content_string.find('"', index_of_ziploc)  # Will be the index of the ending quote after the url
        return 'https://www.curseforge.com' + content_string[index_of_ziploc:end_quote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def curse_datastore(addonpage):
    try:
        # First, look for the URL of the project file page
        page = requests.get(addonpage)
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        end_of_project_page_url = content_string.find('">Visit Project Page')
        index_of_project_page_url = content_string.rfind('<a href="', 0, end_of_project_page_url) + 9
        project_page = content_string[index_of_project_page_url:end_of_project_page_url] + '/files'

        # Then get the project page and get the URL of the first (most recent) file
        page = requests.get(project_page)
        page.raise_for_status()  # Raise an exception for HTTP errors
        project_page = page.url  # We might get redirected, need to know where we ended up.
        content_string = str(page.content)
        start_of_table = content_string.find('project-file-name-container')
        index_of_ziploc = content_string.find('<a class="button tip fa-icon-download icon-only" href="/',
                                              start_of_table) + 55
        end_of_ziploc = content_string.find('"', index_of_ziploc)

        # Add on the first part of the project page URL to get a complete URL
        end_of_project_page_domain = project_page.find("/", 8)
        project_page_domain = project_page[0:end_of_project_page_domain]
        return project_page_domain + content_string[index_of_ziploc:end_of_ziploc]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def convert_old_curse_url(addonpage):
    try:
        # Curse has renamed some addons, removing the numbers from the URL. Rather than guess at what the new
        # name and URL is, just try to load the old URL and see where Curse redirects us to. We can guess at
        # the new URL, but they should know their own renaming scheme better than we do.
        page = requests.get(addonpage)
        page.raise_for_status()  # Raise an exception for HTTP errors
        return page.url
    except Exception:
        print('Failed to find the current page for old URL "' + addonpage + '". Skipping...\n')
        raise


def get_curse_version(addonpage):
    if '/datastore' in addonpage:
        # For some reason, the dev for the DataStore addons stopped doing releases back around the
        # start of WoD and now just does alpha releases on the project page. So installing the
        # latest 'release' version gets you a version from 2014 that doesn't work properly. So
        # we'll grab the latest alpha from the project page instead.
        return get_curse_datastore_version(addonpage)
    try:
        page = requests.get(addonpage + '/files')
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        index_of_ver = content_string.find(
            '<h3 class="text-primary-500 text-lg">') + 37  # first char of the version string
        end_tag = content_string.find('</h3>', index_of_ver)  # ending tag after the version string
        return content_string[index_of_ver:end_tag].strip()
    except Exception:
        # print('Failed to find version number for: ' + addonpage)
        raise Exception('Failed to find version number for: ' + addonpage)


def get_curse_datastore_version(addonpage):
    try:
        # First, look for the URL of the project file page
        page = requests.get(addonpage)
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        end_of_project_page_url = content_string.find('">Visit Project Page')
        index_of_project_page_url = content_string.rfind('<a href="', 0, end_of_project_page_url) + 9
        project_page = content_string[index_of_project_page_url:end_of_project_page_url]

        # Now just call getCurseProjectVersion with the URL we found
        return get_curse_project_version(project_page)
    except Exception:
        print('Failed to find alpha version number for: ' + addonpage)


# Curse Project

def curse_project(addonpage):
    try:
        # Apparently the Curse project pages are sometimes sending people to WowAce now.
        # Check if the URL forwards to WowAce and use that URL instead.
        page = requests.get(addonpage)
        page.raise_for_status()  # Raise an exception for HTTP errors
        if page.url.startswith('https://www.wowace.com/projects/'):
            return wow_ace_project(page.url)
        return addonpage + '/files/latest'
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def get_curse_project_version(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        if page.status_code == 404:
            # Maybe the project page got moved to WowAce?
            page = requests.get(addonpage)
            page.raise_for_status()  # Raise an exception for HTTP errors
            page = requests.get(page.url + '/files')  # page.url refers to the place where the last one redirected to
            page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        start_of_table = content_string.find('project-file-list-item')
        index_of_ver = content_string.find('data-name="', start_of_table) + 11  # first char of the version string
        end_tag = content_string.find('">', index_of_ver)  # ending tag after the version string
        return content_string[index_of_ver:end_tag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        raise


# WowAce Project

def wow_ace_project(addonpage):
    try:
        return addonpage + '/files/latest'
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def get_wow_ace_project_version(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        start_of_table = content_string.find('project-file-list-item')
        index_of_ver = content_string.find('data-name="', start_of_table) + 11  # first char of the version string
        end_tag = content_string.find('">', index_of_ver)  # ending tag after the version string
        return content_string[index_of_ver:end_tag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        raise


# Tukui

def tukui(addonpage):
    try:
        return addonpage + '/-/archive/master/elvui-master.zip'
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def get_tukui_version(addonpage):
    try:
        response = requests.get(addonpage)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = str(response.content)
        match = re.search(
            r'<div class="commit-sha-group">\\n<div class="label label-monospace">\\n(?P<hash>[^<]+?)\\n</div>',
            content)
        result = ''
        if match:
            result = match.group('hash')
        return result.strip()
    except Exception as err:
        print('Failed to find version number for: ' + addonpage)
        print(err)
        raise


# Wowinterface

def wowinterface(addonpage):
    downloadpage = addonpage.replace('info', 'download')
    try:
        page = requests.get(downloadpage + '/download')
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        index_of_ziploc = content_string.find('Problems with the download? <a href="') + 37  # first char of the url
        end_quote = content_string.find('"', index_of_ziploc)  # ending quote after the url
        return content_string[index_of_ziploc:end_quote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        raise


def get_wowinterface_version(addonpage):
    try:
        page = requests.get(addonpage)
        page.raise_for_status()  # Raise an exception for HTTP errors
        content_string = str(page.content)
        index_of_ver = content_string.find('id="version"') + 22  # first char of the version string
        end_tag = content_string.find('</div>', index_of_ver)  # ending tag after the version string
        return content_string[index_of_ver:end_tag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        raise
