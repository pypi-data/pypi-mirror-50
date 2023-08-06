#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"


import http.client

import urllib.request, urllib.parse, urllib.error
import os
import re
import json
import random
import string
import types
import collections
import subprocess
import time

from .encoding import Encoding
from .encoding import get_mimetype
from .encoding import Log

from . import core_session

BATCH_OFFSET = 1000

class Session(core_session.CoreSession):
    """ Low-level session that mirrors the RESTful API. """

    def __init__(self, host, login, auth, protocol='http'):
        """

        :param host:
        :param login:
        :param auth:
        :param protocol:
        :return:
        """

        core_session.CoreSession.__init__(self,
                                          host,
                                          login,
                                          auth,
                                          protocol=protocol)

    def open_batch(self):
        """

        :return:
        """
        global Log

        _param = 'upload'

        _status, _result = self.execute_api(param=_param)

        if _status >= 400:
            Log.error('cannot create a batch')
            return None

        if 'batchId' not in _result:
            Log.error('bad batch return')
            return None

        _batch_id = _result['batchId']

        return _batch_id

    def close_batch(self, batch_id):
        """

        :return:
        """
        global Log

        _param = 'upload/%s' % batch_id

        _status, _result = self.execute_api(method='DELETE', param=_param)

        if _status >= 400:
            Log.error('cannot delete batch')
            return

        Log.info('batch deleted result=%s', repr(_result))

    def upload_files(self, input_names=None, batch_id=None):
        """

        :param name:
        :param batch:
        :return:
        """
        global Log

        if input_names is None:
            return None, None

        _name_list = []
        if isinstance(input_names, (str,)):
            # Log.debug("encode_properties> files are just file_content %s", files)
            _name_list.append(input_names)
        elif isinstance(input_names, list):
            # Log.debug("encode_properties> files are file_content + files %s", repr(files))
            _name_list = input_names
        else:
            # Log.debug("encode_properties> bad argument for files")
            return None, None

        _names = []
        _sizes = []

        for _file_id, _name in enumerate(_name_list):
            _, _head = os.path.split(_name)
            _size = os.path.getsize(_name)

            Log.info('size=%d', _size)

            _headers = dict()

            _headers['X-File-Name'] = _head
            _headers['X-File-Type'] = get_mimetype(_head)
            _headers['Content-Type'] = 'application/octet-stream'
            _headers['Content-Length'] = _size
            # _headers[u'uploadType'] = "normal"

            _param = 'upload/%s/%d' % (batch_id, BATCH_OFFSET + _file_id)

            _status, _result = self.execute_api(param=_param, headers=_headers, file_name=_name)

            if _status >= 400:
                Log.error('cannot upload file')
                return None, None

            Log.info('after upload file result=%s', repr(_result))

        _param = 'upload/%s' % batch_id

        _status, _result = self.execute_api(method='GET', param=_param, headers=dict())

        if _status >= 400:
            Log.error('cannot upload file')
            return None, None

        Log.info('get batch status result=%s', repr(_result))

        _names = []
        _sizes = []

        for _batch_item in _result:
            _names.append(str(_batch_item['name']))
            _sizes.append(_batch_item['size'])

        # Log.debug('%s %s %s', batch, repr(_sizes), repr(_names))

        return _names, _sizes

    def change_title(self, uid, title):
        """

        :param uid:
        :param title:
        :return:
        """

        _req = requests.ChangeTitle(uid, title)
        return _req.send_request(self)

    def get_document(self, name):
        """
        get the uid of a document from its path
        :param name:
        :return:
        """

        # Log.debug(u'get_document %s', name)
        name = re.sub('^[/]', '', name)
        param = 'path/' + name
        return self.execute_api(method='GET', param=param)

    def encode_properties(self, properties=None, files=None):
        """
        private encoding function for properties and attached files
        first we create an empty dict to receive all forth coming properties

        :param properties:
        :param files:
        :return:
        """
        global Log

        _properties = collections.OrderedDict()

        if properties is not None:
            # add all specified properties
            for _property in properties:
                _value = properties[_property]
                _properties[_property] = _value

        # Because of the Nuxeo conventions, the first item of the 'files' list should be
        # understood as 'file_contents'
        #
        # Thus the first step is to construct file_contents + files
        #

        _file_contents = None
        _files = None

        if files is not None:
            if isinstance(files, (str,)):
                # Log.debug("encode_properties> files are just file_content %s", files)
                _file_contents = files
            elif isinstance(files, list):
                # Log.debug("encode_properties> files are file_content + files %s", repr(files))
                if len(files) > 0:
                    _file_contents = files[0]
                    if len(files) > 1:
                        _files = files[1:]
            else:
                # Log.debug("encode_properties> bad argument for files")
                return None, None

        #
        # We manage all files using the Nuxeo batch. Thus files are uploaded first then
        # batch reference is added in the properties.
        #

        _batch_id = None

        if files is not None:
            _batch_id = self.open_batch()

            if _batch_id is None:
                Log.error('cannot open batch')
                return None, None

            _names, _sizes = self.upload_files(files, batch_id=_batch_id)

            if _names is None:
                Log.error('cannot upload files %s', files)
                self.close_batch(_batch_id)

                return None, None

            Log.info('uploaded: %s %s', _names, _sizes)

        if _file_contents is not None:
            # Log.debug(u'encode_properties> file_contents: batch=%s name=%s size=%s',
            # _batch,
            # _name,
            # _size)

            _mimetype = get_mimetype(_file_contents)

            _blob = collections.OrderedDict([
                ('name', _file_contents),
                ('mime-type', _mimetype),
                ('upload-batch', _batch_id),
                ('upload-fileId', '%d' % BATCH_OFFSET),
                ])

            _properties['file:content'] = _blob

        if _files is not None and len(_files) > 0:

            _file_items = []

            for _index in range(len(_files)):
                _file_name = _names[_index + 1]
                _size = _sizes[_index + 1]

                Log.debug('>>> file=%s index=%d', _file_name, _index + 1)

                _mimetype = get_mimetype(_file_name)

                _blob = collections.OrderedDict([
                    ('name', _file_name),
                    ('length', '%d' % _size),
                    ('mime-type', _mimetype),
                    ('upload-batch', _batch_id),
                    ('upload-fileId', '%d' % (BATCH_OFFSET + _index + 1)),
                    ])

                _file_item = collections.OrderedDict([
                    ('file', _blob),
                    ('filename', _file_name),
                ])

                _file_items.append(_file_item)

            _properties['files:files'] = _file_items

        elif _file_contents is not None:
            _properties['files:files'] = []

        return _properties, _batch_id

    def create_document_with_properties(self,
                                        path,
                                        name,
                                        doc_type,
                                        properties=None,
                                        files=None,
                                        from_uid=None):
        """
         We create a document in one single operation:
          - mandatory args are: path, name, doc_type
          - properties can be added(dc:title, uid:minor_version, dc:description, ...)
          - files: joint files.

        :param path:
        :param name:
        :param doc_type:
        :param properties:
        :param files:
        :param from_uid:
        :return:
        """

        # check arguments

        # Log.debug('create_document_with_properties> %s', repr(properties))

        # if properties and not isinstance(properties, dict):
        #     print("create_document_with_properties> bad argument for properties")
        #     return None, None

        _document_properties, _ = self.encode_properties(properties, files)

        #
        # now all properties are collected and prepared for the POST
        #

        _properties = collections.OrderedDict([
            ('entity-type', 'document'),
            ('name', name),
            # (u'path', path),
            ('type', doc_type),
            ('properties', _document_properties),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        if from_uid is not None:
            _param = 'id/' + from_uid
        else:
            # Log.debug(u'path:%s', repr(path))
            _param = 'path' + path

        # Log.debug(u'data:%s', repr(_properties_enc))
        # Log.debug(u'param:%s', repr(_param))

        _status, _result = self.execute_api(method='POST', data=_properties_enc, param=_param)

        # Log.debug(u'Session::create_document_with_properties> END')

        return _status, _result

    def update_document_with_properties(self,
                                        uid,
                                        title,
                                        doc_type,
                                        properties=None,
                                        files=None):
        """
        this function is similar to the create function, but for updating an existing document.

        :param uid:
        :param title:
        :param doc_type:
        :param properties:
        :param files:
        :return:
        """

        _document_properties, _ = self.encode_properties(properties, files)

        #
        # now all properties are collected and prepared for the POST
        #

        _properties = collections.OrderedDict([
            ('entity-type', 'document'),
            ('type', doc_type),
            ('dc:title', title),
            ('repository', 'default'),
            ('uid', uid),
            ('properties', _document_properties),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        # Log.debug('update_document_with_properties> props: %s', _properties_enc)
        # Log.debug('update_document_with_properties> now execute_api')

        _status, _result = self.execute_api(method='PUT',
                                            param='id/%s' % uid,
                                            data=_properties_enc)
        # Log.debug('update_document_with_properties> status=%s res=',
        # _status,
        # _result[u'versionLabel'])

        # Log.debug(u'Session::update_document_with_properties> END')

        return _status, _result

    def read_document(self, doc_id):
        """
        read the properties of an existing document

        :param doc_id:
        :return:
        """

        return self.execute_api(method='GET', param='id/' + doc_id)

    def get_acls(self, doc_id):
        # /id/{docId}/@acl

        _status, _result = self.execute_api(method='GET', param='id/' + doc_id + '/@acl')

        return _status, _result

    def delete_document(self, doc_id):
        """

        :param doc_id:
        :return:
        """

        return self.execute_api(method='DELETE', param='id/' + doc_id)

    def change_document_state(self, uid, state=''):
        """

        :param uid:
        :param state:
        :return:
        """

        _document_properties = collections.OrderedDict()
        _document_properties['value'] = state

        _properties = collections.OrderedDict()
        _properties['params'] = _document_properties

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        _headers = {
            'Content-Type': 'application/json+nxrequest',
            }

        _param = 'id/' + uid + '/@op/Document.SetLifeCycle'
        _status, _result = self.execute_api(method='POST',
                                            extra_headers=_headers,
                                            data=_properties_enc,
                                            param=_param)

        return _status, _result

    # User category
    def read_user(self, name):
        """
        read the properties of an user account
        :param name:
        :return:
        """

        _param = 'user/%s' % name.encode(Encoding)
        return self.execute_api(method='GET', param=_param)

    def create_user(self,
                    user,
                    first_name=None,
                    last_name=None,
                    email='a@b.c',
                    password='user',
                    company=None):
        """
             Basic creation function the required properties are:
               identifier (generally it's the email
               first name
               name
               email
               password

        :param user:
        :param first_name:
        :param last_name:
        :param email:
        :param password:
        :param company:
        :return:
        """

        _user_properties = collections.OrderedDict([
            ('username', user),
            ])

        if email:
            _user_properties['email'] = email
        if last_name:
            _user_properties['lastName'] = last_name
        if first_name:
            _user_properties['firstName'] = first_name
        if password:
            _user_properties['password'] = password
        if company:
            _user_properties['company'] = company

        _properties = collections.OrderedDict([
            ('entity-type', 'user'),
            ('id', user),
            ('properties', _user_properties),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        return self.execute_api(method='POST', data=_properties_enc, param='user')

    def update_user(self, user,
                    first_name=None,
                    last_name=None,
                    email=None,
                    password=None,
                    company=None,
                    is_inactive=None):
        """

        :param user:
        :param first_name:
        :param last_name:
        :param email:
        :param password:
        :param company:
        :param is_inactive:
        :return:
        """

        # extendedGroups
        # isAdministrator
        # isAnonymous
        # properties
        #   username
        #   first_name
        #   last_name
        #   company
        #   groups: []
        #   password
        #   email

        #   FunctionalDomain
        #   IsInactive

        if not (email or last_name or first_name or password or company or is_inactive):
            return None, None

        _user_properties = collections.OrderedDict([
            ('username', user),
            ])

        if email:
            _user_properties['email'] = email
        if last_name:
            _user_properties['lastName'] = last_name
        if first_name:
            _user_properties['firstName'] = first_name
        if password:
            _user_properties['password'] = password
        if company:
            _user_properties['company'] = company
        if is_inactive:
            _user_properties['IsInactive'] = is_inactive

        _properties = collections.OrderedDict([
            ('entity-type', 'user'),
            ('id', user),
            ('properties', _user_properties),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        _param = 'user/' + user

        return self.execute_api(method='PUT', data=_properties_enc, param=_param)

    def delete_user(self, user):
        """

        :param user:
        :return:
        """

        _param = 'user/' + user

        return self.execute_api(method='DELETE', param=_param)

    def get_users(self, query='*', data=False, max_results=None):
        """
          query all users using a wildcard expression
          this internally get a multipage request and assembles the pages

        :param query:
        :param data:
        :param max_results:
        :return:
        """

        _users = []
        page = 0
        while True:
            param = 'user/search?q=%s&currentPageIndex=%d' % (query, page)

            _, _result = self.execute_api(method='GET', param=param)
            page += 1

            if not _result:
                return _users

            if not 'entries' in _result:
                return _users

            for _entry in _result['entries']:
                if _entry['id'] == '':
                    continue

                if data:
                    _users.append(_entry)
                else:
                    _users.append(_entry['id'])

                # Log.info(_entry[u'id'])

                if max_results is not None and len(_users) >= max_results:
                    break

            Log.info('User entries %d', len(_users))

            if max_results is not None and len(_users) >= max_results:
                break

            if _result['isNextPageAvailable']:
                continue
            else:
                break

        return _users

    def query_document(self, query='select * from Document', data=False, max_docs=None):
        """
         query all users using a wildcard expression
         this internally get a multipage request and assembles the pages

        :param query:
        :param data:
        :return:
        """

        query = query.replace('%', '%25')
        query = query.replace(' ', '%20')

        _docs = []

        _size = 10
        _page = 0

        while True:
            _header = {'Nuxeo-Transaction-Timeout': 3,
                       'X-NXproperties': '*',
                       'X-NXRepository': 'default',
                       'content-type': 'application/json'
                       }

            """
            _param2 = urllib.urlencode({u'query': query,
                                        u'pageSize': _size,
                                        u'maxResults': _size,
                                        u'currentPageIndex': _page})
            """

            _param2 = "query=%s" % query \
                      + '&pageSize=%d' % _size \
                      + '&currentPageIndex=%d' % _page \
                      + '&maxResults=%d' % _size

            _param2 = "query=%s" % query

            _param = 'query?' + _param2

            # Log.info(_param2)
            Log.info(_param)

            _, _result = self.execute_api(method='GET', extra_headers=_header, param=_param)
            _page += 1

            if not _result:
                return _docs

            if not 'entries' in _result:
                return _docs

            for _entry in _result['entries']:
                if _entry['uid'] == '':
                    continue

                if data:
                    _docs.append(_entry)
                else:
                    _docs.append(_entry['uid'])

                # Log.info(_entry[u'uid'])

                if max_docs is not None and len(_docs) >= max_docs:
                    break

            Log.info('Doc entries %d', len(_docs))

            if max_docs is not None and len(_docs) >= max_docs:
                break

            if _result['isNextPageAvailable']:
                continue
            else:
                break

        return _docs

    # Directory category
    def get_dusers(self):
        """
        query the userDirectory
        :return:
        """

        _status, _result = self.execute_api(method='GET', param='directory/userDirectory')
        Log.debug('%s %s', _status, _result)

        if not _result:
            return None

        if not 'entries' in _result:
            return None

        users = []
        for _error in _result['entries']:
            users.append(_error['id'])

        return users

    def get_directory(self, domain):
        """
        query a vocabulary
        :param domain:
        :return:
        """

        _, _result = self.execute_api(method='GET', param='directory/%s' % domain)
        # Log.debug('%s %s', _status, _result)

        if not _result:
            return None

        if not 'entries' in _result:
            return None

        _entries = []
        for _entry in _result['entries']:
            _properties = _entry['properties']
            _entries.append(_properties['id'])

        return _entries

    def add_directory_entry(self, directory, entry):
        """

        :param directory:
        :param entry:
        :return:
        """

        _header = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': '8',
            'X-NXRepository': 'default'
            }

        _dir_properties = collections.OrderedDict([
            ('id', entry),
            ('obsolete', '0'),
            ('ordering', '0'),
            ('label', entry),
            ])

        _properties = collections.OrderedDict([
            ('entity-type', 'directoryEntry'),
            ('directoryName', directory),
            ('properties', _dir_properties),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        _status, _result = self.execute_api(method='POST',
                                            extra_headers=_header,
                                            param='directory/%s' % directory,
                                            data=_properties_enc)

        # Log.debug('%s %s', _status, _result)

        return _status, _result

    # Group category
    def get_groups_intern(self, query='*'):
        """
        this internally get a multipage request and assembles the pages
        query all groups using a wildcard expression
        :param query:
        :return:
        """

        _groups = []
        _page = 0
        while True:
            _header = {
                'Accept': '*/*',
                'Nuxeo-Transaction-Timeout': 8,
                'X-NXRepository': 'default',
                'content-type': 'application/json',
                }

            _param = 'group/search?q=' + query + '&currentPageIndex=%d' % _page

            _, _result = self.execute_api(method='GET', extra_headers=_header, param=_param)
            _page += 1

            # Log.debug('%s %s', query, _status)

            if not _result:
                return _groups

            if not 'entries' in _result:
                return _groups

            _entries = _result['entries']
            for _entry in _entries:
                _groups.append(_entry['groupname'])

            if _result['isNextPageAvailable']:
                continue
            else:
                break

        return _groups

    def get_groups(self, pattern):
        """

        :param pattern:
        :return:
        """

        _url = self.server + '/api/v1/group/search?q=' + pattern
        _curl = 'curl -X GET '
        _auth = self.auth

        _headers = []

        _headers.append('-H "X-NXRepository: default"')
        _headers.append('-H "X-NXDocumentProperties: *"')
        _headers.append('-H "Accept: */*"')
        _headers.append('-H "content-type: application/json"')
        _headers.append('-H "Nuxeo-Transaction-Timeout: 8"')
        _headers.append('-H "Authorization: %s"' % _auth)

        _groups = []

        _page = 0
        while True:
            _cmd = _curl + '"%s&currentPageIndex=%d" ' % (_url, _page) + ' '.join(_headers)
            # Log.debug(_cmd)

            _page += 1

            _theproc = subprocess.Popen(_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
            _out = _theproc.stdout.read()
            _theproc.stdout.close()

            _result = json.loads(_out)

            _entries = _result['entries']
            for _entry in _entries:
                _groups.append(_entry['groupname'])

            if not _result['isNextPageAvailable']:
                break

        return _groups

    def query_document_curl(self, query, max_docs=None, action=None, startpage=None):
        """

        :param pattern:
        :return:
        """

        if max_docs is not None:
            max_docs = int(max_docs)

        if startpage is not None:
            _page = startpage
        else:
            _page = 0

        query = query.replace('%', '%25')
        query = query.replace(' ', '%20')

        _a = '-'

        _size = 10

        _docs = []

        while True:
            print(('next page', _page))

            # query = "SELECT%20*%20FROM%20Document"
            _url = self.server + '/api/v1/query' \
                   + "?query=%s" % query \
                   + '&pageSize=%d' % _size \
                   + '&currentPageIndex=%d' % _page \
                   + '&maxResults=%d' % _size

            _curl = 'curl -X GET '
            _auth = self.auth

            _headers = []

            _headers.append('-H "Nuxeo-Transaction-Timeout: 3"')
            _headers.append('-H "X-NXproperties: *"')
            _headers.append('-H "X-NXRepository: default"')
            _headers.append('-H "content-type: application/json"')
            _headers.append('-H "Authorization: %s"' % _auth)
            _headers.append('-d "null"')

            _cmd = _curl + '"%s" ' % _url + ' '.join(_headers)

            # Log.error('cmd=%s', _cmd)

            _retry = 3
            while True:
                try:
                    _theproc = subprocess.Popen(_cmd,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                shell=True)

                    _out = _theproc.stdout.read()
                    _theproc.stdout.close()
                except:
                    Log.error('curl error %s', _cmd)
                    _retry -= 1
                    time.sleep(10.0)
                    if _retry < 0:
                        exit()

                # Log.info('out=%s', _out)

                try:
                    _result = json.loads(_out)
                    _entries = _result['entries']
                    break
                except:
                    Log.error('==== json.loads %s %d', _out, _retry)
                    _retry -= 1
                    time.sleep(10.0)
                    if _retry < 0:
                        exit()
                    continue

            try:
                _ok = 0
                for _entry in _entries:
                    # Log.error(_entry)

                    if 'facets' in _entry:
                        _facets = _entry['facets']
                        if 'Immutable' in _facets:
                            Log.error('Immutable')
                            continue

                    if 'path' not in _entry or _entry['path'] is None:
                        Log.error('no path')
                        continue

                    # Log.error('add doc %d max=%d', len(_docs), max_docs)
                    _docs.append(_entry)

                    if action is not None:
                        try:
                            action(self, _entry)
                        except:
                            Log.error('user action %s', repr(_entry))

                    if max_docs is not None and len(_docs) > max_docs:
                        break

                # Log.error('End of entry. Good docs=%d len(_docs)=%d', _ok, len(_docs))
                # Log.error('Page done=%d', _page)

                if 'isNextPageAvailable' in _result and _result['isNextPageAvailable']:
                    if max_docs is not None and len(_docs) > max_docs:
                        break

                    _page += 1
                    continue

                break

            except:
                Log.error('no result')
                break

        return _docs

    def create_group(self, group):
        """

        :param group:
        :return:
        """

        _headers = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': '8',
            'X-NXRepository': 'default'
            }

        _member_data = []

        _properties = collections.OrderedDict([
            ('entity-type', 'group'),
            ('groupname', group),
            ##(u'grouplabel', group),
            ('memberUsers', _member_data),
            ('memberGroups', _member_data),
            ])

        _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
        _properties_enc = _properties_enc.strip()

        _status, _ = self.execute_api(method='POST',
                                      extra_headers=_headers,
                                      param='group',
                                      data=_properties_enc)

        # Log.debug('%s %s', _status, _result)

        return _status

    def get_group(self, group):
        """

        :param group:
        :return:
        """

        _headers = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': 8,
            'X-NXRepository': 'default',
            'content-type': 'application/json',
            'fetch.group': 'memberGroups'
            }

        _param = 'group/' + group # + '/@groups'

        _status, _result = self.execute_api(method='GET', extra_headers=_headers, param=_param)

        # Log.debug(_status)

        return _status, _result

    def add_user_to_group(self, group, user):
        """

        :param group:
        :param user:
        :return:
        """

        _headers = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': '8',
            'X-NXRepository': 'default'
            }

        _param = 'group/' + group + '/user/' + user

        _status, _ = self.execute_api(method='POST', extra_headers=_headers, param=_param)

        # Log.debug(_status)

        return _status

    def add_subgroups_to_group(self, group, subgroups):
        for subgroup in subgroups:
            _status = self.add_subgroup_to_group(group, subgroup)

        return _status

    def add_subgroup_to_group(self, group, subgroup):
        """

        :param group:
        :param subgroup:
        :return:
        """

        _status, _result = self.get_group(group)

        _headers = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': '8',
            'X-NXRepository': 'default'
            }

        _subgroups = []
        if 'memberGroups' in _result:
            _subgroups = _result['memberGroups']
        elif 'entries' in _result:
            _subgroups = [e['groupname'] for e in _result['entries']]

        if subgroup not in _subgroups:
            _subgroups.append(subgroup)

            # a = []

            _properties = collections.OrderedDict([
                ('entity-type', 'group'),
                ('groupname', group),
                # (u'grouplabel', group),
                # (u'memberUsers', a),
                ('memberGroups', _subgroups),
                ])

            _properties_enc = json.dumps(_properties, sort_keys=True, encoding=Encoding)
            _properties_enc = _properties_enc.strip()

            _param = 'group/' + group

            _status, _result = self.execute_api(method='PUT',
                                                extra_headers=_headers,
                                                param=_param,
                                                data=_properties_enc)

            # Log.debug(_status)

        return _status

    def delete_group(self, group):
        """

        :param group:
        :return:
        """

        _headers = {
            'Accept': '*/*',
            'Nuxeo-Transaction-Timeout': '8',
            'X-NXRepository': 'default'
            }


        # _group = group.replace('/', '')
        _group = urllib.parse.quote_plus(group)

        _param = 'group/%s' % _group
        # Log.debug(_param)

        _status, _ = self.execute_api(method='DELETE', extra_headers=_headers, param=_param)

        Log.info(_status)

        return _status

    # Private
    def execute_api(self,
                    method='POST',
                    extra_headers=None,
                    headers=None,
                    param='',
                    data=None,
                    file_name=None,
                    domain='api'):
        """

        :param method:
        :param extra_headers:
        :param param:
        :param data:
        :param file_name:
        :param domain:
        :return:
        """

        # Log.debug('#-------execute_api-------')

        if headers is not None:
            _headers = headers
            _headers['Authorization'] = self.auth
        else:
            _headers = {
                'Content-Type': 'application/json',
                'Authorization': self.auth,
                'X-NXDocumentProperties': '*',
            }

            if extra_headers:
                for _header in extra_headers:
                    _headers[_header] = extra_headers[_header]

            if 'content-type' in _headers:
                del _headers['Content-Type']

        _host = self.host
        _port = None
        _hp = _host.split(':')
        if len(_hp) == 2:
            _host = _hp[0]
            _port = _hp[1]

        # Log.debug(_headers)
        # Log.debug('host=%s', _host)
        # Log.debug('port=%s', _port, type(_port))

        if _port is not None:
            _port = int(_port)

        if self.protocol == 'http':
            _connection = http.client.HTTPConnection(_host, _port)
        else:
            _connection = http.client.HTTPSConnection(_host, _port)

        # if param.startswith(u'user/search?q=') or param.startswith(u'query?query='):
        if param.startswith('user/search?q='):
            encoded_param = param
        elif param.startswith('group/search?q='):
            encoded_param = param
        elif param.startswith('query?'):
            encoded_param = param.encode(Encoding)
        elif param.startswith('group/'):
            encoded_param = param
            ## encoded_param = urllib.request.pathname2url(param.encode(Encoding))
        else:
            ### encoded_param = urllib.request.pathname2url(param.encode(Encoding))
            encoded_param = urllib.request.pathname2url(param)

        if domain == 'api':
            url = self.api + encoded_param
        elif domain == 'site':
            url = self.site + encoded_param
        else:
            url = self.root + encoded_param

        if data:
            # data = data.encode(Encoding)
            # Log.debug(u'data=%s', repr(data))
            pass

        # if os.getenv('APIREST') is not None:
        if True:
            Log.debug('APIREST> headers=[%s] url=[%s]param=[%s]data=[%s]',
                      repr(_headers),
                      repr(url),
                      repr(param),
                      repr(data))

        if file_name and data is None:
            data = open(file_name, 'rb')

        try:
            _connection.request(method, url, headers=_headers, body=data)
        except:
            Log.error('execute_api> self.api=%s url=%s param=%s', self.api, repr(url), repr(param))

        if file_name and data is not None:
            data.close()

        resp = _connection.getresponse()
        resp.encoding = Encoding

        # Log.debug(u'status=%d', resp.status)
        # Log.debug(u'reason=%s', repr(resp.reason))

        _status = resp.status

        if resp.status >= 400:
            _response = resp.read()
            Log.debug(_response)
            Log.debug('#-------execute_api END-------')
            return _status, resp.reason

        _headers = resp.getheaders()

        # content_type = resp.getheader(u'content-type')

        _response = resp.read()

        try:
            _result = json.loads(_response)
        except Exception as _error:
            Log.info('json.loads(%s)', _response)
            _result = _response

        # Log.debug('#-------execute_api END-------')
        return _status, _result

