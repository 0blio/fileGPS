#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: timebomb
    Coded by: Michele '0blio' Cisternino
    Version: 0.2

    Description:

        This module will do various guesses of possible filenames by using timestamps.
        All the permutations will be calculated, even if you use custom words.
        All the possibile filenames will be calculated in a range of 5 minutes before
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
now = datetime.datetime.now()

# Taking the remote system timestamp
now_remote = get_remote_timestamp (base_url)

timestamps = [now]

# N mins to check before the timestamp
mins = 2

# If difference in minutes between local and remote timestamp is greater than mins add the remote timestamp to computation
if minutes_between_timestamps(now, now_remote) >= mins:
    timestamps.insert(0, now_remote)

# Declaring the possibile filename formats
filename_formats = [fname, string_to_md5(fname), string_to_sha1(fname), string_to_sha256(fname)]

for timestamp in timestamps:

    # Take timestamp of N mins before now
    timestamp_minus_n_mins = timestamp - datetime.timedelta(minutes = mins)

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

                # Computing all the possibile permutations
                all_permutations = list(permutations (permutation_items))

                # Iterate over all generated permutations
                for permutation in all_permutations:

                    # For each separator
                    for separator in ["_", "-", "", "."]:

                        # Separate the current permutation with the current separator
                        result = separator.join(permutation)
                        output.append(result + fext)
                        output.append(string_to_md5(result) + fext)

                # Deleting the actual formatted timestamp
                del permutation_items[-1]

                # Resetting all permutations
                all_permutations = []

        # Subtract one second to the current timestamp
        tmp_timestamp -= datetime.timedelta(seconds=1)
