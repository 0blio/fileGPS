#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import datetime, time
from graphic import *
from itertools import permutations, chain, izip_longest, product

def string_to_md5 (string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def string_to_sha1 (string):
    m = hashlib.sha1()
    m.update(string)
    return m.hexdigest()

def string_to_sha256 (string):
    m = hashlib.sha256()
    m.update (string)
    return m.hexdigest()

def percentage(part, whole):
    return format(100 * float(part)/float(whole), '.2f')

def timestamp_all_formats (timestamp):
    timestamps = []
    format_strings = ["%Y%m%d%H%M%S", "%d%m%Y%H%M%S", "PHP_TIME"]

    for format_string in format_strings:
        if format_string == "PHP_TIME":
            formatted_string = str(int(time.mktime(timestamp.timetuple())))
        else:
            formatted_string = time.strftime(format_string, timestamp.timetuple())

        timestamps.append(formatted_string)
        timestamps.append(string_to_md5(formatted_string))

    return timestamps

# This function create combinations merging two lists.
def zipped_combinations (a, b, append = "", md5 = False):
    output = []

    for perm in permutations (a):
        for prod in product (b, repeat=len(a) - 1):
            tpls = list(chain.from_iterable(izip_longest(perm, prod, fillvalue='')))
            output.append (''.join(tpls) + append)

            if md5 == True:
                output.append (string_to_md5(''.join(tpls)) + append)

    return output

def minutes_between_timestamps (t1, t2):
    difference = t1 - t2 if t1 > t2 else t2 - t1
    return int(round(difference.total_seconds() / 60))

def question_yn (question):
    while 1:
        try:
            proceed = ""
            proceed = raw_input (question + "? [y/n]: ").lower().replace(" ", "")
            if proceed in ['y', 'n', ""]:
                return proceed
        except KeyboardInterrupt:
            print
            notification ("Stopped\n", "removed")
            exit()
