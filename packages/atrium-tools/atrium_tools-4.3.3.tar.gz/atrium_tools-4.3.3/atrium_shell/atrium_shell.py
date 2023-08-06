#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"

import sys
sys.path.append("..")

import os
import re
import sys
import codecs
import nuxeolib.tools

DIR_TYPES = ('SectionRoot',
             'Section',
             'AtriumSectionRoot',
             'AtriumSectionBase',
             'AtriumSectionBase',
             'AtriumSectionPublic',
             'DirectionFolder',
             'TplFolder',
             'Projets',
             'Laboratoires',
             'Activites',
             'Projet',
             'Laboratoire',
             'Activite',
             'HiddenFolder',
             'BatchTreatmentSpace')

RIGHTS_SCHEMA = 'AtriumLocalRolesSchema'
RIGHTS = ('Publisher',
          'Approver',
          'Validator',
          'Reader',
          'PublisherSection',
          'LocalAdmin',
          'Writer')
BLOCK = 'BlockInheritance'


class Rights(object):
    def __init__(self, properties):
        self.rights = dict()
        self.block = False
        rights_names = [RIGHTS_SCHEMA + ':' + r for r in RIGHTS]
        block_name = RIGHTS_SCHEMA + ':' + BLOCK
        for p in properties:
            if p in rights_names:
                value = properties[p]
                key = p.split(":")[1]
                self.add(key, value)
            elif p == block_name:
                self.block = properties[p]

    def add(self, key, value):

        """
        if key == "Everything":
            print("???????", key)
        """

        if key == "Read":
            self.add("Reader", value)
        elif key == "ReadWrite":
            self.add("Writer", value)
        else:
            if type(value) == list:
                if len(value) > 0:
                    if key in self.rights:
                        v = self.rights[key]
                        v.extend(value)
                        self.rights[key] = v
                    else:
                        self.rights[key] = value
            else:
                if key in self.rights:
                    v = self.rights[key]
                    v.append(value)
                    self.rights[key] = v
                else:
                    self.rights[key] = [value]

    def __str__(self):
        s = ",".join(["{}={}".format(r, ",".join(self.rights[r])) for r in self.rights])
        if s != "":
            s = "[{}]".format(s)
        return s

def children(session, global_path, uid, depth=0, level=0, here=''):
    """
    Recursive scan of a document hierarchy
    Accumulate knowledge of the hierarchy

    :param session: Atrium session
    :param global_path: Original top path
    :param uid: UID of the current document
    :param depth: depth of the scan
    :param level: running level along the scan
    :param here: running path along the scan
    :return: A structured list of tuples of all hierarchy nodes
    """

    # get basic properties of the current root node
    status, result = session.read_document(uid)

    if status >= 400:
        return None

    ### status_acls, result_acls = session.get_acls(uid)

    properties = result['properties']

    # consider using the title instead of the path properties in case the document has been renamed
    name = result['path']

    if 'dc:title' in properties:
        title = properties['dc:title']
    else:
        print("no title ???")

    if not title is None:
        name = title


    # check if the current node has been blocked to stop inheritance
    block = False
    if RIGHTS_SCHEMA + ':BlockInheritance' in properties:
        block = properties[RIGHTS_SCHEMA + ':BlockInheritance']

    # print('--'*level, 'global_path=', global_path, here, block)

    # query of immediate children
    query = "SELECT ecm:uuid FROM Document WHERE ecm:parentId = '%s' ORDER BY ecm:pos" % (uid)

    nuxeo_entries = session.query(query)

    # construct the current accumulated path
    if here != '':
        here += '/'

    here = here + name

    entries = []

    """
    recursively scan children
        filter out the deleted entries
        extract some the relevant properties into a tuple
            state
            doctype
            name
            uid
    """
    for entry in nuxeo_entries:
        # print('--'*level, entry[u'path'])
        state = entry[u'state']
        doctype = entry[u'type']
        properties = entry['properties']
        name = entry['title']
        uid = entry[u'uid']

        ### print("scanning children doctype={}".format(doctype))

        result_acls = None
        if 'Structure' in doctype:
            status_acls, result_acls = session.get_acls(uid)

        rights = Rights(properties)

        if state == 'deleted':
            continue

        if 'dc:title' in properties:
            title = properties['dc:title']
        else:
            print("no title ???")

        if not title is None:
            name = title

        entries.append((name, state, doctype, uid, here, rights, result_acls))

        # analyze the doc type
        if depth > 0:
            # recursion up to the specified depth
            local_uid = entry[u'uid']
            sub = children(session, global_path,
                           local_uid,
                           depth - 1,
                           level=level + 1,
                           here=here)

            for e in sub:
                entries.append(e)

    return entries


