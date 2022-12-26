import os
from setuptools import setup

setup(
    name="wow_addon_updater",
    version="v1.7.1",
    description=(
        "This utility provides an alternative to the Twitch/Curse "
        "client for management and updating of addons for World of Warcraft. "
    ),
    author="Garrett Edwards",
    url="https://github.com/grrttedwards/wow-addon-manager",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    packages=["updater", "updater.manager", "updater.site"],
    entry_points={"console_scripts": ["wow-addon-updater = updater.__main__:main"],},
    extras_require={
        "dev": [
            "appdirs==1.4.4",
            "attrs==21.2.0",
            "black==19.10b0; python_version >= '3.6'",
            "cached-property==1.5.2",
            "cerberus==1.3.4",
            "certifi==2021.5.30",
            "chardet==4.0.0",
            "click==8.0.1",
            "colorama==0.4.4",
            "coverage==5.5",
            "distlib==0.3.2",
            "idna==2.10",
            "orderedmultidict==1.0.1",
            "packaging==20.9",
            "pathspec==0.8.1",
            "pep517==0.10.0",
            "pip-shims==0.5.3",
            "pipenv-setup==3.1.1",
            "pipfile==0.0.2",
            "plette[validation]==0.2.3",
            "pyparsing==2.4.7",
            "python-dateutil==2.8.1",
            "regex==2021.4.4",
            "requests==2.25.1",
            "requirementslib==1.5.16",
            "six==1.16.0",
            "toml==0.10.2",
            "tomlkit==0.7.2",
            "typed-ast==1.4.3",
            "urllib3==1.26.5",
            "vistir==0.5.2",
            "wheel==0.38.1",
        ]
    },
    install_requires=[
        "beautifulsoup4==4.9.3",
        "certifi==2021.5.30",
        "chardet==4.0.0",
        "cloudscraper==1.2.58",
        "idna==2.10",
        "pyparsing==2.4.7",
        "requests==2.25.1",
        "requests-toolbelt==0.9.1",
        "soupsieve==2.2.1; python_version >= '3.0'",
        "urllib3==1.26.5",
    ],
    python_requires=">=3.8.0",
)
