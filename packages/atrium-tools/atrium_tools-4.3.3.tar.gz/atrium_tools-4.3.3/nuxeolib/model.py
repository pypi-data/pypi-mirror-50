#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"



import nuxeolib.session

import netrc
import base64


class Client(object):
    def __init__(self, host, login='', password='', auth='', protocol='http'):

        self.host = host
        self.protocol = protocol

        if auth == '':
            if login == '' and password == '':
                secrets = netrc.netrc()
                login, username, password = secrets.authenticators(self.host.split(':')[0])
                login = login.encode("utf-8")
                password = password.encode("utf-8")
            else:
                login = login.encode("utf-8")
                password = password.encode("utf-8")

            self.login = login
            if password != '':
                try:
                    user = self.login + ':'.encode('utf-8') + password
                    enc = base64.b64encode(user)
                    enc2 = enc.decode()
                    self.auth = 'Basic %s' % enc2
                except:
                    print("Cannot b64encode")
                    exit()
        else:
            self.auth = auth

        self.session = None

    def get_session(self):
        """"Returns a low-level session to the server. You probably don't want to use it.
        """
        if not self.session:
            self.session = nuxeolib.session.Session(self.host, login=self.login, auth=self.auth, protocol=self.protocol)
        return self.session

    def get_root(self):
        """Returns the root folder as a Document object.
        """
        return self.get_document("/")

    def get_document(self, path):
        """Returns document at the given path.
        """
        session = self.get_session()
        resp = session.fetch(path)
        return Document(session, resp)


class Document(object):
    def __init__(self, session, property_dict):
        self.session = session
        self._update(property_dict)

    def _update(self, property_dict):
        self.type = property_dict['type']
        self.uid = property_dict['uid']
        self.path = property_dict['path']
        self.title = property_dict['title']
        self.name = self.path.split("/")[-1]
        self.properties = property_dict.get('properties', {})
        self.dirty_properties = {}

    def __getitem__(self, key):
        """Gets a property value using <schema>:<name> as a key.
        """
        if key in self.properties:
            return self.properties[key]
        else:
            return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets a property value using <schema>:<name> as a key. Marks it dirty so it can be saved
        by calling 'save()' (don't forget to do it).
        """
        self.properties[key] = value
        self.dirty_properties[key] = value

    def refresh(self):
        """Refreshes own properties.
        """
        property_dict = self.session.fetch(self.path)
        self._update(property_dict)

    def save(self):
        """Updates dirty (modified) properties.
        """
        if self.dirty_properties:
            property_dict = self.session.update(self.path, self.dirty_properties)
            self._update(property_dict)

    def get_blob(self):
        """Returns the blob (aka content stream) for this document.
        """
        if self.type == "Note":
            # Hack
            return self["note:note"]
        else:
            return self.session.get_blob(self.path)

    def set_blob(self, blob):
        """Sets the blob (aka content stream) for this document.
        """
        if self.type == "Note":
            # Hack
            property_dict = self.session.setProperty(self.path, "note:note", blob)
            self._update(property_dict)
        else:
            return self.session.attach_blob(self.path, blob)

    def get_children(self):
        """Returns children of document as a document.
        """
        property_dicts = self.session.get_children(self.path)['entries']
        return [Document(self.session, property_dict) for property_dict in property_dicts]

    def create(self, name, doc_type):
        """Creates a new document (or folder) object as child of this document.
        """
        child_doc = self.session.create(self.path, doc_type, name)
        return Document(self.session, child_doc)

    def delete(self):
        """Deletes this document (including children).
        """
        self.session.delete(self.path)
