# wow-addon-updater

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

[![Build Status](https://travis-ci.com/grrttedwards/wow-addon-updater.svg?branch=master)](https://travis-ci.com/grrttedwards/wow-addon-updater)

## First-time setup

This utility has two dependencies:

* A version of [Python](https://www.python.org/) 3.6+
* The [requests](http://docs.python-requests.org/en/master/) module

The install should be managed by [`pipenv`](https://github.com/pypa/pipenv). All you need to do is run the following:

```bash
cd wow-addon-updater/
pip install pipenv
pipenv install
```

## Running the utility

After performing the setup steps, `pipenv run` is used to execute the utility. To run from the command line, use:
```bash
pipenv run python -m updater
```

## Configuring the utility

The `config.ini` file is used by the utility to find where to install the addons to, and where to get the list of addons from.

The default location in Windows to install the addons to is `C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns`. If this is not the location where you have World of Warcraft installed, you will need to edit `config.ini` to point to your addons folder.

The standard addon location on macOS is `/Applications/World of Warcraft/Interface/AddOns`

The default name of the addon list file is `addons.txt`, but this file will not exist on your PC, so you should either create `addons.txt` in the same location as the utility, or name the file something else and edit "config.ini" to point to the new file.

The `Installed Versions File` property determines where to store the file that keeps track of the current versions of your addons.

The game version that you would like to target addons for must be specified in the `Game Version` property. The two options are `retail` or `classic`.

## Supported addon hosts
The following hosts are supported as download targets. The URL specified should be to the main page of the addon, or in the case of GitHub, to the root of the repository.

|               | Retail | Classic |
|---------------|--------|---------|
| Curse         | ✅      | ✅       |
| WoWAce        | ✅      | ❌ Soon  |
|  WoWInterface | ✅      | ❌ Soon  |
| GitHub        | ✅      | ✅       |
| Tukui         | ✅      | N/A     |

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