# Global database of node entries
TopAtriumEntry = None


def get_atrium_entry(path):
    """
    Find one entry in the global Database given its path
    :param path:
    :return:
    """
    a1, a2 = os.path.split(path)
    if a1 == '':
        return TopAtriumEntry
    else:
        e = get_atrium_entry(a1)
        if a2 in e.entries:
            return e.entries[a2]
        print('{} is not a child of {}'.format(a2, a1))
        exit()


class AtriumEntry:
    """
    Class of objects storing the graph of node entry in the scanned hierarchy

    """
    def __init__(self, here, name, state, doctype, uid, rights, acls):
        self.here = here
        self.name = name
        self.state = state
        self.doctype = doctype
        self.uid = uid
        self.rights = rights

        self.ace = dict()
        for acl in acls['acl']:
            # we select useful entries
            acl_name = acl['name']
            if acl_name == 'SuperAdminACL' or acl_name == 'inherited' or 'LocalAdmin' in acl_name:
                continue
            if acl_name == 'LocalRolesACL' or acl_name == 'local':
                for entry in acl['ace']:
                    if not entry['granted']:
                        continue
                    key = entry['permission']
                    value = entry['username']
                    self.rights.add(key, value)

        # setup the sub-hierarchy
        self.entries = dict()
        self.parent = None

        if here != '':
            self.install()

    def install(self):
        """
        Install this objec into the node DTB
        :return:
        """
        p = get_atrium_entry(self.here)
        p.entries[self.name] = self
        self.parent = p

    def ls(self, show_rights, prefix=0):
        """
        Recursively show the DTB
        :param prefix:
        :return:
        """

        block = ""
        if self.rights.block:
            block = "[Block]"

        print('{}{}/{} {}'.format("  "*prefix, self.here, self.name, block))

        if show_rights:
            for key in self.rights.rights:
                value = self.rights.rights[key]
                print("{}={}".format(key, ",".join(value)))

        for child_name in self.entries:
            child = self.entries[child_name]
            child.ls(show_rights, prefix=prefix + 1)

    def csv(self, f, prefix=0):
        """
        Recursively fill in a CSV file describing the hierarchy
        :param f:
        :param prefix:
        :return:
        """

        block = ""
        if self.rights.block:
            block = "[Block]"

        here = self.here.replace('/', ';')
        f.write('{};{};{};{};{};{};{}\n'.format(here, self.name, ";"*prefix, self.doctype, self.uid, block, str(self.rights)))

        for child_name in self.entries:
            child = self.entries[child_name]
            child.csv(f, prefix=prefix - 1)

    def rm_acl(self, session, permission, group, uid):

        status, result = session.read_document(uid)

        properties = result['properties']

        xpath = RIGHTS_SCHEMA + ':' + permission
        if xpath in properties:
            value = properties[xpath]
            try:
                index = value.index(group)
                session.remove_property_item(uid, xpath, index=index)
            except ValueError:
                pass

        for child_name in self.entries:
            child = self.entries[child_name]
            child.rm_acl(session, permission, group, child.uid)

    def subs_acl(self, session, permission1, group1, permission2, group2, uid):

        status, result = session.read_document(uid)

        properties = result['properties']

        if permission1 == "%":
            """
            We handle the special case where both permission is wild carded using '%'
            In this case, only the group/user will be considered:
            Then, the ACL will be transformed by keeping the permission as it is and substituting the goup/user
            """
            for prop in properties:
                pre_xpath = RIGHTS_SCHEMA + ':'
                if pre_xpath in prop:
                    value = properties[prop]
                    if type(value) != list:
                        continue

                    try:
                        # print("Try Substituting group {} from property {} (value={}) to {}".format(group1, prop, str(value), group2))
                        index = value.index(group1)
                        print("Substituting group {} from property {} to {} index={}".format(group1, prop, group2, index))
                        session.remove_property_item(uid, prop, index=index)
                        session.add_property_item(uid, prop, group2)
                    except ValueError:
                        pass
        else:
            xpath = RIGHTS_SCHEMA + ':' + permission1
            if xpath in properties:
                value = properties[xpath]
                try:
                    index = value.index(group1)
                    session.remove_property_item(uid, xpath, index=index)
                    session.add_property_item(uid, RIGHTS_SCHEMA + ':' + permission2, group2)
                except ValueError:
                    pass

        for child_name in self.entries:
            child = self.entries[child_name]
            child.subs_acl(session, permission1, group1, permission2, group2, child.uid)


