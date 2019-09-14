#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: timebomb
    Coded by: Michele '0blio' Cisternino
    Version: 0.4

    Description:

        This module will do various guesses of possible filenames by using timestamps.
        All the permutations will be calculated, even if you use custom words.
        All the possibile filenames will be calculated in a range of N minutes before
        the start of the script.
"""

import os
from itertools import permutations
import datetime, time
from Helpers.utilities import *

output = []

# Taking the name and the ext of the file you uploaded
fname, fext = os.path.splitext(filename)

# Taking system timestamp
verbose_message (notification ("Reading local datetime..", "added", False), verbose)
now = datetime.datetime.now().replace(microsecond=0)
verbose_message (notification ("Local datetime: %s" % (now), "added", False), verbose)

# Taking the remote system timestamp
verbose_message (notification ("Reading target datetime..", "added", False), verbose)
now_remote = get_remote_timestamp (base_url)
verbose_message (notification ("Target datetime: %s" % (now_remote), "added", False), verbose)

timestamps = [now]

# N mins to check before the timestamp
mins = 1

# If difference in minutes between local and remote timestamp is greater than mins add the remote timestamp to computation
if minutes_between_timestamps(now, now_remote) >= mins:
    timestamps.insert(0, now_remote)

# Declaring the possibile filename formats
verbose_message (notification ("Hashing '%s' in various ways.." % (filename), "added", False), verbose)
filename_formats = [fname, fname + fext, string_to_md5(fname), string_to_sha1(fname), string_to_sha256(fname)]

for timestamp in timestamps:

    #verbose_message (notification ("Iterating timestamps up to %s minutes ago.." % (str(mins)), "added", False), verbose)

    # Take timestamp of N mins before now
    timestamp_minus_n_mins = timestamp - datetime.timedelta(minutes = mins)

    verbose_message (notification ("Iterating timestamps from '%s' to '%s' (%s mins)" % (timestamp, timestamp_minus_n_mins, str(mins)), "added", False), verbose)
    verbose_message (notification ("Calculating all possible combinations of filenames, timestamps and custom words provided as input (if any)", "added", False), verbose)

    # Timestamp taken at the start of the script
    tmp_timestamp = timestamp

    # Iterate N minutes before the timestamp taken at the start of the script
    while tmp_timestamp != timestamp_minus_n_mins:
        permutation_items = []

        # If the user defined any custom words add them to the permutation items
        if len(custom_words) > 0:
            permutation_items += custom_words

        # Adding the uploaded filename to permutation items
        for i, filename_format in enumerate(filename_formats):
            # If it is the first iteration the filename has to be inserted in the first place
            if i == 0:
                permutation_items.insert(0, filename_format)

            # Else the filename has to be replaced
            else:
                permutation_items[0] = filename_format

            # Iterate over different timestamp_format
            timestamp_formats = timestamp_all_formats(tmp_timestamp)
            for timestamp_format in timestamp_formats:
                output.append(timestamp_format + fext)

                # Adding the formatted timestamp to the permutation item list
                permutation_items.append(timestamp_format)

                # zipped_combinations (permutation_items, ["_", "-", "", "."], fext)
                output += zipped_combinations (permutation_items, ["_", "-", "", "."], fext, True)

                # Deleting the actual formatted timestamp
                del permutation_items[-1]

        # Subtract one second to the current timestamp
        tmp_timestamp -= datetime.timedelta(seconds=1)
