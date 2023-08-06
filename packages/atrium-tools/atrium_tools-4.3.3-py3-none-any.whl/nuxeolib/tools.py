#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
Ce logiciel est régit par la LICENCE DE LOGICIEL LIBRE CeCILL
http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.txt
"""

__author__ = "Chris Arnault"
__license__ = "CeCILL"


def test_tools():
    print('test_tools')


import sys
import nuxeolib.model
import nuxeolib.encoding

Encoding = nuxeolib.encoding.Encoding

import time
import os
import codecs
import re
import smtplib
from email.mime.text import MIMEText
import random
import string
import getpass

DataSpace = '../data'
Login = ''

MailTesting = False


# --------------------------------------------
# Initialise the session according to the host modes: local, dev, prod
def init_session(host='prod', login='', password='', auth=''):
    global Login

    hosts = dict()
    protocoles = dict()

    hosts['prod'] = 'atrium.in2p3.fr'
    hosts['local'] = 'localhost:8080'
    hosts['dev'] = 'atrium-dev.in2p3.fr'
    hosts['pre'] = 'atrium-pre.in2p3.fr'
    hosts['edms'] = 'edms.in2p3.fr'

    protocoles['local'] = 'http'
    protocoles['prod'] = 'https'
    protocoles['dev'] = 'https'
    protocoles['pre'] = 'https'
    protocoles['edms'] = 'https'

    if host not in ['local', 'dev', 'pre', 'prod', 'edms']:
        print('Bad host')
        return None

    client = nuxeolib.model.Client(hosts[host],
                                   protocol=protocoles[host],
                                   login=login,
                                   password=password,
                                   auth=auth)
    Login = client.login

    session = client.get_session()

    return session


# --------------------------------------------
# on top of the init_session function
# permit to enter the hidden password
def connect(host, login='', auth='', password = ''):
    if login != '':
        if auth == '' and password == '':
            password = getpass.getpass()

    session = None

    try:
        session = init_session(host, login=login, password=password, auth=auth)
    except:
        print(('cannot connect to', host))

    return session


# --------------------------------------------
# retreive the actual login
#
def get_login():
    global Login
    return Login


# --------------------------------------------
# convert accented chars
#
def ascii(s):
    # s1 = 'éèçàâêûîôäëüïö'
    # s2 = 'eeeeaaaoooiiiuuuc'

    s1 = ['\xe9', '\xe8', '\xea', '\xe2', '\xf4', '\xe0', '\xfb', '\xb0', '\xee', '\xef',
          '\xce', '\xe7', '\xeb', '\xc7', '\xc9', '\xc8', '\xdc', '\xf6',
          '&#232;', '&#233;', '&#244']
    s2 = ['e', 'e', 'e', 'e', 'o', 'a', 'u', 'o', 'i', 'i', 'i', 'c', 'e', 'c', 'e', 'e', 'u', 'a',
          'e', 'e', 'o']

    c1 = ''
    c2 = ''

    for i in range(len(s1)):
        c1 = s1[i]
        c2 = s2[i]

        if c1 in s:
            s = s.replace(c1, c2)

    return s


# --------------------------------------------
# Deep suppression of a given document (including from the Corbeille)
#
def purge_document(session, path, title='', edms=''):
    path = path.replace("'", "\\'")
    title = title.replace("'", "\\'")

    if title != '':
        query = "SELECT * FROM Document WHERE ecm:path STARTSWITH '%s' AND dc:title='%s'" % (path, title)
    elif edms != '':
        query = 'SELECT * FROM Document WHERE ecm:path STARTSWITH "%s" AND DocumentSchema:EDMS_ID="%s"' % (path, edms)
    else:
        print('Cannot purge: not enough info')
        return

    # print(query)

    entries = session.query(query)

    for entry in entries:
        # print('----------------------')
        # print('uid=%s' % entry['uid'])
        uid = entry['uid']

        if not uid:
            break

        status, result = session.execute_api(method='DELETE', param='id/%s' % uid)
        if status >= 400:
            print('error in purge')


# --------------------------------------------
# get the current time
#
def now():
    return time.asctime(time.localtime(time.time()))


# --------------------------------------------
# manage command line arguments
#  all arguments have the form:
#    key=value
#  or
#    -option
#
# all values are retreived using args.key (string) or args.option (boolean)
# all matched arguments are popped from the arglist
#
# in case of error the expected syntax is printed
#
class Arguments:

    def _help(self, info=''):
        if info != '':
            print(('==> Error: ' + info))
        print(('Syntax for %s:' % sys.argv[0]))
        print(('\n  ' + '\n  '.join(self._help_)))
        sys.exit(0)

    def _analyze_syntax(self):

        default_syntax = """
    host   =* str[prod|pre|dev] :Serveur Nuxeo
    login  =  str[]             :Compte de connexion
    -help  =                     aide
        """
        options = dict()
        params = dict()
        help = []

        syntax = default_syntax + self._syntax_

        if syntax is None:
            return

        lines = syntax.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue

            help.append(line)

            # print(line)

            is_option = line.startswith('-')
            if is_option:
                option = re.sub('^-', '', line)
                option = re.sub('=.*', '', option)
                options[option.strip()] = True
            else:
                items = line.split('=')
                param = items[0].strip()
                param_type = 'str'
                values = [None]
                if len(items) > 1:
                    # * = <properties> : *
                    properties = items[1].split(':')
                    property = properties[0]
                    mandatory = property.startswith('*')
                    property = property.strip()
                    if mandatory:
                        property = property[1:].strip()

                    choice = '[' in property

                    values = None

                    if choice:
                        value_items = property.split('[')
                        param_type = value_items[0].strip()

                        if len(value_items) > 1:
                            value_items = value_items[1]
                            value_items = re.sub('].*', '', value_items)
                            values = [i.strip() for i in value_items.split('|')]

                    else:
                        param_type = property

                params[param] = [param, param_type, values, mandatory]

        self._params_ = params
        self._options_ = options
        self._help_ = help

    def __init__(self, params=None, options=None, syntax=None):
        try:
            self._params_ = dict()
            self._options_ = options
            self._syntax_ = syntax

            self.host = 'local'

            # get params definition either from the syntax specification or from arguments of the __init__ constructor
            if syntax is not None:
                self._analyze_syntax()
            elif params is not None:
                for param in params:
                    value = params[param]
                    self._params_[param] = [param, 'str', [value], False]

            # then setup default values from para definitions
            if self._params_ is not None:
                for param_name in self._params_:
                    param = self._params_[param_name]
                    # print('set param %s' % param)
                    param_name = param[0]
                    param_type = param[1]
                    param_values = param[2]
                    param_value = None
                    if param_values is not None and len(param_values) > 0:
                        param_value = param_values[0]
                    setattr(self, param_name, param_value)

            if self._options_ is not None:
                for option in self._options_:
                    # print('set option %s' % option)
                    setattr(self, option, False)

            # then analyze the real application arguments to set the effective param values
            n_decoded = 0
            first = True
            for arg in sys.argv:
                if first:
                    first = False
                    continue

                if arg.startswith('-'):
                    opt = arg[1:]
                    if not hasattr(self, opt):
                        self._help('Bad option %s' % arg)
                        return

                    if opt == 'help':
                        self._help()
                        exit()

                    setattr(self, opt, True)
                    n_decoded += 1
                    continue

                if arg == '':
                    continue

                # handle non-option arguments

                words = arg.split('=')
                if len(words) < 2:
                    self._help('Bad argument [%s]' % repr(sys.argv))
                    return

                param_name = words[0]
                if not hasattr(self, param_name):
                    self._help('Bad argument %s' % arg)
                    return

                value = arg.replace(param_name + '=', '')
                setattr(self, param_name, value)
                n_decoded += 1

            # then fix up ro check param values
            for param_name in self._params_:
                param = self._params_[param_name]
                param_type = param[1]
                param_values = param[2]
                param_value = None
                if param_values is not None and len(param_values) > 0:
                    param_value = param_values[0]
                mandatory = param[3]

                effective_value = getattr(self, param_name)

                if effective_value is None and mandatory:
                    self._help('Mandatory value missing for %s' % param_name)

                if param_values is not None and len(param_values) > 1 and effective_value not in param_values:
                    self._help('Value error for %s' % param_name)

                if param_type == 'str' and effective_value is not None:
                    # effective_value = effective_value.decode(Encoding)
                    pass
                elif param_type == 'int' and effective_value is not None:
                    effective_value = int(effective_value)

                setattr(self, param_name, effective_value)

            for i in range(n_decoded):
                sys.argv.pop()
            pass
        except:
            print('bad arguments')
            raise


# --------------------------------------------
# Several data spaces are available:
#  cache    cache for the EDMS export
#  csv      CSV files (users, groups, ...)
#  tmp      temp space for the EDMS import of attached files
#
# By defult this space is in u'/workspace/atriumdata'
#
def set_dataspace(space=None):
    global DataSpace

    if space:
        DataSpace = space


def dataspace():
    global DataSpace

    return DataSpace


def init_objets_from_string(lignes, constructor, key, output_dict):
    running = True
    first = True
    numero = 0

    for ligne in lignes:
        ligne = ligne.strip()
        ligne = ligne.split(';')

        if not running:
            break

        if first:
            labels = ligne
            first = False
            continue

        numero += 1

        if len(ligne) == 0 or ligne[0].startswith('#'):
            continue

        objet = constructor()

        if hasattr(objet, 'ligne'):
            dkey = objet.ligne(numero, labels, ligne)
            if dkey is None:
                continue
        else:
            i = 0
            for label in labels:
                if label == '':
                    label = 'C%d' % i

                if i >= len(ligne):
                    # print('label=%s ligne=%s' % (label, repr(ligne)))
                    pass
                else:
                    # print('label=%s ligne=%s' % (label, repr(ligne[i])))
                    setattr(objet, label, ligne[i])
                i += 1

            dkey = getattr(objet, key)

        output_dict[dkey] = objet


# --------------------------------------------
# Read a CSV file , building a dictionary of objects
#
# - we assume that the input file obeys the following format:
#    + the first line contains the object field list
#    + fields are separated by ';'
#    + empty lines are ignored
#    + lines starting with '#' are ignored
# - every line generates one object using the specified constructor
# - the specified key is the key to the dictionary
#
def init_objets(file_name, constructor, key, output_dict):
    global DataSpace

    #
    # We look for the file either in the current space or in the dataspace
    #
    if not os.path.exists(file_name):
        file_name = DataSpace + '/' + file_name

    if not os.path.exists(file_name):
        return 'FileNotFound ' + file_name

    try:
        # print('codecs.open(%s)' % file_name)
        fichier = codecs.open(file_name, 'rb', 'windows-1252')

        # lignes = csv.reader(fichier, delimiter=';')
        lignes = fichier.readlines()

        init_objets_from_string(lignes, constructor, key, output_dict)

    except IOError:
        return('cannot open file ', file_name)
    else:
        fichier.close()

    return 'OK'

# --------------------------------------------
# calling the SetAtriumFunctionalDomain primitive
#
def set_atrium_functional_domain(session, user, domain, role):
    if user == "":
        return None

    # print('user=%s' % user)

    if "SetAtriumFunctionalDomain" not in session.operations:
        print("Cannot set AtriumFunctionalDomain")
        return None

    return session._execute("SetAtriumFunctionalDomain", user=user, domain=domain, role=role)


# --------------------------------------------
# calling the SetAtriumIsInactive primitive
#
def set_atrium_is_inactive(session, user, is_inactive=True):
    if user == "":
        return None

    # print('user=%s' % user)

    if "SetAtriumIsInactive" not in session.operations:
        print("Cannot set AtriumIsInactive")
        return None

    return session._execute("SetAtriumIsInactive", user=user, is_inactive=is_inactive)


# --------------------------------------------
# test if atrium_is_inactive
#
def test_atrium_is_inactive(session, user):
    status, infos = session.read_user(user)

    if status >= 400:
        return None

    if 'extendedGroups' not in infos:
        return None
 
    groups = infos['extendedGroups']

    is_inactive = False
    for g in groups:
        if g['label'] == 'Atrium_InactiveUsers':
            is_inactive = True
            break

    return is_inactive


# --------------------------------------------
# Reading all functional domains for Laboratoires|Projets|Activites declared in the Atrium base :
#
#  we get all primary spaces of type Laboratoire|Projet|Activite then whe read the FunctionalDomain metadata
#  this approach is needed since the FunctionalDomain vocabulary does not differenciate
#        Laboratoires | Projets | Activités
#
def get_fds(session, cat="Laboratoire"):
    query = "SELECT * FROM %s" % cat

    entries = session.query(query)

    # print(result)

    fds = []

    for doc in entries:
        f = doc['path']

        if not (re.match('.*/%ss/.*' % cat, f) or re.match('.*/%s' % 'Direction', f)):
            continue

        properties = doc['properties']
        fds.append(properties['AtriumFunctionalDomainSchema:FunctionalDomain'])

    return fds


# --------------------------------------------
# test if this user has a role for this functional domain
#
#  return 2 values:
#   bool = True if the user exists
#   role or None = granted role.
#
def test_user_role(session, user, fd):
    status, result = session.read_user(user)
    if status != 200:
        return None, None

    if 'extendedGroups' in result:
        props = result['extendedGroups']
        for prop in props:
            name = prop['name']
            if re.match('Atrium_[^_]+_[^_]+$', name):
                m = re.match('Atrium_([^_]+)_([^_]+)$', name)
                if m.group(1) == fd:
                    return True, m.group(2)

    return True, None


# -----------------------------------------------------------------
#  Get the user personal space to build the Atrium perma-link
#
def get_user_workspace(host, session, email):

    # ce pattern est commun à toutes les plateformes
    # par contre il faudrait vérifier que le fitre sur les caractères est complet
    #
    # So far this function is devalidated until we solve the problem

    url = ''

    """
    path = '/default-domain/UserWorkspaces/' + re.sub('[@_.]', '-', email)

    # query = "SELECT * FROM Workspace WHERE ecm:path = '%s'" % path
    query = "SELECT * FROM Workspace WHERE ecm:path STARTSWITH '/default-domain/UserWorkspaces/'"

    entries = session.query(query)

    paths = [e['path'] for e in entries]

    for p in paths:
        if re.match(p, path):
            print('ok')
            break

    # status, result = session.get_document(path)

    url = None

    if host == 'local':
        host = 'http://localhost:8080'
    elif host == 'dev':
        host = 'https://atrium-dev.in2p3.fr'
    elif host == 'prod':
        host = 'https://atrium.in2p3.fr'

    if status < 400:
        url = '%s/nuxeo/nxdoc/default/%s/view_documents' % (host, result['uid'])
    """

    return url


def set_mail_test_mode(mode=False):
    global MailTesting
    MailTesting = mode


# -----------------------------------------------------------------
# Construct a mail contents after the account creation
#  - this mail give
#    + the password
#    + the perma-link to the personal space
#
def build_account_creation_mail(email, prenom, nom, pwd, racine, url='', role='Reader'):
    labo = ''
    labo_txt = ''
    if racine != '':
        labo = repr(racine)
        labo = re.sub("^u'", '', labo)
        labo = re.sub("'$", '', labo)
        labo_txt = "Par ailleurs, vous avez reçu la permission de %s sur l'espace documentaire de la racine [%s]\n" % (role, labo)

    uws_text = ''

    if url != '':
        url = repr(url)
        url = re.sub("^u'", '', url)
        url = re.sub("'$", '', url)
        uws_text = """
