#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"


import mimetypes
import logging
import os

Encoding = 'ISO-8859-1'

def setlog(name=''):
    """
    :param name:
    :return:
    """

    if name == '':
        _log = logging.getLogger(__name__)
    else:
        _log = logging.getLogger(name)

    _handler = logging.StreamHandler()
    _handler.setLevel(logging.DEBUG)
    _formatter = logging.Formatter('%(asctime)s[%(funcName)s] %(levelname)s> %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
    _handler.setFormatter(_formatter)
    _log.addHandler(_handler)

    return _log

Log = setlog()

def get_mimetype(filename):
    """

    :param filename:
    :return:
    """

    _extension = os.path.splitext(filename)[1]
    try:
        _mimetype = mimetypes.types_map[_extension.lower()]
    except KeyError:
        _mimetype = 'application/octet-stream'

    return _mimetype



