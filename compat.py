# -*- coding: utf-8 -*-
# Copyright (c) 2019, IgorPrus.  All Rights Reserved.

try:
    strtype = basestring
except NameError:
    strtype = str


def to_s(val):
    try:
        return unicode(val)
    except NameError:
        return str(val)
