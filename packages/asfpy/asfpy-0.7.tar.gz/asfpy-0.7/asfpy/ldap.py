#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
 #the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" ASF LDAP Account Manager """

import sys
assert sys.version_info >= (3, 2)

import ldap
import ldap.modlist
import ldif
import re
import crypt
import random
import string


LDAP_URI = "ldaps://ldap-sandbox.apache.org:636"
LDAP_SUFFIX = 'dc=apache,dc=org'
LDAP_PEOPLE_BASE = 'ou=people,dc=apache,dc=org'
LDAP_APLDAP_BASE = 'cn=apldap,ou=groups,ou=services,dc=apache,dc=org'
LDAP_CHAIRS_BASE = 'cn=pmc-chairs,ou=groups,ou=services,dc=apache,dc=org'
LDAP_PMCS_BASE = 'ou=project,ou=groups,dc=apache,dc=org'
LDAP_DN = 'uid=%s,ou=people,dc=apache,dc=org'



def bytify(ldiff):
    """ Convert all values in a dict to byte-string """
    for k, v in ldiff.items():
        if type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is str:
                    v[n] = xv.encode('utf-8')
                n += 1
        else:
            if type(v) is str:
                v = [v.encode('utf-8')]
        ldiff[k] = v
    return ldiff
        
def stringify(ldiff):
    """ Convert all values in a dict to string """
    for k, v in ldiff.items():
        # Convert single-list to string
        if type(v) is list and len(v) == 1:
            v = v[0]
        
        if type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is bytes:
                    v[n] = xv.decode('utf-8')
                n += 1
        else:
            if type(v) is bytes:
                v = v.decode('utf-8')
        ldiff[k] = v
    return ldiff


class ConnectionException(Exception):
    """ Simple exception with a message and an optional origin exception (WIP) """
    def __init__ (self, message, origin = None):
        super().__init__(message)
        self.origin = origin

class ValidatorException(Exception):
    """ Simple validator exception with a message and an optional triggering attribute """
    def __init__ (self, message, attrib = None):
        super().__init__(message)
        self.attribute = attrib