Vous pouvez directement joindre votre espace personnel en suivant ce lien:
    %s\n
    """ % url

    french_text = """------------- Création d'un compte Atrium ---------

Vous recevez ce mail (automatique) car vous avez demandé l'ouverture d'un compte Atrium.

Le compte, dont les caractéristiques suivent, a été créé pour %s %s:

identifiant: %s
mot de passe: %s

Vous pouvez également vous connecter via votre certificat si l'adresse mail correspond.

(Merci de modifier ce mot de passe dès votre première connexion: [Home/Profile/Actions])

Utilisez ce lien pour vous connecter à Atrium: https://atrium.in2p3.fr/nuxeo/login.jsp
%s
Contactez votre Administrateur Local Atrium pour de plus amples informations, et pour obtenir des droits spécifiques adaptés à votre activité.
%sLien vers la documentation Atrium (une fois la connexion établie).

https://atrium.in2p3.fr/nuxeo/nxdoc/default/57e2cadf-70c0-43d2-ac16-3dfa530fce0d/view_documents

(merci de ne pas répondre à ce mail)

Cordialement
L'équipe Projet Atrium
    """ % (prenom, nom, email, pwd, labo_txt, uws_text)

    english_text = """------------- Atrium account creation ---------

You are receiving this (automatic) mail because you asked for an Atrium account.

