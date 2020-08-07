#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_logo ():
    print """
    \033[97m███████╗██╗██╗     ███████╗\033[91m ██████╗ ██████╗ ███████╗\033[0m
    \033[97m██╔════╝██║██║     ██╔════╝\033[91m██╔════╝ ██╔══██╗██╔════╝\033[0m
    \033[97m█████╗  ██║██║     █████╗  \033[91m██║  ███╗██████╔╝███████╗\033[0m
    \033[97m██╔══╝  ██║██║     ██╔══╝  \033[91m██║   ██║██╔═══╝ ╚════██║\033[0m
    \033[97m██║     ██║███████╗███████╗\033[91m╚██████╔╝██║     ███████║\033[0m
    \033[97m╚═╝     ╚═╝╚══════╝╚══════╝\033[91m ╚═════╝ ╚═╝     ╚══════╝\033[0m \033[95m{v0.4}
    \033[93m                   Coded by 0blio                   \033[0m
                  \033[94m\033[4mhttps://github.com/0blio\033[0m

\033[4m\033[1m\033[91mLegal disclaimer\033[0m
Usage of fileGPS for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers are not responsible for any misuse or damage caused by this software.
    """

def notification (text, type, verbose = True):
    symbol = bcolors.BOLD

    if type == "added":
        symbol += bcolors.PINK + "+"
    elif type == "success":
        symbol += bcolors.GREEN + "✓"
    elif type == "removed":
        symbol += bcolors.RED + "-"
    elif type == "notify":
        symbol += bcolors.BLUE + "★"
    elif type == "error":
        symbol += bcolors.RED + "✗"
    elif type == "found":
        symbol += bcolors.RED + "♥"
    elif type == "info":
        symbol += bcolors.YELLOW + "INFO"

    symbol += bcolors.ENDC

    if verbose == True:
        print "[" + symbol + "] " + text
    return "[" + symbol + "] " + text

def verbose_message (text, verbose = False):
    if verbose == True:
        print text

def print_overriding (values):
    for value in values:
        print value

        # Back to the previous line
        sys.stdout.write("\033[F")

        # Clear line
        sys.stdout.write("\033[K")
