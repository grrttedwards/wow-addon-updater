# wow-addon-updater

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

_Now supporting both retail and classic addon management!_

[![Build Status](https://travis-ci.com/grrttedwards/wow-addon-updater.svg?branch=master)](https://travis-ci.com/grrttedwards/wow-addon-updater)

## First-time setup

You must have a version of [Python](https://www.python.org/) 3.6+.

_If you know how to manage Python packages and virtual environments, you can skip this section._

You should already have `pip` included with your Python installation. This is the default package manager for Python.
If not, download the latest version of Python  for your platform, with `pip` bundled.


### Installing the dependencies

This utility has two external dependencies:

- The [requests](https://pypi.org/project/requests/) module, for making HTTP requests
- The [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) module, for HTML document parsing

It's recommended you manage this with [`pipenv`](https://github.com/pypa/pipenv). All you need to do is run the following to install `pipenv` and the dependencies:

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
| WoWAce        | ✅      | ❌ Soon  |
| WoWInterface  | ✅      | ❌ Soon  |
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
```

Each link needs to be the main page for the addon, as shown above.

### Addons archives containing subfolders
If you want to extract a subfolder from the default downloaded folder (typically needed with Tukui addons), add a pipe character (`|`) and the name of the subfolder at the end of the line. For example, the ElvUI addon can be added as follows:

```
https://git.tukui.org/elvui/elvui|ElvUI
```

## Contributing
Bring up the dev `pipenv` with:
```bash
pipenv install --dev
```

Run tests with:
```bash
pipenv run -m unittest -v
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
