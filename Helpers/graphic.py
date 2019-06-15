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
    ███████╗██╗██╗     ███████╗\033[91m ██████╗ ██████╗ ███████╗\033[0m
    ██╔════╝██║██║     ██╔════╝\033[91m██╔════╝ ██╔══██╗██╔════╝\033[0m
    █████╗  ██║██║     █████╗  \033[91m██║  ███╗██████╔╝███████╗\033[0m
    ██╔══╝  ██║██║     ██╔══╝  \033[91m██║   ██║██╔═══╝ ╚════██║\033[0m
    ██║     ██║███████╗███████╗\033[91m╚██████╔╝██║     ███████║\033[0m
    ╚═╝     ╚═╝╚══════╝╚══════╝\033[91m ╚═════╝ ╚═╝     ╚══════╝\033[0m \033[95mv0.2
    \033[93m                   Coded by 0blio                   \033[0m
                  \033[94m\033[4mhttps://github.com/0blio\033[0m
    """

def notification (text, type):
    symbol = bcolors.BOLD

    if type == "added":
        symbol += bcolors.GREEN + "+"
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

    print "[" + symbol + "] " + text

def print_overriding (values):
    for value in values:
        print value

        # Back to the previous line
        sys.stdout.write("\033[F")

        # Clear line
        sys.stdout.write("\033[K")
