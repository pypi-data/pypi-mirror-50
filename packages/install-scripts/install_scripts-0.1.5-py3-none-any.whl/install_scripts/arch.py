"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of install-scripts.

install-scripts is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

install-scripts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with install-scripts.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""


import os
import shutil
from typing import List
from subprocess import Popen
from install_scripts.helper import process_call


def install_packages(packages: List[str]):
    """
    Installs packages on arch linux
    If it's not installed beforehand,
    pacaur will be installed before any other packages
    :param packages: The packages to install
    :return: None
    """

    if not os.path.isfile("/usr/bin/pacaur"):
        process_call(["sudo", "pacman", "-S", "git", "--noconfirm"])
        install_aur_package("https://aur.archlinux.org/auracle-git.git")
        install_aur_package("https://aur.archlinux.org/pacaur.git")

    Popen(["pacaur", "-Syy", "--noconfirm"] + packages).wait()


def install_aur_package(git_url: str):
    """
    Installs an AUR package from a git URL
    :param git_url: The URL of the git repository
    :return: None
    """
    # Make sure git is installed
    process_call(["git", "clone", git_url, "aur-package"])
    os.chdir("aur-package")
    process_call(["makepkg", "-si", "--noconfirm"])
    os.chdir("..")
    shutil.rmtree("aur-package")


def install_essentials(desktop: bool = False):
    """
    Installs essential packages
    :param desktop: Specifies if this is for a desktop system or not
    :return: None
    """
    packages = [
        "git",
        "rsync",
        "curl",
        "wget",
        "python",
        "python-pip",
        "python-setuptools",
        "openssh",
        "sshfs",
        "youtube-dl",
        "unrar"
    ]
    if desktop:
        packages += [
            "firefox",
            "thunderbird",
            "sublime-text-dev",
            "jetbrains-toolbox",
            "nextcloud-client",
            "vlc",
            "eog",
            "evince",
            "libreoffice",
            "gnome-terminal"
        ]

    install_packages(packages)