def ls(show_rights):
    TopAtriumEntry.ls(show_rights)


def csv(depth):
    path = TopAtriumEntry.name
    while True:
        path, name = os.path.split(path)
        if name != '':
            break

    with codecs.open('{}.csv'.format(name), 'w', 'windows-1252') as f:
        TopAtriumEntry.csv(f, prefix=depth)


def draw():

    # Create the DOT file
    path = TopAtriumEntry.name
    while True:
        path, name = os.path.split(path)
        if name != '':
            break

    file_name = name
    f = codecs.open('%s.dot' % file_name, 'w', 'windows-1252')
    f.write('digraph G {\n')
    f.write('node[shape=box];\n')
    f.write('  rankdir=LR;\n')

    def draw_entry(f, entry):
        # setup all links between connected nodes

        name = entry.name
        if entry.doctype == 'StructureLaboratoire':
            color = 'azure'
            if entry.rights.block:
                color = 'red'
            f.write('"{}" [shape=box; style=filled; fillcolor={}; label="{}"];\n'.format(name, color, name))
        else:
            f.write('"{}" [shape=ellipse; label="{}"];\n'.format(name, name))

        for child_name in entry.entries:
            child = entry.entries[child_name]
            f.write('"{}" -> "{}";\n'.format(entry.name, child_name))
            draw_entry(f, child)

    draw_entry(f, TopAtriumEntry)

    f.write('}')
    f.close()

    # Creation of the graphical output as a PNG file
    if sys.platform == 'win32':
        dot = '/Install/Graphviz2.38/bin/dot.exe'
    else:
        dot = 'dot'

    cmd = '{} -Gcharset=latin1 -Tpng -o{}.png {}.dot'.format(dot, file_name, file_name)
    print(cmd)
    os.system(cmd)

    """
    cmd = '{} -Gcharset=latin1 -Tcmapx -o{}.cmapx {}.dot'.format(dot, file_name, file_name)
    print(cmd)
    os.system(cmd)
    """

    print('create {}.html file'.format(file_name))

    with codecs.open('{}.html'.format(file_name), 'w', 'windows-1252') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
    
    
        <img src="{}.png" usemap="#G" alt="graphviz graph" />
        '''.format(file_name))

    """
    with codecs.open('{}.cmapx'.format(file_name), 'r', 'windows-1252') as g:
        for line in g:
            description = ''
            m = re.match('(.*href=")(.*)(mailto.*)', line)
            if m is not None:
                p = m.group(2)
                line = m.group(1) + m.group(3)
                if p in descriptions:
                    description = descriptions[p]
                else:
                    print(u'no description pour {}'.format(p))

                if description == '' or description is None:
                    description = u'Ceci est la racine pour {}'.format(p)

                print(u'{}: {}'.format(p, description))
                line = line.replace(u'alt=""', u'alt="{}"'.format(description))

            else:
                print(u'-----no match for {}'.format(line))

            line = line.replace(u"&lt;TABLE&gt;", u'{}'.format(description))
            f.write(line)

    f.write('''
        </body>
        </html>    ''')
    f.close()
    """

def find_from_title(session, path):
    """
    Utility to query a document from its title instead of its path
    We scan upward the hierarchy from the expected path:
    if a path is not understood it might be because the node has been renamed, in which case the
    title no longer matches the "path" properties

    :param session:
    :param path:
    :return:
    """

    status, result = session.get_document(path)

    if status >= 400:
        # print("Path {} not found".format(path))
        # we try looking at upper level path
        p1, p2 = os.path.split(path)

        status, result = find_from_title(session, p1)
        uid = result['uid']
        entries = children(session, p1, uid, depth=0)

        found = False

        for entry in entries:
            name = entry[0]
            if name == p2:
                found = True
                break

        if not found:
            status = 400

    return status, result

def copy(session, from_doc, to_doc):
    print("cp {} to {}".format(from_doc, to_doc))

    root = u"/Atrium"

    status, result = find_from_title(session, root + from_doc)

    if status >= 400:
        print("Path {} not found".format(root + from_doc))
        exit()

    from_uid = result['uid']

    print(status, from_uid)

    status, result = find_from_title(session, root + to_doc)

    if status >= 400:
        print("Path {} not found".format(root + to_doc))
        exit()

    to_uid = result['uid']

    print(status, to_uid)

    session.copy(from_uid, to_uid, name="xxx")


def set_acl(session, permission, group, to_doc):

    print("permission={} group={} to_doc{}".format(permission, group, to_doc))

    if not permission in RIGHTS:
        print("Bad syntax for permission")
        return

    root = u"/Atrium"
    status, result = find_from_title(session, root + to_doc)

    if status >= 400:
        print("Path {} not found".format(root + to_doc))
        exit()

    to_uid = result['uid']

    ### print(status, to_uid)

    session.add_property_item(to_uid, RIGHTS_SCHEMA + ':' + permission, group)

    # session.updateAtriumLocalRolesACL(to_uid)


def rm_acl(session, permission, group, to_doc):

    print("permission={} group={} to_doc{}".format(permission, group, to_doc))

    if not permission in RIGHTS:
        print("Bad syntax for permission")
        return

    root = u"/Atrium"
    status, result = find_from_title(session, root + to_doc)

    if status >= 400:
        print("Path {} not found".format(root + to_doc))
        exit()

    to_uid = result['uid']

    ### print(status, to_uid)

    TopAtriumEntry.rm_acl(session, permission, group, to_uid)


def subs_acl(session, permission1, group1, permission2, group2, to_doc):
    print("permission1={} group1={} permission2={} group2={} to_doc{}".format(permission1, group1, permission2, group2, to_doc))

    extended_rights = RIGHTS + ('%', )

    if not permission1 in extended_rights:
        print("Bad syntax for permission")
        return

    if not permission2 in extended_rights:
        print("Bad syntax for permission")
        return

    if (permission1 == '%' and permission2 != '%') \
            or (permission2 == '%' and permission1 != '%'):
        print("Bad syntax for permission")
        return

    root = u"/Atrium"
    status, result = find_from_title(session, root + to_doc)

    if status >= 400:
        print("Path {} not found".format(root + to_doc))
        exit()

    to_uid = result['uid']

    # print(status, to_uid)

    status = TopAtriumEntry.subs_acl(session, permission1, group1, permission2, group2, to_uid)

    print(status)


def check_user_or_group(session, identifier):
    # check group or user inside an ACL specifcation

    user_answer = session.get_user(identifier)
    if type(user_answer) == dict and user_answer['uid'] == identifier:
        # print('user is {}'.format(identifier))
        return "USER"

    status, result = session.get_group(identifier)
    if status == 200:
        # print('group is {}'.format(identifier))
        return "GROUP"

    # print('unknown group/user {}'.format(identifier))

    return "UNKNOWN"


if __name__ == '__main__':

    # define the syntax for this application
    syntax = """
    cd    =  str[/]     : Directory courant
    depth =  int[0]     : Profondeur dans l'arborescence
    -draw =             : Produce a graph of the tree
    -csv  =             : Produce a CSV file of the tree
    -ls  =              : simple listing of the tree
    -rights =           : display rights
    user = str[]        : user space
    cp = str[]          : document to copy
    set_acl = str[]     : acl to set (<permission>,<group>)
    rm_acl = str[]      : acl to remove (<permission>,<group>)
    subs_acl = str[]    : acl to substitute (<permission1>,<group1>,<permission2>,<group2>)
    to = str[]          : destination document (cp, set_acl, rm_acl, subs_acl)
    """

    try:
        args = nuxeolib.tools.Arguments(syntax=syntax)
    except:
        print('host=[dev] cd=[]')
        sys.exit()

    login = args.login
    host = args.host

    if args.user != "":
        root = u'/default-domain/UserWorkspaces/' + re.sub('[@_.]', '-', args.user)
    else:
        root = u'/Atrium'

    show_rights = args.rights

    # Connecting to Atrium
    session = nuxeolib.tools.connect(args.host, login)
    login = nuxeolib.tools.Login

    showing = args.ls \
              or args.csv \
              or args.draw \
              or (args.rm_acl != ""  and args.to) \
              or (args.subs_acl != ""  and args.to)

    if showing:
        target = root + args.cd
        depth = int(args.depth)
        if (args.rm_acl != "" and args.to != "") \
                or (args.subs_acl != ""  and args.to):
            target = root + args.to
            depth = 10000

        # Setting up the context from the arguments
        global_path = target

        # Get the parameters for the top document
        status, result = find_from_title(session, global_path)

        if status >= 400:
            print("Path {} not found".format(global_path))
            exit()

        # Scan all children from the top document according to the specified depth
        uid = result['uid']
        properties = result['properties']
        rights = Rights(properties)
        status_acls, result_acls = session.get_acls(uid)

        # Build a hierarchy of AtriumEntries
        TopAtriumEntry = AtriumEntry('', global_path, None, None, uid, rights, result_acls)

        entries = children(session, global_path, uid, depth=depth)

        for entry in entries:
            name = entry[0]
            state = entry[1]
            doctype = entry[2]
            uid = entry[3]
            here = entry[4]
            rights = entry[5]
            status_acls, result_acls = session.get_acls(uid)

            ### print('creating AtriumEntry here={} name={}'.format(here, name))

            AtriumEntry(here, name, state, doctype, uid, rights, result_acls)

    # Manage options
    if args.ls:
        ls(show_rights)
    elif args.csv:
        csv(depth + 1)
    elif args.draw:
        draw()
    elif args.cp != "" and args.to != "":
        copy(session, args.cp, args.to)
    elif args.set_acl != "" and args.to != "":
        try:
            acl = args.set_acl.split(",")
            permission = acl[0]
            group = acl[1]
            if check_user_or_group(session, group) != "UNKNOWN":
                set_acl(session, permission, group, args.to)
            else:
                print("Unknown user/group {}".format(group))
        except:
            print("Syntax error in set_acl=<permission>,<group> to=<where>")
    elif args.rm_acl != "" and args.to != "":
            try:
                acl = args.rm_acl.split(",")
                permission = acl[0]
                group = acl[1]
                rm_acl(session, permission, group, args.to)
            except:
                print("Syntax error in rm_acl=<permission>,<group> to=<where>")
    elif args.subs_acl != "" and args.to != "":
            try:
                acl = args.subs_acl.split(",")
                permission1 = acl[0]
                group1 = acl[1]
                permission2 = acl[2]
                group2 = acl[3]

                if check_user_or_group(session, group2) != "UNKNOWN":
                    subs_acl(session, permission1, group1, permission2, group2, args.to)
                else:
                    print("Unknown user/group {}".format(group2))
            except:
                print("Syntax error in subs_acl=<permission1>,<group1>,<permission2>,<group2> to=<where>")
    else:
        print('unknown command')
