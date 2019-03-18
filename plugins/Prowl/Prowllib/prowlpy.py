#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, Jaccob Burch
# Copyright (c) 2010, Olivier Hervieu
# Copyright (c) 2011, Ken Pepple
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# * Neither the name of the University of California, Berkeley nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Prowlpy V0.50 originally written by Jacob Burch, modified by Olivier Hervieu.
Updated to Prowl API version 1.2 by Ken Pepple.

Python Prowlpy is a python module that implement the public api of Prowl to
send push notification to iPhones.

See http://prowlapp.com for information about Prowl.

The prowlpy module respect the API of prowl. So prowlpy provides a Prowl class
which implements four methods :
- post, to push a notification to an iPhone,
- verify_key, to verify an API key.
- retrieve_token, to get a registration token for use in retrieve/apikey and
  the associated URL for the user to approve the request.
- retrieve_apikey, to get an API key from a registration token retrieved in
  retrieve/token.
"""
from httplib import HTTPSConnection as Https
from urllib import urlencode
from xml.dom import minidom

API_DOMAIN = 'api.prowlapp.com'
VERSION = '0.52'

class Prowl(object):
    def __init__(self, apikey, providerkey=None):
        """
        Initialize a Prowl instance.
        """
        self.apikey = apikey
        # Set User-Agent
        self.headers = {'User-Agent': "Prowlpy/%s" % VERSION,
                        'Content-type': "application/x-www-form-urlencoded"}

        # Aliasing
        self.add = self.post

    def _relay_error(self, error_code, reason=""):
        """
        Errors from http://www.prowlapp.com/api.php:
         - 400 Bad request, the parameters you provided did not validate,
           see ERRORMESSAGE,
         - 401 Not authorized, the API key given is not valid, and does not
           correspond to a user,
         - 406 Not acceptable, your IP address has exceeded the API limit,
         - 409 Not approved, the user has yet to approve your retrieve request,
         - 500 Internal server error, something failed to execute properly on
           the Prowl side.
        """

        if error_code == 400:
            raise Exception(
                "Bad Request. The parameters you provided did not validate")
        elif error_code == 401:
            raise Exception(
                "%s Probably invalid API key %s" % (reason, self.apikey))
        elif error_code == 406:
            raise Exception(
                "Not acceptable, your IP address has exceeded the API limit")
        elif error_code == 409:
            raise Exception(
                "Not approved, the user has yet to approve your retrieve request")
        elif error_code == 500:
            raise Exception(
                "Internal server error")

    def post(self, application=None, event=None,
             description=None, priority=0, providerkey=None,
             url=None):
        """
        Post a notification..

        You must provide either event or description or both.
        The parameters are :
        - application ; The name of your application or the application
          generating the event.
        - providerkey (optional) : your provider API key.
          Only necessary if you have been whitelisted.
        - priority (optional) : default value of 0 if not provided.
          An integer value ranging [-2, 2] representing:
             -2. Very Low
             -1. Moderate
              0. Normal
              1. High
              2. Emergency (note : emergency priority messages may bypass
                            quiet hours according to the user's settings)
        - event : the name of the event or subject of the notification.
        - description : a description of the event, generally terse.
        - url (optional) : The URL which should be attached to the
          notification.
        """

        # Create the http object
        h = Https(API_DOMAIN)

        # Perform the request and get the response headers and content
        data = {'apikey': self.apikey,
                'application': application,
                'event': event,
                'description': description,
                'priority': priority}

        if providerkey is not None:
            data['providerkey'] = providerkey

        if url is not None:
            data['url'] = url[0:512]  # API limits to 512 characters

        h.request("POST",
                  "/publicapi/add",
                  headers=self.headers,
                  body=urlencode(data))
        response = h.getresponse()
        request_status = response.status

        if request_status == 200:
            return True
        else:
            self._relay_error(request_status, response.reason)

    def verify_key(self, providerkey=None):
        """
        Verify if the API key is valid.

        The parameters are :
        - providerkey (optional) : your provider API key.
          Only necessary if you have been whitelisted.
        """
        h = Https(API_DOMAIN)

        data = {'apikey': self.apikey}

        if providerkey is not None:
            data['providerkey'] = providerkey

        h.request("GET",
                  "/publicapi/verify?" + urlencode(data),
                  headers=self.headers)

        request_status = h.getresponse().status

        if request_status != 200:
            self._relay_error(request_status)

    def retrieve_token(self, providerkey=None):
        """
        Get a registration token for use in retrieve/apikey
        and the associated URL for the user to approve the request.

        The parameters are :
        - providerkey (required) : your provider API key.

        This returns a dictionary such as:
        {'code': u'0',
         'remaining': u'999',
         'resetdate': u'1299535575',
         'token': u'60fd568423e3cd337b45172be91cabe46b94c200',
         'url': u'https://www.prowlapp.com/retrieve.php?token=60fd5684'}
        """

        h = Https(API_DOMAIN)

        data = {'apikey': self.apikey}

        if providerkey is not None:
            data['providerkey'] = providerkey

        h.request("GET",
                  "/publicapi/retrieve/token?" + urlencode(data),
                  headers=self.headers)

        request = h.getresponse()
        request_status = request.status

        if request_status == 200:
            dom = minidom.parseString(request.read())
            code = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('code')
            remaining = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('remaining')
            resetdate = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('resetdate')
            token = dom.getElementsByTagName('prowl')[0].\
                        getElementsByTagName('retrieve')[0].\
                        getAttribute('token')
            url = dom.getElementsByTagName('prowl')[0].\
                      getElementsByTagName('retrieve')[0].\
                      getAttribute('url')
            return dict(token=token, url=url, code=code,
                        remaining=remaining, resetdate=resetdate)
        else:
            self._relay_error(request_status)

    def retrieve_apikey(self, providerkey=None, token=None):
        """
        Get an API key from a registration token retrieved in retrieve/token.
        The user must have approved your request first, or you will get an
        error response.

        The parameters are :
        - providerkey (required) : your provider API key.
        - token (required): the token returned from retrieve_token.

        This returns a dictionary such as:
        {'apikey': u'16b776682332cf11102b67d6db215821f2c233a3',
         'code': u'200',
         'remaining': u'999',
         'resetdate': u'1299535575'}
        """

        h = Https(API_DOMAIN)

        data = {'apikey': self.apikey}

        if providerkey is not None:
            data['providerkey'] = providerkey
        else:
            raise Exception("Provider Key is required for retrieving API key")

        if token is not None:
            data['token'] = token
        else:
            raise Exception("Token is required for retrieving API key.\
                             Call retrieve_token to request it.")

        h.request("GET",
                  "/publicapi/retrieve/apikey?" + urlencode(data),
                  headers=self.headers)

        request = h.getresponse()
        request_status = request.status

        if request_status == 200:
            dom = minidom.parseString(request.read())
            code = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('code')
            remaining = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('remaining')
            resetdate = dom.getElementsByTagName('prowl')[0].\
                            getElementsByTagName('success')[0].\
                            getAttribute('resetdate')
            users_api_key = dom.getElementsByTagName('prowl')[0].\
                                getElementsByTagName('retrieve')[0].\
                                getAttribute('apikey')
            return dict(apikey=users_api_key, code=code, remaining=remaining,
                        resetdate=resetdate)
        else:
            self._relay_error(request_status)