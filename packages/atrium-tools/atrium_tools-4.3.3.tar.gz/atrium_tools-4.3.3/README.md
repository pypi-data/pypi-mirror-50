Ce package rassemble un ensemble d'outils permettant de communiquer avec, ou agir sur, la base documentaire Atrium
en utilisant l'interface APIREST entre le serveur Nuxeo et des applications clientes

Deux composantes principales:

- **atrium_shell**: application cliente offrant plusieurs actions de navigation vers la base Atrium
- **nuxeolib**: la librairie de base impl�mentant l'APIREST selon le protocole d�crit dans la documentation Nuxeo,
  ainsi que plusieurs utilitaires bas�s sur les conventions Atrium.


Installation
============

Installation de base
--------------------

Ici, nous allons exploiter le m�canisme standard du monde Python: **pip** pour installer ce package Python.

Le package **atrium_tools** a �t� configur� au format standard des packages Python, et a �t� d�pos� dans le
d�p�t officiel **PyPi**.

Le seul mode d'installation propos� ici est bas� sur les environnements virtuels de Python. Nous supposons 
que Python (version >= 3) est install� dans votre syst�me

    > python -V
    > python -m venv atrium

    > source atrium/bin/activate (*sous Unix*)
    > atrium \Scripts\activate (*sous Windows*)

    > pip install atrium-tools
    > python -m atrium_shell.atrium_shell login=<myatriumaccount> -ls

Pour mettre � jour la version du package:

    > pip install --upgrade atrium-tools

Il est possible de questionner l'installation actuelle:

    > pip show atrium-tools


Ou bien de d�sinstaller le package:

    > pip uninstall -y atrium-tools

Et de d�sactiver l'environ `atrium` Python

    > deactivate

L'application atrium_shell
==========================

Introduction
------------

Cette application permet d'interroger la base Atrium un peu comme la commande **ls** en unix ou **dir** en windows.

Authentification
----------------

Pour acc�der au serveur Nuxeo, une authentification est n�cessaire. Deux m�thodes d'authentification sont possibles:

- en utilisant le param�tre ``login=xxx`` sur la ligne de commande. Ensuite, le mot de passe
  sera demand� en interrogation cach�e

