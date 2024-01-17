#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---[Name & Dates]----------------------------------------------------------#
#  Filename ~ config.py                 [Created: 2023-03-28 |  8:35 - AM]  #
#                                       [Updated: 2023-04-10 | 13:27 - PM]  #
# ---[Info]------------------------------------------------------------------#
#  The Python config file of gitpy                                          #
#  Language ~ Python3                                                       #
# ---[Authors]---------------------------------------------------------------#
#  Thomas Pellissier (dedroot)                                               #
# ---[Operating System]------------------------------------------------------#
#  Developed for Linux                                                      #
# ---[License]---------------------------------------------------------------#
#  GNU General Public License v3.0                                          #
#  -------------------------------                                          #
#                                                                           #
#  This program is free software; you can redistribute it and/or modify     #
#  it under the terms of the GNU General Public License as published by     #
#  the Free Software Foundation; either version 2 of the License, or        #
#  (at your option) any later version.                                      #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             #
#  GNU General Public License for more details.                             #
#                                                                           #
#  You should have received a copy of the GNU General Public License along  #
#  with this program; if not, write to the Free Software Foundation, Inc.,  #
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              #
# ---------------------------------------------------------------------------#

import configparser
import os
import platform

# Imports section
import re
import subprocess
import sys
from copy import deepcopy
from time import sleep

from src.util.colors import Color
from src.util.exit_tool import exit_tool

## Third party libraries
from src.util.github_repo import GitHub_Repo
from src.util.help_messages import Help_Messages as HM


