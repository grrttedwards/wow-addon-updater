# Changelog

## Unreleased

## v1.10.0 - 11/27/2022
- Added support for addons in the form of GitHub releases, separately from GitHub commits
- Added support for Wrath classic addons from some sources

## v1.9.2 - 08/03/2021
- Fix bug where an entry in `installed.ini` could be zeroed out if there was an error updating the addon
- Remove broken test case where addon was removed from Tukui repository

## v1.9.1 - 06/06/2021
- Bump version of urllib3 for a security update
- Fix Curse site choosing wrong version when game version is Classic (Thanks @cr0ok)

## v1.9.0 - 05/19/2021
- Add support for TBC Classic addons from Curse

## v1.8.1 - 04/09/2021
- Upgrade dependency versions to fix broken Curse addons
- Fix for better support running in WSL
- Fix for the run_Windows.bat file not relying so much on PATH
- Fix the tukui regex that finds the version number to install and record.

## v1.8.0 - 09/09/2020
- Add support for installing as a module and have a command named `wow-addon-updater` available. (Thanks @elebertus)
- Add ability to follow `alpha`, `beta`, or `release` tracks for addons hosted on Curse. (Thanks @amas0)

## v1.7.1 - 04/29/2020
- Fix a regression and actually enable all of the Tukui/ElvUI family addons to work, including both retail and classic.

## v1.7.0 - 04/24/2020
- Fix some bugs, choose a fake useragent that Curse is happy with, support more Tukui addons.

## v1.6.3 - 03/21/2020
- Update cloudscraper version.

## v1.6.2 - 03/11/2020
- Upgrade cloudscraper version and improve internal logging format.

## v1.6.1 - 03/04/2020
- Add current version logging and a broad exception clause in the main method.

## v1.6.0 - 03/04/2020
- Finally start logging exceptions properly. Output should look familiar in the console, but exceptions and detailed debug information is available in a log file.
- Also fixes an issue with curse issuing reCaptcha challenges because cloudscraper was out of date.

## v1.5.2 - 01/19/2020
- Improve the version check to actually check for latest releases and compare a new VERSION file. Should alert users only when a new release has been published, not just any change to master.

## v1.5.1 - 01/19/2020
- Forgot to update changelog for v1.5.0, oops.
- Bring in new versions of dependencies and unblock users of Curse, who has made more breaking anti-scraper changes.

## v1.4.2 - 10/11/2019
- Use a new internal method of fetching GitHub addons which appears to be more reliable, and fails less often.

## v1.4.1 - 10/11/2019
- Fix for an issue involving subfolders and archives that aren't from git (GitHub, ElvUI). For example, you can now correctly extract single subfolders from Curse, etc.

## v1.4.0 - 10/06/2019
- Add support for WowAce classic addons.

## v1.3.0 - 10/05/2019
- Add the ability to use a Windows-style addon directory path when using Windows, but calling the code from within Windows Subsystem for Linux.

## v1.2.2 - 10/05/2019
- Fix for a problem where an existing installed addon can be deleted, and the new extract fails, which essentially deletes the addon from the system.

## v1.2.1 - 09/29/2019
- Relaxed the pattern match for most URLs which may not be prefixed with "www.".

## v1.2.0 - 09/28/2019
- Integrated cfscrape as an anti-measure for Cloudflare bot-detection, for Curse and WoWAce. Node.js is now a requirement for Curse-based sites.

## v1.1.2 - 09/24/2019
- Fix WoWInterface site to accept any characters for the addon name instead of a more rigid regex.

## v1.1.1 - 09/23/2019
- Add message for when Curse is being a jerk and blocking your requests.

## v1.1.0 - 09/03/2019
- Add support for WoWInterface classic addons.

## v1.0 - 08/31/2019
- Add command-line argument for specifying a configuration file. Now multiple independent configurations can be used i.e. one for retail, and one for classic.
- Enhance support for Curse classic-only addons. Now those addons can download if the page only supports one release, and that release is the classic game version.
- Made the version number fetching for ElvUI more robust and human-readable. (v12.34 instead of 8f3ade9), as well as add support for ElvUI classic repo as well.
- Fixed an issue extracting addons that have multiple top-level folders.
- Fixed a folder naming issue with GitHub repository addons.
- Added basic support for Classic addons from Curse.
- Fixed a major problem with subfolder extraction for archives i.e. you can now select folders again from the ElvUI repo!
- Fixed an installation record being added for an addon which really didn't get installed due to a download or unzip failure.
- Added support for any generic GitHub-hosted addon (thanks @Hjaltesorgenfrei)!
- Large internal project refactor. As a result, new commands to install and execute the module. Details in the README.md.
- Took over development of this great dead project. Improved run time by a huge factor (it should run in just a few seconds total, vs. a few seconds PER addon update). Added clickable executables, so users don't have to run python in their terminal. Cleaned up lots of style and refactored some code.

## Legacy Changes
* 8/24/2018 - Added update message to notify if a new version of WoWAddonUpdater is available

* 8/24/2018 - Added subfolder information to installed.txt - Should now allow multiple lines with different subfolders from the same addon

* 8/24/2018 - Added extra error checking for page responses - Should fix some issues with ugly error page HTML text being spit out

* 8/7/2018 - Fixed broken TukUI/ElvUI downloads since they redesigned their site.

* 6/30/2018 - Added license information. This shouldn't really affect anyone's use of or contributions to the project.

* 6/8/2018 - Added support for Tukui repos, as well as an option to extract the subfolder of a mod folder (see changes to Input File Format section below). Thanks to https://github.com/Fezzik for assistance with this!

* 5/20/2018 (My apologies for the wait, have finally finished classes forever) - Fixed various issues with Curse URLs and redirects, added WowAce support, better error handling. MAJOR thanks to https://github.com/zurohki for this!

* 2/27/2018 - More consistent conversion of old Curse URLs. Thanks to https://github.com/zurohki for this!

* 2/27/2018 - Added formatted table of updated addons and added comment support in the in.txt file (Will ignore lines beginning with the hash character #). Thanks to https://github.com/helpfuljohn for this!

* 2/27/2018 - Added support for Curse Projects. Thanks to https://github.com/Delduwath for this!

* 2/27/2018 - Fixed crash if any blank lines in the input file. Thanks to https://github.com/SeamusConnor for this!

* 11/17/2017 - Fixed compatability issues with new CurseForge site. Also backwards-compatible with old URLs still left in the input file. Major thanks to https://github.com/lithium720 for letting me know about this (as I'm currently on an extended break from WoW) and https://github.com/adrien-martin for contributing to the fix.

* 7/2/2017 - Fixed bug that would cause the app to crash after downloading with no previous pip installations (i.e. the import errors)
