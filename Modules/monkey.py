#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: monkey
    Coded by: Michele '0blio' Cisternino
    Version: 0.1

    Description:

        This module generate a list of combinations by using random numbers generation.
"""

import itertools

output = []
len_number = 4

incremental = True

# Taking the name and the ext of the file the user uploaded
fname, fext = os.path.splitext(filename)

# Creating a list with the clear-text filename and various filename hashes
verbose_message (notification ("Hashing '%s' in various ways.." % (filename), "added", False), verbose)
filename_formats = [fname, string_to_md5(fname), string_to_sha1(fname)]

# Default: generate random numbers by using an incremental value (from 1 to 4)
# TODO: User input to set len_number

# Generate all the possible numbers with incremental cardinality (from 1 to len_number)
numbers = []

if incremental == True:
    counter = 0
    for i in range(1, len_number + 1, 1):
        verbose_message (notification ("Generating all the possible numbers with len %s" % (str(i)), "added", False), verbose)
        for j in itertools.product(range(10), repeat=i):
            numbers.append(''.join(map(str, j)))
            counter += 1

        verbose_message (notification ("Generated numbers: %s." % (str(counter)), "added", False), verbose)
        counter = 0

elif incremental == False:
    verbose_message (notification ("Generating all the possible numbers with len %s" % (str(len_number)), "added", False), verbose)
    for i in itertools.product(range(10), repeat=len_number):
        numbers.append(''.join(map(str, i)))

# Calculating all the possible permutations
verbose_message (notification ("Calculating all possible combinations of filenames, random numbers and custom words provided as input (if any)", "added", False), verbose)
for number in numbers:
    for f in filename_formats:
        output += zipped_combinations ([f, number], ["_", "-", "", "."], fext)
