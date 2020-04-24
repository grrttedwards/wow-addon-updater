# wow-addon-updater

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

_Supporting both retail and classic addons!_

[![Build Status](https://github.com/grrttedwards/wow-addon-updater/workflows/Build%20and%20test%20wow-addon-updater/badge.svg?branch=master)](https://github.com/grrttedwards/wow-addon-updater/actions?query=workflow%3A%22Build+and+test+wow-addon-updater%22+branch%3Amaster)

## Downloading
The best way to get the latest stable code is to head to the [Latest Releases page](https://github.com/grrttedwards/wow-addon-updater/releases/latest), or checking out the `master` branch.

If you're feeling adventurous, you can also download the latest (possibly unstable) `develop` branch.

## First-time setup

### System dependencies
- You must have a version of [Python](https://www.python.org/) 3.7.4+.
Basically, any new version of Python.

### Python module dependencies

You should already have `pip` included with your Python installation.
This is the default package manager for Python.
You can check by running `pip --version` on the command line.
If it's not there, download the latest version of Python for your platform, and check the box during installation to include `pip`.

This utility has three Python module dependencies:

- The [requests](https://pypi.org/project/requests/) module, for making HTTP requests
- The [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) module, for HTML document parsing
- The [cloudscraper](https://pypi.org/project/cloudscraper/) module, for bypassing Curse's bot-detection measures

It's recommended you manage this with [`pipenv`](https://github.com/pypa/pipenv). All you need to do is run the following on the command line to install `pipenv` and the dependencies:

```bash
cd wow-addon-updater/
pip install pipenv
pipenv install
```

The packages will be automagically installed by `pipenv` to a local virtual environment.

## Running the utility

After performing the setup steps, you can run the executable scripts by clicking either:
 - `run_Windows.bat` for Windows or 
 - `run_MacLinux.sh` for other platforms.

To run directly from the command line, use `pipenv run`:
```bash
pipenv run python -m updater [-c FILE]
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

## Configuring the utility

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
    - The game version (either `retail` or `classic`) that you would like to target for addons 
    - (default `= retail`)
    
### Multiple configurations
The module supports a command-line configuration for maintaining multiple set of addons. For example, a set of addons for retail, and a different set of addons for classic.
To use a different configuration file, specify it with the `--config` flag (or `-c`) e.g.

```bash
pipenv run python -m updater -c my-custom-config.ini
```

## Supported addon hosts
The following hosts are supported as download targets. The URL specified should be to the main page of the addon, or in the case of GitHub, to the root of the repository.

|               | Retail | Classic |
|---------------|--------|---------|
| Curse         | ✅      | ✅       |
| WoWAce        | ✅      | ✅       |
| WoWInterface  | ✅      | ✅       |
| GitHub        | ✅      | ✅       |
| Tukui         | ✅      | ✅       |

## Input file format

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

### Addons archives containing subfolders
If you want to extract a subfolder from the default downloaded folder, add a pipe character (`|`) and the name of the subfolder at the end of the line. For example, the ElvUI addon can be added as follows:

```
https://www.github.com/some-user/some-addon-repo|AddOn
```

## Contributing
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

1. Submit Issues, PR's, or make general comments
1. ????
1. Profit

## Thanks
Shout out to GitHub user [`kuhnertdm`](https://github.com/kuhnertdm) for establishing the original base of this utility, and giving people an alternative to the wasteland of mainstream clients.
