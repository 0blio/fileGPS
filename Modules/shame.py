#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module name: shame
    Coded by: Michele '0blio' Cisternino
    Version: 0.1

    Description:

        This module generate different types of hashes of the filename.
"""

from Helpers.utilities import *

# Taking the name and the ext of the file you uploaded
fname, fext = os.path.splitext(filename)

# Output the filename in clear-text and hashed in various ways
output = [o + fext for o in [fname, string_to_md5(fname), string_to_sha1(fname), string_to_sha256(fname)]]
