#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: shame
    Coded by: Michele '0blio' Cisternino
    Version: 0.4

    Description:

        This modules generate different hashed version of the filenames.
        If the user don't specify a specific path to search the file in, it append the generated values to a list of common upload directories.
"""

output = []
common_dirs = []

verbose_message (notification ("Reading a list of common upload directories..", "added", False), verbose)
common_dirs = open("txt/common-directories.txt", "r").read().splitlines()
verbose_message (notification ("%s directories read!" % (str(len(common_dirs))), "added", False), verbose)

# Taking the name and the ext of the file the user uploaded
fname, fext = os.path.splitext(filename)

# Creating a list with the clear-text filename and various filename hashes
verbose_message (notification ("Hashing '%s' in various ways.." % (filename), "added", False), verbose)
hashed_filenames = [o + fext for o in [fname, string_to_md5(fname), string_to_md5(fname + fext), string_to_sha1(fname), string_to_sha256(fname)]]

# Output hashed_filenames
output += hashed_filenames

# If the user specified some custom words to computate
if len(custom_words) > 0:
    verbose_message (notification ("Calculating all the possible combinations of filename using the custom words provided as input", "added", False), verbose)

    # Generate all the possible permutations with the separators
    permutation_items = [fname] + custom_words

    output += zipped_combinations (permutation_items, ["_", "-", "", "."], fext)

# Output common directories + hashed_filenames
if common_dirs != []:
    verbose_message (notification ("Appending generated values to the common upload directories wordlist..", "added", False), verbose)

output += [dir + f for dir in common_dirs for f in output]