# Main
class Configuration:
    """
    The configuration class of GitPy. Where all the variables are stored.
    This class is used to parse all arguments from the 'ars.py' file (The "Arguments"' class).
    """

    # Verbosity level: 1 = executed commands, 2 = executed commands and stdout/stderr,
    # 3 = level 1 + 2 + more information about the execution of Python functions
    verbose = 0
    PROGRAM_NAME = "gitpy"

    # The main version of GitPy
    VERSION = "0.1.0.0"

    # Owner's info
    ## dedroot
    OWNER_EMAIL_dedroot = "thomas.pellissier.pro@proton.me"
    OWNER_DISCORDTAG_dedroot = "dedroot#0141 "

    # The version's message for the -V/--version argument
    version_message = VERSION
    version_message_verbose = (
        """GitPy %s
    \r
    \rCopyright (C) 2021-2023 PSociety™, All rights reserved. By Thomas Pellissier (dedroot)
    \rLicense GPLv3+: GNU GPL version 3 or later <https://www.gnu.org/licenses/gpl-3.0.html>.
    \rThis is free software; you can modify the program and share it as long as the {R}original authors
    \rappears in credit and the program is of the same license{W}.
    \r
    \rThis tool was written by Thomas Pellissier (dedroot)."""
        % VERSION
    )

    # Where GitPy is installed
    DEFAULT_INSTALL_PATH = r"/opt/gitpy/"
    # The News Version Notification's config file
    DEFAULT_NOTIFICATION_CONFIG_FILE_PATH = r"/opt/gitpy/config/new_version_notification.conf"

    # The logs file
    # LOG_FILE_PATH = DEFAULT_INSTALL_PATH + r'logs'

    # The bin directory of GitPy
    BIN_PATH = r"/usr/bin/"

    # The GitPy temporary directory
    TEMP_PATH = r"/tmp/gitpy/"

    # For the environment variables
    ## The GitPy's install path
    gitpy_install_path_env_var_name = "GITPY_INSTALL_PATH"
    gitpy_install_path_env_var_value = DEFAULT_INSTALL_PATH
    ## The News Version Notification's config file
    gitpy_notification_config_file_env_var_name = "GITPY_NOTIFICATION_CONFIG_FILE_PATH"
    gitpy_notification_config_file_env_var_value = DEFAULT_NOTIFICATION_CONFIG_FILE_PATH

    # Github's repo settings
    REPO_URL = "https://github.com/dedroot/GitPy"
    REPO_CLONE_URL = "https://github.com/dedroot/GitPy.git"
    REPO_BRANCH = "master"
    REPO_MASTER_BRANCH = "master"
    REPO_METADATA_URL = "https://raw.githubusercontent.com/dedroot/GitPy/master/metadata.json"
    REPO_CHANGELOG_URL = "https://github.com/dedroot/GitPy/blob/master/src/docs/CHANGELOG.md"
    REPO_ISSUES_URL = "https://github.com/dedroot/GitPy/issues"
    ## The GitPy's version from the Github's repo. Will be attributed by the 'compare_version'
    ## function from the 'github_repo.py' file
    REPO_VERSION = None

    @classmethod
    def load_arguments(cls, pwd):
        from src.__main__ import GitPy
        from src.args import Arguments

        """
            Load argument and parse them to the specific function.

            Arguments:
                pwd (str): The current working directory
        """

        cls.pwd = pwd

        # Get the arguments
        args = Arguments.get_arguments()

        # if the user run gitpy with -q/--quiet and -v/--verbose options
        if args.quiet and args.verbose:
            Color.pl(GitPy.Banner())
            print()

            Color.pl(
                "  {!} The {G}-q{W}/{G}--quiet{W} and {G}-v{W}/{G}--verbose{W} option are not compatible together."
            )
            exit_tool(1, pwd=cls.pwd)

        # Set the verbosity level
        if args.verbose == 1:
            cls.verbose = 1

        if args.verbose == 2:
            cls.verbose = 2

        if args.verbose == 3:
            cls.verbose = 3

        # Parse the arguments
        cls.parse_informations_args(args)
        cls.first_args_to_parse(args)
        cls.parse_main_args(args, pwd)
        cls.parse_installation_args(args, pwd)
        cls.parse_repo_args(args)
        cls.parse_miscellaneous_args(args, pwd)
        # cls.parse_test_args(args)

    @classmethod
    def first_args_to_parse(cls, args):
        from src.__main__ import GitPy

        """
            Parse the first arguments that should be parsed before the others.

            Arguments:
                args (object): The arguments object
        """
        if args.install_path == "0":
            Color.pl(GitPy.Banner())
            print()
            Color.pl("  {!} You must specify a path where GitPy will be installed.")
            exit_tool(1, pwd=cls.pwd)

    # -------------------- [ MAIN ARGUMENTS ] -------------------- #
    @classmethod
    def parse_main_args(cls, args, pwd):
        """
        Parse all main arguments.

        Arguments:
            args (object): The arguments object
            pwd (str): The current working directory
        """
        if args.console:
            Color.pl("  {-} Starting the GitPy's console...")
            sleep(1)
            # Call the main console of GitPy
            from src.core.console import Main_Console

            Main_Console(pwd=pwd)

        if args.cli:
            # Color.pl('  {!} The GitPy\'s CLI is not available yet.')
            # exit_tool(1,pwd=cls.pwd)

            from src.core.cli_console import CLI_Console

            CLI_Console(pwd=pwd)

    # -------------------- [ INSTALLATION ARGUMENTS ] -------------------- #
    @classmethod
    def parse_installation_args(cls, args, pwd):
        """
        Parse all installation arguments

        Arguments:
            args (object): The arguments object
            pwd (str): The current working directory
        """
        if args.install:
            from src.core.installer import entry_point as Installer

            Installer(args, pwd=pwd)

        if args.uninstall:
            from src.core.uninstaller import entry_point as Uninstaller

            Uninstaller(args=args, pwd=pwd)

    # -------------------- [ REPO ARGUMENTS ] -------------------- #
    @classmethod
    def parse_repo_args(cls, args):
        """
        Parse all repo arguments

        Arguments:
            args (object): The arguments object
        """
        if args.check_repo:
            from src.core.send_email import send_email

            send_email()

        if args.unsub:
            config = configparser.ConfigParser()
            INSTALL_PATH = os.environ[cls.gitpy_install_path_env_var_name]
            NOTIF_CONFIG_FILE_PATH = INSTALL_PATH + "src/config/new_version_notification.conf"
            config.read(NOTIF_CONFIG_FILE_PATH)

            # Obtient la liste de toutes les sections dans le fichier de configuration
            sections = config.sections()

            # Vérifie si le fichier de configuration contient des sections
            if len(sections) == 0:
                Color.pl("  {!} The configuration file does not contain any sections.")
            else:
                Color.pl("  {*} Here are the sections of the configuration file :")
                for i, section in enumerate(sections):
                    Color.pl("  {D}[{W}{SB2}%s{W}{D}]{W} %s" % (i + 1, section))
                # Demande à l'utilisateur de sélectionner une section à supprimer
                selection = input(Color.s("  {*} Enter the number of the section you wish to delete :  "))

                # Vérifie si l'utilisateur a entré un nombre valide
                try:
                    selection = int(selection)
                    if selection < 1 or selection > len(sections):
                        Color.pl("  {!} Invalid selection. Please enter a valid section number.")
                        return
                except ValueError:
                    Color.pl("  {!} Invalid selection. Please enter a valid section number.")
                    return

                # Supprime la section sélectionnée
                section_to_remove = sections[selection - 1]
                config.remove_section(section_to_remove)

                # Écrit les modifications dans le fichier
                with open(NOTIF_CONFIG_FILE_PATH, "w") as configfile:
                    config.write(configfile)
                Color.pl("  {*} The section %s has been successfully removed." % section_to_remove)

    # -------------------- [ INFORMATIONS ARGUMENTS ] -------------------- #
    @classmethod
    def parse_informations_args(cls, args):
        from src.__main__ import GitPy

        """
            Parse all informations arguments

            Arguments:
                args (object): The arguments object
        """
        if args.help:
            # Show more help for wich command
            # ---------- [ Main options ] ---------- #
            if args.console:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_console())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.cli:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_cli())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---------- [ Installation options ] ---------- #
            if args.install:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_install())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.uninstall:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_uninstall())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.skip_update:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_skip_update())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.offline:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_offline())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.install_path:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_install_path())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---------- [ Output options ] ---------- #
            if args.quiet:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_quiet())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            if args.verbose:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_verbose())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---------- [ Additional options ] ---------- #
            if args.no_confirm:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_no_confirm)
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---------- [ Informations options ] ---------- #
            if args.info:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_info())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.version:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_version())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---------- [ Miscellaneous options ] ---------- #
            if args.update:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_update())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.force_update:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_force_update())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.show_env_var:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_show_env_var())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)
            if args.remove_cache:
                Color.pl(GitPy.Banner())
                Color.pl(HM.option_remove_cache())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

            # ---- No options ---- #
            else:
                Color.pl(GitPy.Banner())
                Color.pl(HM.main_help_msg())
                print()
                GitHub_Repo.compare_version()
                exit_tool(0, pwd=cls.pwd)

        if args.info:
            from src.util.informations import Informations

            Color.pl(GitPy.Banner())
            Color.pl(Informations.print_info())
            print()
            GitHub_Repo.compare_version()
            exit_tool(0, pwd=cls.pwd)

        if args.version:
            if args.verbose:
                Color.pl(cls.version_message_verbose)
            else:
                Color.pl(cls.version_message)
            exit_tool(0, pwd=cls.pwd)

    # -------------------- [ MISCELLANEOUS ARGUMENTS ] -------------------- #
    @classmethod
    def parse_miscellaneous_args(cls, args, pwd):
        """
        Parse all miscellaneous arguments

        Arguments:
            args (object): The arguments object
            pwd (str): The current working directory
        """
        if args.update:
            from src.core.updater import entry_point as Updater

            Updater(args, pwd=pwd)

        if args.show_env_var:
            # if args.show_env_var == 'install_path':
            if Configuration.verbose > 0:
                try:
                    GITPY_PATH = os.environ[cls.gitpy_install_path_env_var_name]
                    Color.pl("%s=%s" % (cls.gitpy_install_path_env_var_name, GITPY_PATH))

                except KeyError:
                    Color.pl("  {!} GitPy is not installed on this machine.")
                    Color.pl(
                        "  {*} Because the {C}{bold}%s{W} environment variable is not set."
                        % cls.gitpy_install_path_env_var_name
                    )
                    exit_tool(1, pwd=cls.pwd)

            else:
                try:
                    GITPY_PATH = os.environ[cls.gitpy_install_path_env_var_name]
                    Color.pl("%s" % GITPY_PATH)

                except KeyError:
                    Color.pl("  {!} GitPy is not installed on this machine.")
                    Color.pl(
                        "  {*} Because the {C}{bold}%s{W} environment variable is not set."
                        % cls.gitpy_install_path_env_var_name
                    )
                    exit_tool(1, pwd=cls.pwd)

        # if args.show_config:
        #     # Open the file in read mode
        #     with open(cls.CONFIG_FILE_PATH, "r") as config_file:
        #         # Read the file content
        #         content=config_file.read()
        #         # Prompt the file content
        #         Color.pl(content)
        #         # Close the file
        #         content=config_file.close()

        if args.remove_cache:
            from src.util.remove_python_cache import remove_python_cache

            remove_python_cache(pwd=pwd)

    # @classmethod
    # def parse_test_args(cls, args):
    #     from src.util.process import Process
    #     if args.process:
    #         if args.verbose and args.verbose > 1:
    #             cls.verbose = args.verbose
    #         Process.exists(program='pacman')
    #         Process.call(command='pacman --help', shell=True)
    #         Process.call(command='pacman --dasdd', shell=True)
    #         Process.call('git clone https://github.com/dedroot/GitPy.git', shell=True)


class Main_prompt:
    """
    Main prompt class for the GitPy's CLI environment (GitPy's shell).
    """

    original_prompt = prompt = Color.s("{underscore}GitPy{W}> {W}")
    main_prompt_ready = True
    SPACE = "#>SPACE$<#"

    @staticmethod
    def rst_prompt(prompt=prompt, prefix="\r"):
        import gnureadline as global_readline

        Main_prompt.main_prompt_ready = True
        sys.stdout.write(prefix + Main_prompt.prompt + global_readline.get_line_buffer())

    @staticmethod
    def set_main_prompt_ready():
        Main_prompt.main_prompt_ready = True


def print_shadow(msg):
    print(msg)


def chill():
    pass


def clone_dict_keys(_dict):
    clone = deepcopy(_dict)
    clone_keys = clone.keys()
    return clone_keys