class committer:
    """ Committer class, allows for munging data """
    
    def __init__(self, manager, res):
        self.manager = manager
        self.dn = res[0][0]
        self.dn_enc = self.dn.encode('ascii')
        self.attributes = stringify(res[0][1])
        
    def add_project(self, project):
        """ Add person to project (as committer) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'member', self.dn_enc)])
    
    def add_pmc(self, project):
        """ Add person to project (as PMC member) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'owner', self.dn_enc)])
    
    def remove_project(self, project):
        """ Remove person from project (as committer) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'member', self.dn_enc)])
    
    def remove_pmc(self, project):
        """ Remove person from PMC """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'owner', self.dn_enc)])


class manager:
    """ Top LDAP Manager class for whomever is using the script """
    def __init__(self, user, password, host = LDAP_URI):
        # Verify correct user ID syntax, construct DN
        if not re.match(r"^[-_a-z0-9]+$", user):
            raise ConnectionException("Invalid characters in User ID. Must be alphanumerical or dashes only.")
        
        # Init LDAP connection
        lc = ldap.initialize(host)
        
        lc.set_option(ldap.OPT_REFERRALS, 0)
        lc.set_option(ldap.OPT_TIMEOUT, 5)
        
        # Attempt to bind with user and pass provided
        try:
            lc.simple_bind_s(LDAP_DN % user, password)
        except ldap.INVALID_CREDENTIALS:
            raise ConnectionException("Invalid username or password supplied!")
        except ldap.TIMEOUT:
            raise ConnectionException("The backend authentication server timed out, please retry later.")
        except:
            raise ConnectionException("An unknown error occurred, please retry later.")
        
        # So far so good, set uid
        self.uid = user
        self.dn = LDAP_DN % user
        self.lc = lc
        
        # Get full name etc
        try:
            res = lc.search_s(LDAP_DN % user, ldap.SCOPE_BASE)
            assert(len(res) == 1)
            assert(len(res[0]) == 2)
            fn = res[0][1].get('cn')
            assert(type(fn) is list and len(fn) == 1)
            self.fullname = str(fn[0], 'utf-8')
            self.email = '%s@apache.org' % user
        except ldap.TIMEOUT:
            raise ConnectionException("The backend authentication server timed out, please retry later.")
        except AssertionError:
            raise ConnectionException("Common backend assertions failed, LDAP corruption?")

        
        # Get apldap status
        try:
            res = lc.search_s(LDAP_APLDAP_BASE, ldap.SCOPE_BASE)
            assert(len(res) == 1)
            assert(len(res[0]) == 2)
            members= res[0][1].get('member')
            assert(type(members) is list and len(members) > 0)
            self.isAdmin = bytes(LDAP_DN % user, 'utf-8') in members
        except ldap.TIMEOUT:
            raise ConnectionException("The backend authentication server timed out, please retry later.")
        except AssertionError:
            raise ConnectionException("Common backend assertions failed, LDAP corruption?")

    def load_account(self, uid):
        # Check if account exists!
        res = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uid=%s'%uid)
        if res:
            return committer(self, res)
        return None
    
    def nextUid(self):
        """ Find highest uid/gid number and return the number that follows. """
        try:
            res = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uidNumber=*', ['uidNumber'])
            umap = {}
            for x in res:
                umap[x[1].get('uidNumber')[0].decode('ascii')] = x[0]
            uids = [int(x[1].get('uidNumber')[0].decode('ascii')) for x in res]
            assert(type(uids) is list and len(uids) > 0)
            uids = sorted(uids)
            print("Highest current uidNumber: %s (%s)" % (uids[-1], umap[str(uids[-1])]))
            return uids[-1]+1
        except ldap.TIMEOUT:
            raise ConnectionException("The backend authentication server timed out, please retry later.")
        except AssertionError:
            raise ConnectionException("Common backend assertions failed, LDAP corruption?")
        
    def create_account(
        self,
        uid,
        email,
        fullname,
        forcePass = None,
        requireTwo = True,
    ):
        """ Attempts to create a committer account in LDAP """
        
        if not self.isAdmin:
            raise ConnectionException("You do not have sufficient access to create accounts")
        
        # Test if uid exists
        if self.load_account(uid):
            raise ConnectionException("An account with this uid already exists")
        
        # Test for clashing cn's
        res = self.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, 'cn=%s' % uid)
        if res:
            raise ValidatorException("availid clashes with project name %s!" % res[0][0], 'uid')
        
        uidnumber = self.nextUid()
        
        
        # Get surname and given name, validate against spurious whitespace
        names = fullname.split(' ')
        if len(names) < 2 and requireTwo:
            raise ValidatorException("Full name needs at least two parts!", 'fullname')
        givenName = names[0]
        surName = names[-1]
        for n in names:
            if not n.strip():
                raise ValidatorException("Found part of name with too much spacing!", 'fullname')
        
        # Validate email
        if not re.match(r"^\S+@\S+?\.\S+$", email):
            raise ValidatorException("Invalid email address supplied!", 'email')
        
        # Set password, b64-encoded crypt of random string
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        if forcePass:
            password = forcePass
        password_crypted = crypt.crypt(password, crypt.mksalt(method= crypt.METHOD_MD5))
        
        ldiff = {
            'objectClass': ['person', 'top', 'posixAccount', 'organizationalPerson', 'inetOrgPerson', 'asf-committer', 'hostObject', 'ldapPublicKey'],
            'loginShell': '/bin/bash',
            'asf-sascore': '10',
            'givenName': givenName,
            'sn': surName,
            'mail': email,
            'gidNumber': str(uidnumber),
            'uidNumber': str(uidnumber),
            'asf-committer-email': '%s@apache.org' % uid,
            'cn': fullname,
            'homeDirectory': '/home/%s' % uid,
            'userPassword': '{CRYPT}' + password_crypted,
        }
        
        # Convert everything to bytestrings because ldap demands it...
        bytify(ldiff)
        
        
        # Run LDIF on server
        dn = LDAP_DN % uid
        am = ldap.modlist.addModlist(ldiff)
        self.lc.add_s(dn, am)
        
        return self.load_account(uid)

class LDIFWriter_Sane(ldif.LDIFWriter):
    """ LDIFWriter with b64 detection fixed """
    
    def _needs_base64_encoding(self,attr_type,attr_value):
        """
        returns 1 if attr_value has to be base-64 encoded because
        of special chars or because attr_type is in self._base64_attrs
        """
        if attr_type.lower() == 'dn':
            # We must always exclude DN, as our own library makes this a str (utf-8)
            return False

        SAFE_STRING_PATTERN = r"(^[\x22-\x7Fa-zA-Z ]+$)"
        if type(attr_value) is bytes:
            attr_value = attr_value.decode('utf-8')
        return attr_type.lower() in self._base64_attrs or \
               re.match(SAFE_STRING_PATTERN, attr_value) is None

    