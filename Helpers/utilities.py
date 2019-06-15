#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import datetime, time

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

def minutes_between_timestamps (t1, t2):
    difference = t1 - t2 if t1 > t2 else t2 - t1
    return int(round(difference.total_seconds() / 60))
