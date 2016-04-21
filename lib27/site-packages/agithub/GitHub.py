# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import *

class GitHub(API):
    '''
    The agnostic GitHub API. It doesn't know, and you don't care.
    >>> from agithub import GitHub
    >>> g = GitHub('user', 'pass')
    >>> status, data = g.issues.get(filter='subscribed')
    >>> data
    ... [ list_, of, stuff ]

    >>> status, data = g.repos.jpaugh.repla.issues[1].get()
    >>> data
    ... { 'dict': 'my issue data', }

    >>> name, repo = 'jpaugh', 'repla'
    >>> status, data = g.repos[name][repo].issues[1].get()
    ... same thing

    >>> status, data = g.funny.I.donna.remember.that.one.get()
    >>> status
    ... 404

    That's all there is to it. (blah.post() should work, too.)

    NOTE: It is up to you to spell things correctly. A GitHub object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    '''
    def __init__(self, username=None, password=None, token=None, *args, **kwargs):
        props = ConnectionProperties(
                    api_url = 'api.github.com',
                    secure_http = True,
                    extra_headers = {
                        'accept' : 'application/vnd.github.v3+json',
                        'authorization' : self.generateAuthHeader(username, password, token)
                    })

        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)

    def generateAuthHeader(self, username=None, password=None, token=None):
        if token is not None:
            if password is not None:
                raise TypeError("You cannot use both password and oauth token authenication")
            return 'Token %s' % token
        elif username is not None:
            if password is None:
                raise TypeError("You need a password to authenticate as " + username)
            self.username = username
            return self.hash_pass(password)

    def hash_pass(self, password):
        auth_str = ('%s:%s' % (self.username, password)).encode('utf-8')
        return 'Basic '.encode('utf-8') + base64.b64encode(auth_str).strip()