Your account for %s %s is :
Login : %s
Password : %s

You may also use your electronic certificate when the email matches.

(Please change your password the first time you log in [Home/Profile/Actions]).

(Please change your language preference the first time you log in [Home/Preferences/Actions]).

Please use this link for login to Atrium: https://atrium.in2p3.fr/nuxeo/login.jsp

You can ask your Atrium local administration contact for more authorizations.
Atrium documentation (in French) (once connected to Atrium):

https://atrium.in2p3.fr/nuxeo/nxdoc/default/57e2cadf-70c0-43d2-ac16-3dfa530fce0d/view_documents

(Please do not answer this message)

Regards,
Atrium Project Team
    """ % (prenom, nom, email, pwd)

    msg = MIMEText("""
%s
%s
""" % (french_text, english_text), 'plain', 'utf-8')

    msg['Subject'] = "Ouverture de compte Atrium"

    return msg


# -----------------------------------------------------------------
# Construct a mail contents after the account creation
#  - this mail give
#    + the password
#    + the perma-link to the personal space
#
def build_logging_creation_mail(email, prenom, nom, racine, role='Reader'):
    labo = ''
    labo_txt = ''
    if racine != '':
        labo = repr(racine)
        labo = re.sub("^u'", '', labo)
        labo = re.sub("'$", '', labo)
        labo_txt = "Avec mise en place du rôle %s pour la racine %s" % (role, labo)

    msg = MIMEText("""
