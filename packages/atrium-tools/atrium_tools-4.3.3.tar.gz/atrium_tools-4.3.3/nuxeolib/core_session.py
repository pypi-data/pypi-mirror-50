#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"


import urllib.request, urllib.error, urllib.parse
import os
import re
import json
import mimetypes
import random
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import time

from .encoding import Encoding
from .encoding import Log
from . import error

BATCH_OFFSET = 1000

class CoreSession(object):
    """ Low-level session that mirrors the RESTful API. """

    def __init__(self, host, login='', auth='', protocol='http'):
        """

        :param host:
        :param login:
        :param auth:
        :param protocol:
        :return:
        """

        self.host = host
        self.protocol = protocol
        self.server = '%s://%s/nuxeo' %(self.protocol, self.host)
        self.root = self.server + '/site/automation/'
        self.api = self.server + '/api/v1/'
        self.site = self.server + '/site/api/v1/'
        self.login = login
        self.auth = auth
        self.operations = {}
        self.aliases = {}

        _cookie_processor = urllib.request.HTTPCookieProcessor()
        self.opener = urllib.request.build_opener(_cookie_processor)

        mimetypes.init()

        self.fetch_api()

    def fetch_api(self, show=False):
        """

        :param show:
        :return:
        """

        # show = True

        _headers = {'Authorization': self.auth,}
        _request = urllib.request.Request(self.root, headers=_headers)
        _raw = self.opener.open(_request)
        _response = json.loads(_raw.read())
        self.operations = {}
        self.aliases = {}
        for _operation in _response['operations']:
            self.operations[_operation['id']] = _operation
            if 'aliases' in _operation:
                _aliases = _operation['aliases']
                for _alias in _aliases:
                    self.aliases[_alias] = _operation['id']
            if show:
                print(_operation)

    def login_as(self, name):
        """

        :param name:
        :return:
        """

        return self._execute('Auth.LoginAs', name=name)

    def create(self, ref, doc_type, name=None, properties=None):
        """

        :param ref:
        :param doc_type:
        :param name:
        :param properties:
        :return:
        """

        # Log.debug(u'ref=%s type=%s name=%s', ref, doc_type, name)
        return self._execute('Document.Create', input_param='doc:' + ref,
                             type=doc_type, name=name, properties=properties)

    def update(self, ref, properties=None):
        """

        :param ref:
        :param properties:
        :return:
        """

        return self._execute('Document.Update', input_param='doc:' + ref,
                             properties=properties)

    def checkout(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.CheckOut', input_param='doc:' + ref)

    def checkin(self, ref, version='minor', comment=''):
        """

        :param ref:
        :param version:
        :param comment:
        :return:
        """

        if version != 'minor' and version != 'major':
            return None
        return self._execute('Document.CheckIn',
                             input_param='doc:' + ref,
                             context=True,
                             version=version,
                             comment=comment)

    def checkoutin(self, ref, version='minor', comment=''):
        """

        :param ref:
        :param version:
        :param comment:
        :return:
        """

        if version != 'minor' and version != 'major':
            return None
        return self._execute('restCheckInCheckOut',
                             input_param='doc:' + ref,
                             context=True,
                             versionType=version,
                             versionComment=comment)

    def create_tree_snapshot(self, ref, version='minor'):
        """

        :param ref:
        :param version:
        :return:
        """

        version = version.lower()
        if version != 'minor' and version != 'major':
            return None

        version = version.upper()

        _ = self._execute('Document.CreateTreeSnapshot',
                          input_param='doc:' + ref,
                          versioning_option=version)

        _result = self._execute('Document.Save', input_param='doc:' + ref)

        return _result

    def create_version(self, ref, increment='Minor', save_document=True):
        """

        :param ref:
        :param increment:
        :param save_document:
        :return:
        """

        if increment != 'Minor' and increment != 'Major':
            return None
        return self._execute('Document.CreateVersion',
                             input_param='doc:' + ref,
                             increment=increment,
                             saveDocument=save_document)

    def set_property(self, ref, xpath, value):
        """

        :param ref:
        :param xpath:
        :param value:
        :return:
        """

        return self._execute('Document.SetProperty', input_param='doc:' + ref,
                             xpath=xpath, value=value)

    def add_property_item(self, ref, xpath, value):
        """

        :param ref:
        :param xpath:
        :param value:
        :return:
        """

        return self._execute('DocumentMultivaluedProperty.addItem', input_param='doc:' + ref,
                             xpath=xpath, value=value)

    def remove_property_item(self, ref, xpath, index=None):
        """

        :param ref:
        :param xpath:
        :param value:
        :return:
        """

        return self._execute('Document.RemoveItemFromListProperty', input_param='doc:' + ref,
                             xpath=xpath,
                             index=index)

    def delete(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.Delete', input_param='doc:' + ref)

    def get_children(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.GetChildren', input_param='doc:' + ref)

    def get_parent(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.GetParent', input_param='doc:' + ref)

    def get_versions(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.GetVersions', input_param='doc:' + ref)

    def lock(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.Lock', input_param='doc:' + ref)

    def unlock(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Document.Unlock', input_param='doc:' + ref)

    def move(self, ref, target, name=None):
        """

        :param ref:
        :param target:
        :param name:
        :return:
        """

        return self._execute('Document.Move', input_param='doc:' + ref,
                             target=target, name=name)

    def publish(self, ref, target):
        """

        :param ref:
        :param target:
        :return:
        """

        return self._execute('Document.Publish', input_param='doc:' + ref,
                             target=target)

    def copy(self, ref, target, name=None):
        """

        :param ref:
        :param target:
        :param name:
        :return:
        """

        return self._execute('Document.Copy', input_param='doc:' + ref,
                             target=target, name=name)

    def add_permission(self, ref, permission, user, acl='local'):
        """

        :param ref:
        :param permission:
        :param user:
        :param acl:
        :return:
        """

        return self._execute('Document.AddPermission', input_param='doc:' + ref,
                             permission=permission,
                             user=user,
                             acl=acl)

    def remove_permission(self, ref, permission, user, acl='local'):
        """

        :param ref:
        :param permission:
        :param user:
        :param acl:
        :return:
        """

        return self._execute('Document.RemovePermission', input_param='doc:' + ref,
                             permission=permission,
                             user=user,
                             acl=acl)

    def get_relations(self, ref):
        """

        :param ref:
        :return:
        """

        outgoing = 'true'

        status = self._execute('Relations.GetRelations',
                               input_param='doc:' + ref,
                               predicate='http://purl.org/dc/terms/References',
                               outgoing=outgoing)

        # Log.info('get_relations> ref=%s', ref)

        if 'entries' not in status:
            raise error.GetError
            return None

        return status['entries']

    def delete_relation(self, source, destination):
        """
        This will be implemented only in Nuxeo versions > 5.8
        :param source:
        :param destination:
        :return:
        """

        _outgoing = 'true'

        _status = self._execute('Relations.DeleteRelation',
                                input_param='doc:' + source,
                                object=destination,
                                predicate='http://purl.org/dc/terms/References',
                                outgoing=_outgoing)

        # Log.info('delete_relations> source=%s dest=%s', source, destination)

        return _status

    def create_relation(self, ref, destination):
        """

        :param ref:
        :param destination:
        :return:
        """

        _relations = self.get_relations(ref)
        # Log.debug('create_relations> len(es)=%d', len(_relations))
        if _relations:
            for _relation in _relations:
                Log.debug('create_relations> e[path]=%s %s %s',
                          _relation['path'].encode('utf8'),
                          ref.encode('utf8'),
                          destination.encode('utf8'))
                if _relation['path'] == destination:
                    Log.debug('create_relations> destination already referenced')
                    return _relations

        _outgoing = 'false'

        # let's use a proper predicate.
        # simple implementation: give a string
        # next step use a dedicated Vocabulary
        #   -> use get_directory(self, vocabulary)
        #   then select one value from the result

        return self._execute('Relations.CreateRelation',
                             input_param='doc:' + ref,
                             object=destination,
                             predicate='http://purl.org/dc/terms/References',
                             # predicate=u'est en lien avec',
                             outgoing=_outgoing)

    def tag(self, ref, label, username):
        """

        :param ref:
        :param label:
        :param username:
        :return:
        """

        return self._execute('SetDocumentTag',
                             input_param='doc:' + ref,
                             label=label,
                             username=username)

    def fetch(self, ref):
        """
        These ones are special: no u'input' parameter
        :param ref:
        :return:
        """

        return self._execute('Document.Fetch', value=ref)

    def updateAtriumLocalRolesACL(self, ref):
        """
        These ones are special: no u'input' parameter
        :param ref:
        :return:
        """

        return self._execute('_updateAtriumLocalRolesACL', input_param=ref)

    def AtriumRemoveNegativeACE(self, ref):
        """
        These ones are special: no u'input' parameter
        :param ref:
        :return:
        """

        return self._execute('AtriumRemoveNegativeACE', input_param=ref)

    def principal(self, login=None):
        """

        :param login:
        :return:
        """

        if login:
            # Log.debug(u'login=%s', login)
            return self._execute('NuxeoPrincipal.Get', login=login)
        else:
            # Log.debug(u'no login')
            return self._execute('NuxeoPrincipal.Get')

    def get_user(self, name):
        """

        :param name:
        :return:
        """

        return self._execute('User.Get', login=name)

    def query(self, query, language=None):
        """

        :param query:
        :param language:
        :return:
        """

        # pages = ?q=' + query + u'&currentPageIndex=%d'

        # print("session.query> {}".format(query))

        entries = []

        page_index = 0
        while True:
            result = self._execute('Document.Query',
                                   query=query,
                                   language=language,
                                   currentPageIndex=page_index,
                                   maxResults=10)
            pages = result['numberOfPages']
            ### print(result)
            page_index += 1
            if result['hasError']:
                break

            entries.extend(result['entries'])

            if page_index >= result['pageCount']:
                break
            if not result['isNextPageAvailable']:
                break


        return entries

    # Blob category

    def get_blob(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Blob.Get', input_param='doc:' + ref)

    def get_blobs(self, ref):
        """

        :param ref:
        :return:
        """

        return self._execute('Blob.GetAll', input_param='doc:' + ref)

    # Special case. Yuck:(
    def attach_blob(self, ref, blob):
        """

        :param ref:
        :param blob:
        :return:
        """

        return self._attach_blob(blob, document=ref)

    def _execute(self, command, input_param=None, **params):
        """

        :param command:
        :param input_param:
        :param params:
        :return:
        """

        if 'versioning_option' in params:
            params['versioning option'] = params['versioning_option']
            del params['versioning_option']

        if command in self.aliases:
            command = self.aliases[command]

        self._check_params(command, input_param, params)
        _headers = {
            'Content-Type': 'application/json+nxrequest',
            'Authorization': self.auth,
            'X-NXDocumentProperties': '*',
        }

        _data_dict = dict()
        _data_key = 'params'

        if params:
            if 'context' in params:
                _data_key = 'context'

            _data_dict[_data_key] = {}

            for _key, _value in list(params.items()):
                if _value is None:
                    continue
                if _key == 'properties':
                    _properties = ''
                    for _prop_name, _prop_value in list(_value.items()):
                        _properties += '%s=%s\n' % (_prop_name, _prop_value)
                        # Log.debug(u'filling properties [%s]', s)

                    _data_dict[_data_key][_key] = _properties.strip()
                if _key == 'context':
                    pass
                else:
                    # Log.debug(u'filling param [%s]', repr(_value))
                    _data_dict[_data_key][_key] = _value

        if input_param:
            # Log.debug(u'filling input [%s]', s)
            _data_dict['input'] = input_param

        """
        if u'params' not in _data_dict:
            _data_dict[u'params'] = {}

        if u'context' not in _data_dict:
            _data_dict[u'context'] = {}
        """

        if len(_data_dict) > 0:
            # better keep dictionary sorted
            ## _data = json.dumps(_data_dict, sort_keys=True, encoding=Encoding)
            _data = json.dumps(_data_dict, sort_keys=True)
            ### _data = json.dumps(_data_dict)
            ## _data = urllib.parse.urlencode(_data_dict)
            _data = _data.encode('utf-8')
        else:
            _data = None

        if os.getenv('APIREST') is not None:
            Log.debug('APIREST> headers:[%s] url:[%s] data:[%s]',
                      repr(_headers),
                      self.root + command,
                      repr(_data))

        _request = urllib.request.Request(self.root + command, _data, _headers)
        try:
            _raw_response = self.opener.open(_request)
        except Exception as _error:
            self._handle_error(_error)
            raise

        _info = _raw_response.info()
        _response = _raw_response.read()

        if 'content-type' in _info and _info['content-type'].startswith('application/json'):
            if _response:
                return json.loads(_response)
            else:
                return None
        elif 'content-type' in _info and _info['content-type'].startswith('multipart/mixed'):
            _boundary = _info.typeheader
            _boundary = _boundary.split('boundary=')
            _boundary = _boundary[1]
            _boundary = _boundary.replace('"', '')
            _response_items = _response.split(_boundary)

            _file_descriptions = []

            for _response_item in _response_items:
                _separator = _response_item.strip()
                if _separator == '--':
                    continue
                _response_lines = _response_item.split('\r\n')
                _file_description = dict()

                _filename = ''
                for _response_line in _response_lines:
                    if _response_line.startswith('Content-type: '):
                        _file_description['Content-type'] = \
                            _response_line.replace('Content-type: ', '')
                    elif 'filename="' in _response_line:
                        _filename = re.sub('.*filename=', '', _response_line)
                    elif 'filename=' in _response_line:
                        _filename = re.sub('.*filename=', '', _response_line)
                    elif _filename != '':
                        if _response_line == '':
                            break
                        else:
                            _filename += _response_line

                _filename = _filename.replace('"', '')
                _file_description['filename'] = _filename

                _separator = '\r\n\r\n'
                _marker1 = 'Content-Disposition: attachment; filename=%s%s' % (_filename,
                                                                               _separator)
                _marker2 = 'Content-Disposition: attachment; filename="%s"%s' % (_filename,
                                                                                 _separator)
                if _marker1 in _response_item:
                    _pos = _response_item.index(_marker1) + len(_marker1)
                elif _marker2 in _response_item:
                    _pos = _response_item.index(_marker2) + len(_marker2)
                else:
                    Log.error('bad format')

                _file_description['data'] = _response_item[_pos:-4]

                _file_descriptions.append(_file_description)

            return _response, _file_descriptions
        else:
            return _response, None

    def _attach_blob(self, blob, **params):
        """

        :param blob:
        :param params:
        :return:
        """

        _ref = params['document']
        _filename = os.path.basename(_ref)

        _container = MIMEMultipart('related',
                                   type='application/json + nxrequest',
                                   start='request')

        _params_data = {'params': params}
        _json_data = json.dumps(_params_data, sort_keys=True)
        _json_part = MIMEBase('application', 'json + nxrequest')
        _json_part.add_header('Content-ID', 'request')
        _json_part.set_payload(_json_data)
        _container.attach(_json_part)

        _ctype, _ = mimetypes.guess_type(_filename)
        if _ctype:
            _maintype, _subtype = _ctype.split('/', 1)
        else:
            _maintype, _subtype = 'application', 'binary'

        _blob_part = MIMEBase(_maintype, _subtype)
        _blob_part.add_header('Content-ID', 'input')
        _blob_part.add_header('Content-Transfer-Encoding', 'binary')
        _blob_part.add_header('Content-Disposition',
                              'attachment;filename=%s' % _filename)

        _blob_part.set_payload(blob)
        _container.attach(_blob_part)

        # Create data by hand :(
        _boundary = '====Part=%s=%s===' % (time.time, random.randint(0, 1000000000))
        _content_type = 'multipart/related;boundary="%s";' \
                        'type="application/json+nxrequest";' \
                        'start="request"' % _boundary
        _headers = {'Accept': 'application/json+nxentity, */*',
                    'Authorization': self.auth,
                    'Content-Type': _content_type,
                   }
        _data = '--' + _boundary + '\r\n' \
                      + _json_part.as_string() + '\r\n' \
                      + '--' + _boundary + '\r\n' \
                      + _blob_part.as_string() + '\r\n' \
                      + '--' + _boundary + '--'

        _request = urllib.request.Request(self.root + 'Blob.Attach', _data, _headers)
        try:
            _response = self.opener.open(_request)
        except Exception as _error:
            self._handle_error(_error)
            raise

        _status = _response.read()
        return _status

    def _check_params(self, command, input_param, params):
        """

        :param command:
        :param input_param:
        :param params:
        :return:
        """

        if command.startswith('batch'):
            return
        if command.startswith('_updateAtriumLocalRolesACLRemoveDeniedPermissions'):
            return
        if command.startswith('AtriumRemoveNegativeACE'):
            return
        if command.startswith('Document.Query'):
            return
        if command.startswith('restCheckInCheckOut'):
            return
        if command.startswith('Relations.DeleteRelation'):
            return

        method = self.operations[command]
        required_params = []
        other_params = []
        for param in method['params']:
            if param['required']:
                required_params.append(param['name'])
            else:
                other_params.append(param['name'])

        # Log.debug(required_params)
        # Log.debug(other_params)

        """
        for param in params.keys():
            if not param in required_params \
                and not param in other_params:
                raise Exception(u'Bad param: %s' % param)
        """

        for param in required_params:
            if not param in list(params.keys()):
                raise Exception('Missing param: %s' % param)

    def _handle_error(self, error):
        """

        :param error:
        :return:
        """

        Log.error(error)
        if hasattr(error, 'fp'):
            _detail = error.fp.read()
            try:
                _exc = json.loads(_detail)
                Log.error(_exc['message'])
                Log.error(_exc['stack'])
            except:
                # Error message should always be a JSON message, but sometimes it's not
                Log.error(_detail)


