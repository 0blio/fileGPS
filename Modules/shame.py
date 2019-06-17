#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: shame
    Coded by: Michele '0blio' Cisternino
    Version: 0.2

    Description:

        This modules generate different hashed version of the filenames.
        It also append the generated values to a list of common upload directories.
"""

output = []

# Taking the list of common directories
common_dirs = open("txt/common-directories.txt", "r").read().splitlines()

# Taking the name and the ext of the file the user uploaded
fname, fext = os.path.splitext(filename)

# Creating a list with the clear-text filename and various filename hashes
hashed_filenames = [o + fext for o in [fname, string_to_md5(fname), string_to_sha1(fname), string_to_sha256(fname)]]

# Output hashed_filenames
output += hashed_filenames

# Output common directories + hashed_filenames
output += [dir + f for dir in common_dirs for f in hashed_filenames]
