#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"

import json
from encoding import Encoding
from session import get_mimetype
from encoding import Log
from error import *

import collections

class Requester(object):
    def __init__(self):
        self.method = u'GET'
        self.param = None

    def send_request(self, session):
        self.build(session)

        _data = json.dumps(self.data, encoding=Encoding)
        _data = _data.strip()

        _status, _result = session.execute_api(method=self.method,
                                               param=self.param,
                                               data=_data)

        return _status, _result

class ChangeTitle(Requester):
    def __init__(self, uid, title):
        Requester.__init__(self)
        self.uid = uid
        self.title = title
        self.method = u'PUT'
        self.param = u'id/%s' % uid

    def build(self, session):
        _properties = collections.OrderedDict()
        _properties[u'entity-type'] = u'document'
        _properties[u'uid'] = self.uid
        _properties[u'repository'] = u'default'
        _properties[u'properties'] = collections.OrderedDict([(u'dc:title', self.title)])
        self.data = _properties

