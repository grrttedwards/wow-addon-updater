# wow-addon-updater

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

_Supporting retail, classic, tbc, and wrath addons!_

[![Build Status](https://github.com/grrttedwards/wow-addon-updater/workflows/Build%20and%20test%20wow-addon-updater/badge.svg?branch=master)](https://github.com/grrttedwards/wow-addon-updater/actions?query=workflow%3A%22Build+and+test+wow-addon-updater%22+branch%3Amaster)

# Downloading
The best way to get the latest stable code is to head to the [Latest Releases page](https://github.com/grrttedwards/wow-addon-updater/releases/latest), or checking out the `master` branch.

If you're feeling adventurous, you can also download the latest (possibly unstable) `develop` branch.

# First-time setup

## Dependencies
- [Python](https://www.python.org/) 3.7.4+.
Basically, any new version of Python.

## Python module dependencies
- [requests](https://pypi.org/project/requests/), for making HTTP requests
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), for HTML document parsing
- [cloudscraper](https://pypi.org/project/cloudscraper/), for bypassing Curse's bot-detection measures

You should already have `pip` included with your Python installation.
This is the default package manager for Python.
You can check by running `pip --version` on the command line.
If it's not there, download the latest version of Python for your platform, and check the box during installation to include `pip`.

It's recommended you manage the dependencies with [`pipenv`](https://github.com/pypa/pipenv). All you need to do is run the following on the command line to install `pipenv` and the dependencies:

```bash
cd wow-addon-updater/
pip install pipenv
pipenv install
```

The packages will be automagically installed by `pipenv` to a local virtual environment.

## Taking updates

If the utility reports that there are updates available from this repo, simply extract the new version into the directory where you store the previous version. Be careful not to stomp on any input or configuration files that you would like to save (e.g. `config.ini`, `addons.txt`, or `installed.ini`)

# Running the utility

After performing the setup steps, you can run the executable scripts by clicking either:
 - `run_Windows.bat` for Windows or 
 - `run_MacLinux.sh` for other platforms.

To run directly from the command line, use `pipenv run`:
```bash
pipenv run python -m updater [-c FILE]
```

Alternatively you can install the python module and have a command named `wow-addon-updater` available:
```bash
pipenv install
pipenv shell
# Make sure you're in a virtual environment! pipenv shell should place you in the venv
# created by `pipenv install` but to be sure you can check with `which python` and
# verify that it's $VIRTUAL_ENV/bin/python

# Either using the distutils method
python setup.py install
# Or using pip
pip install .
# Make sure the command is where we expect
which wow-addon-updater
# This should output $VIRTUAL_ENV/bin/wow-addon-updater

```

More advanced usage includes optionally specifying a configuration file, which is detailed in the next section.

## Issues Downloading Addons?

Occasionally, this utility may fail to download files from sites. This is generally caused by an update to Cloudflare's anti-bot page, and can be fixed by updating the cloudscraper module.

To update this module from the command line, use `pipenv update`:

```bash
cd wow-addon-updater/
pipenv update
```

After updating, re-run the utility to attempt updating the affected addons.

# Configuring the utility

The `config.ini` file is used by default to find where to install the addons to, and where to get the list of addons from.

It requires that some properties be set, if you do not want to use the defaults such as:

- `WoW Addon Location`
    - The WoW application files addon directory
    - (The standard addon location on macOS is `/Applications/World of Warcraft/Interface/AddOns`)
    - (default `= C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns`)

- `Addon List File`
    - A file specifying which addons to install and/or update
    - This file will not exist at first, so you should create `addons.txt` in the same directory as the utility.
    - (default `= addons.txt`)

- `Installed Versions File`
    - A file which tracks your installed addon versions
    - (default `= installed.ini`)

- `Game Version`
    - The game version (`retail`, `classic`, `tbc`, or wrath) that you would like to target for addons 
    - (default `= retail`)

## The `GitHub` Section

To support a higher API request limit, you can add your own [personal GitHub access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to the configuration.
The tool will use the token when making requests to GitHub, reducing the chance of you being rate-limited.

To use, uncomment the section in the `config.ini`, and populate the `token` with a value.
    
## Multiple configurations
The module supports a command-line configuration for maintaining multiple set of addons. For example, a set of addons for retail, and a different set of addons for classic.
To use a different configuration file, specify it with the `--config` flag (or `-c`) e.g.

```bash
pipenv run python -m updater -c my-custom-config.ini
```

# Supported addon hosts
The following hosts are supported as download targets. The URL specified should be to the main page of the addon, or in the case of GitHub, to the root of the repository.

|               | Retail | Classic |
|---------------|--------|---------|
| Curse         | ✅      | ✅       |
| WoWAce        | ✅      | ✅       |
| WoWInterface  | ✅      | ✅       |
| GitHub        | ✅      | ✅       |
| Tukui         | ✅      | ✅       |

# Input file format

Whatever file you use for your list of addons needs to be formatted in a particular way. Each line corresponds to an addon, and the line just needs to contain the link to the page for the addon. For example:

```
https://www.curseforge.com/wow/addons/world-quest-tracker
https://www.curseforge.com/wow/addons/deadly-boss-mods
https://www.curseforge.com/wow/addons/auctionator
https://www.wowinterface.com/downloads/info24005-RavenousMounts.html
https://www.github.com/some-user/some-addon-repo
https://www.tukui.org/classic-addons.php?id=2
```

Each link needs to be the main page for the addon, as shown above.

>**_NOTE_**: Tukui addon URLs should point to the standard download page, and not the git repo.
>i.e. https://www.tukui.org/classic-addons.php?id=2 and not https://git.tukui.org/elvui/elvui|ElvUI

## Addons archives containing subfolders
If you want to extract a subfolder from the default downloaded folder, add a pipe character (`|`) and the name of the subfolder at the end of the line. For example, the ElvUI addon can be added as follows:

```
https://www.github.com/some-user/some-addon-repo|AddOn
```

## Tracking alpha/beta addon releases from Curse
If you are running a beta or PTR version of the game or are simply interested in testing out the latest features of an addon, you may want to update as
alpha or beta versions are released. You can specify which version releases you would like to follow by including `alpha`
or `beta` after a space following the addon URL, see below:

```
https://www.curseforge.com/wow/addons/deadly-boss-mods beta
https://www.curseforge.com/wow/addons/auctionator alpha
```

The updater will follow a hierarchy of release versions, meaning that tracking the "alpha" releases will pull more recent beta or full releases. 
Likewise, following beta will pull newer full release versions while ignoring alpha releases.

Omitting the release option or incorrectly specifying it will automatically fall back on tracking the offical
release track.

# Contributing
Bring up the dev `pipenv` with:
```bash
pipenv install --dev
```

Run tests with:
```bash
pipenv run python -m unittest -v
```

or tests with coverage:
```bash
pipenv run coverage run --source=updater -m unittest -v
pipenv run coverage report
```

Updating deps in setup.py:
```bash
pipenv-setup sync -d
```

1. Submit Issues, PR's, or make general comments
1. ????
1. Profit

# Publishing Releases

This is only available to the repo owner.

1. Commit a new version number to the `VERSION` file
1. Stamp the `CHANGELOG.md`
1. Create a new Release: https://github.com/grrttedwards/wow-addon-updater/releases/new

# Thanks
Shout out to GitHub user [`kuhnertdm`](https://github.com/kuhnertdm) for establishing the original base of this utility, and giving people an alternative to the wasteland of mainstream clients.