------------- Création d'un compte Atrium ---------

Le compte, dont les caractéristiques suivent, a été créé pour %s %s

identifiant: %s

%s
""" % (prenom, nom, email, labo_txt), 'plain', 'utf-8')

    msg['Subject'] = "Ouverture de compte Atrium"

    return msg


# -----------------------------------------------------------------
#  Sending a email to one single destination
#  the message itself has to be constructed using the MIMEText facility.
#
def sendmail(sender, to, message):
    global MailTesting

    message['From'] = sender
    message['To'] = to

    if MailTesting:
        print(('expected to=[%s]' % to))
        sender = 'arnault@lal.in2p3.fr'
        to = 'arnault@lal.in2p3.fr'
        print(('real to=[%s]' % repr(to)))

    s = smtplib.SMTP('smtp.in2p3.fr')
    try:
        s.sendmail(sender, [to], message.as_string())
    except:
        print('Cannot send mail')

    s.quit()

# --------------------------------------------
# Utility to create a random password
#
PwdChars = string.ascii_letters + string.digits
PwdLength = 10


def get_random_password():
    global PwdChars, PwdLength

    random.seed = os.urandom(1024)

    p = ''.join(random.choice(PwdChars) for i in range(PwdLength))

    return p


# --------------------------------------------
# creation of a user account
#  - specify the host mode (local|dev|prod)
#  - give name and first name
#  - email is the account identifier
#  - specify the functional domain (IE. laboratory)
#
def create_user(host, session, nom, prenom, email, racine):
    global MailTesting

    ok = False

    pwd = get_random_password()
    session.create_user(email, prenom, nom, email, pwd)
    status, result = session.read_user(email)
    if result:
        print(('%s created' % email))
        set_atrium_functional_domain(session, email, racine, 'Reader')
        url = get_user_workspace(host, session, email)
        msg = build_account_creation_mail(email, prenom, nom, pwd, racine, url)

        if MailTesting:
            sender = 'arnault@lal.in2p3.fr'
        else:
            sender = email

        sendmail(sender, email, msg)

        msg = build_logging_creation_mail(email, prenom, nom, racine)

        if MailTesting:
            sender = 'arnault@lal.in2p3.fr'
        else:
            sender = "ATRIUM-ACCOUNT-L@IN2P3.FR"

        sendmail(sender, email, msg)

        ok = True

    return ok

# /default-domain/UserWorkspaces/mathieu-walter-cc-in2p3
# /default-domain/UserWorkspaces/mathieu-chretien-lpnhe-in2p3-f