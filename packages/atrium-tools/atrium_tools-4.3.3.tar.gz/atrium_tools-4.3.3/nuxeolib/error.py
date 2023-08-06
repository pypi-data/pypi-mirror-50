#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"


class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class BatchError(Error):
    def __init__(self, msg):
        Error.__init__(self, msg)

class DataBuildError(Error):
    def __init__(self, msg):
        Error.__init__(self, msg)

class GetError(Error):
    def __init__(self, msg):
        Error.__init__(self, msg)