- en utilisant le fichier **.netrc** (https://sites.google.com/site/diezone/ftp---file-transfert-protocol/ftp---le-fichier-netrc)

Il est ainsi possible de sp�cifier le couple `<user id>/<mdp>` dans le fichier Unix/Windows standard `$HOME/.netrc`
Ce fichier doit obligatoirement �tre prot�g� ainsi:

    > ls -al ../.netrc
    -rw------- 1 arnault SI 399 Apr  8 17:10 ../.netrc

Autrement dit, seul l'utilisateur doit avoir acc�s � ce document

Ce fichier texte contient des lignes au format suivant:

    machine atrium.in2p3.fr login <identifiant> password <motdepasse>

Si le fichier `~/.netrc` existe et que la variable d'environnement `HOME` est d�finie, 
alors il ne sera pas n�cessaire d'utiliser l'argument `login=xxx` 
et la connexion Atrium sera �tablie automatiquement avec l'identifant d�crit dans le ficher `~/.netrc` 


Arguments
---------

    login = str      : Compte Atrium (le mot de passe sera demand�)

    cd    =  str[/]  : Dossier courant 
                       Par exemple cd=/Laboratoires/IPNO
                       
    user   = str[]   : Specification alternative pour le dossier au lieu de cd
                       exemple: arnault@lal.in2p3.fr
    

    cp      = str[]  : document � copier
    set_acl = str[]  : acl � installer sur le dossier sp�cifi� (<permission>,<group/user>)
    rm_acl  = str[]  : acl � supprimer du le dossier sp�cifi� (<permission>,<group/user>)
    subs_acl = str[] : acl � supprimer du le dossier sp�cifi� (<permission1>,<group1/user1>,<permission2>,<group2/user2>)
    
    permission:
        Publisher
        Approver
        Validator
        Reader
        PublisherSection
        LocalAdmin
        Writer

    to      = str[]  : document destination (cp, set_acl, rm_acl, subs_acl)

    depth  =  int[0] : Profondeur dans l'arborescence. Par d�faut la valeur 0 indique le seul premier niveau
    
    -ls              : Listing des documents � partir d'un espace donn�
    -csv             : Production d'un fichier CSV d�crivant l'arborescence des documents 
    -draw            : Production d'un graphique d�crivant l'arborescence des documents 
    -rights          : Controle l'affichage des droits

Quelques pr�cisions:

* La cible de d�part peut �tre sp�cifi�e:
    * soit avec `cd` pour un espace institutionnel
    * soit avec `user` pour un espace personnel, en sp�cifiant l'intitul� du compte Atrium
* L'option `set_acl` s'applique uniquement au dossier sp�cifi� avec `to=<dossier>`
* L'option `rm_acl` s'applique r�cursivement � tous les dossiers enfants � partir du dossier `to=<dossier`
* L'option `subs_acl` s'applique r�cursivement � tous les dossiers enfants � partir du dossier `to=<dossier`
* Dans l'option `subs_acl` on peut substituer une groupe/user ind�pendemment de la permission en utilisant "%" pour la permission
* Les options `ls`, `csv`, `draw` exploitent l'option `depth=n`

Utilisation
-----------

Quelques exemples d'utilisation (*dans les exemples ci-dessous on suppose que 
l'authentification est r�alis�e via le fichier .netrc*):

    >>> python -m atrium_shell.atrium_shell -ls cd=/Laboratoires/LAL/ATLAS
    //Atrium/Laboratoires/LAL/ATLAS
      ATLAS/PIXELS
      ATLAS/CALORIM�TRIE Argon Liquide [Block]
      ATLAS/HGTD (High Granularity Timing Detector)


    >>> python -m atrium_shell.atrium_shell -ls cd=/Laboratoires/LAL/ATLAS depth=1
    //Atrium/Laboratoires/LAL/ATLAS
      ATLAS/PIXELS
        ATLAS/PIXELS/M�canique [Block]
        ATLAS/PIXELS/Om�gapix [Block]
        ATLAS/PIXELS/FEi4 [Block]
        ATLAS/PIXELS/Doping_Profile [Block]
        ATLAS/PIXELS/RD53 [Block]
        ATLAS/PIXELS/Interconnexion [Block]
        ATLAS/PIXELS/Acquisition [Block]
        ATLAS/PIXELS/atlas_synchro [Block]
        ATLAS/PIXELS/Salle Blanche PIXELS
      ATLAS/CALORIM�TRIE Argon Liquide [Block]
        ATLAS/CALORIM�TRIE Argon Liquide/Banc de tests robotis�
      ATLAS/HGTD (High Granularity Timing Detector)
        ATLAS/HGTD (High Granularity Timing Detector)/Ing�nierie M�canique
        ATLAS/HGTD (High Granularity Timing Detector)/Recrutement-AI bac+2



Nuxeolib
=========

Ce module contient tous les appels de bas niveau vers l'APIREST de Nuxeo, et permet de d�velopper des applications
utilitaires acc�dant � la base de donn�es Atrium.


- checkout(ref)
- checkin(ref, version='minor', comment='')
- checkoutin(ref, version='minor', comment='')
- create_tree_snapshot(ref, version='minor')
- create_version(ref, increment='Minor', save_document=True)
- set_property(ref, xpath, value)
- delete(ref)
- get_children(ref)
- get_parent(ref)
- get_versions(ref)
- lock(ref)
- unlock(ref)
- move(ref, target, name=None)
- publish(ref, target)
- copy(ref, target, name=None)
- add_permission(ref, permission, user, acl='local')
- get_relations(ref)
- delete_relation(source, destination)
- create_relation(ref, destination)
- query(query, language=None)
- get_blob(ref)
- get_blobs(ref)
- attach_blob(ref, blob)
-

- open_batch()
- close_batch(batch_id)
- upload_files(input_names=None, batch_id=None)
- change_title(uid, title)
- get_document(name)

    get the uid of a document from its path

- create_document_with_properties(path,
                                  name,
                                  doc_type,
                                  properties=None,
                                  files=None,
                                  from_uid=None)


         We create a document in one single operation:
          - mandatory args are: path, name, doc_type
          - properties can be added(dc:title, uid:minor_version, dc:description, ...)
          - files: joint files.


- update_document_with_properties(uid,
                                  title,
                                  doc_type,
                                  properties=None,
                                  files=None)

        this function is similar to the create function, but for updating an existing document.



- read_document(doc_id)

        read the properties of an existing document


- get_acls(doc_id)
- delete_document(doc_id)
- change_document_state(uid, state=u'')
- read_user(name)

        read the properties of an user account


- create_user(user,
              first_name=None,
              last_name=None,
              email='a@b.c',
              password='user',
              company=None)

             Basic creation function the required properties are:
               identifier (generally it's the email
               first name
               name
               email
               password


- update_user(user,
              first_name=None,
              last_name=None,
              email=None,
              password=None,
              company=None,
              is_inactive=None)
- delete_user(user)
- get_users(query=u'*', data=False, max_results=None)

          query all users using a wildcard expression
          this internally get a multipage request and assembles the pages


- get_directory(domain)

        query a vocabulary


- add_directory_entry(directory, entry)
- get_groups(pattern)
- create_group(group)
- get_group(group)
- add_user_to_group(group, user)
- add_subgroup_to_group(group, subgroup)
- delete_group(group)
-
-

- init_session(host=u'local', login='', password='', auth='')

    Initialise the session according to the host modes: local, dev, prod

- connect(host, login, auth='')

    on top of the init_session function permit to enter the hidden password

- get_login()

    retreive the actual login

- purge_document(session, path, title='', edms='')

    Deep suppression of a given document (including from the Corbeille)

- init_objets_from_string(lignes, constructor, key, output_dict)



- init_objets(file_name, constructor, key, output_dict)

    Read a CSV file , building a dictionary of objects

    - we assume that the input file obeys the following format:
      + the first line contains the object field list
      + fields are separated by ';'
      + empty lines are ignored
      + lines starting with '#' are ignored
    - every line generates one object using the specified constructor
    - the specified key is the key to the dictionary

- set_atrium_functional_domain(session, user, domain, role)

    call the SetAtriumFunctionalDomain primitive

- set_atrium_is_inactive(session, user, is_inactive=True)

    call the SetAtriumIsInactive primitive

- test_atrium_is_inactive(session, user)

    test if atrium_is_inactive

- get_fds(session, cat="Laboratoire")

    Reading all functional domains for Laboratoires|Projets|Activites declared in the Atrium base :

     we get all primary spaces of type Laboratoire|Projet|Activite then whe read the FunctionalDomain metadata
     this approach is needed since the FunctionalDomain vocabulary does not differenciate
        Laboratoires | Projets | Activit�s

- test_user_role(session, user, fd)

    test if this user has a role for this functional domain

     return 2 values:
     bool = True if the user exists
     role or None = granted role.

- get_user_workspace(host, session, email)

    Get the user personal space to build the Atrium perma-link

- build_account_creation_mail(email, prenom, nom, pwd, racine, url, role='Reader')

    Construct a mail contents after the account creation
     - this mail give
      + the password
      + the perma-link to the personal space

- build_logging_creation_mail(email, prenom, nom, racine, role='Reader')

    Construct a mail contents after the account creation
     - this mail give
      + the password
      + the perma-link to the personal space

- sendmail(sender, to, message)

    Sending a email to one single destination
    the message itself has to be constructed using the MIMEText facility.

- get_random_password()

    Utility to create a random password

- create_user(host, session, nom, prenom, email, racine)

    creation of a user account
     - specify the host mode (local|dev|prod)
     - give name and first name
     - email is the account identifier
     - specify the functional domain (IE. laboratory)

Installation en tant que d�veloppeur, du package **atrium_tools**
-----------------------------------------------------------------

On peut installer ce package � partir de **GitLab**, par exemple en t�l�chargeant et installant l'archive au format ZIP.
Mais il est aussi possible de *cloner* directement le projet � partir de **GitLab** si on souhaite contribuer
au d�veloppement.

Ce logiciel est enti�rement bas� sur le langage Python. Il est d�velopp� en compatibilit� avec la
version >=3.6 du langage Python.
Donc il est indispensable qu'une version >= 3.6 du langage Python soit install�e sur votre machine

Ensuite pour installer la suite logicielle voici les deux m�thodes:

1. en clonant le d�p�t Git::

    > mkdir myworkspace
    > cd myworkspace
    > git clone git@gitlab.in2p3.fr:atrium/atrium_tools.git

petit rappel pour modifier un �l�ment en git::

    > [edit]...
    > git status
    > git commit -am "porquoi cette modification"
    > git push


2. en r�cup�rant une archive ZIP � partir de GitLab::

    � partir du site GitLab https://gitlab.in2p3.fr/atrium/atrium_tools
    installer et d�zipper l'archive


