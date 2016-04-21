# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
import json
import base64
import re
from functools import partial, update_wrapper


import sys
if sys.version_info[0:2] > (3,0):
    import http.client
    import urllib.parse
else:
    import httplib as http
    http.client = http
    import urllib as urllib
    urllib.parse = urllib

VERSION = [2,0]
STR_VERSION = 'v' + '.'.join(str(v) for v in VERSION)

# These headers are implicitly included in each request; however, each
# can be explicitly overridden by the client code. (Used in Client
# objects.)
_default_headers = {
    #XXX: Header field names MUST be lowercase; this is not checked
      'user-agent': 'agithub/' + STR_VERSION
    }

class API(object):
    '''
    The toplevel object, and the "entry-point" into the client API.
    Subclass this to develop an application for a particular REST API.

    Model your __init__ after the GitHub example.
    '''
    def __init__(self, *args, **kwargs):
        raise Exception (
                'Please subclass API and override __init__()  to'
                'provide a ConnectionProperties object. See the GitHub'
                ' class for an example'
                )

    def setClient(self, client):
        self.client = client

    def setConnectionProperties(self, props):
        self.client.setConnectionProperties(props)

    def __getattr__(self, key):
        return IncompleteRequest(self.client).__getattr__(key)
    __getitem__ = __getattr__

    def __repr__(self):
        return IncompleteRequest(self.client).__repr__()

    def getheaders(self):
        return self.client.headers

class IncompleteRequest(object):
    '''IncompleteRequests are partially-built HTTP requests.
    They can be built via an HTTP-idiomatic notation,
    or via "normal" method calls.

    Specifically,
    >>> IncompleteRequest(client).path.to.resource.METHOD(...)
    is equivalent to
    >>> IncompleteRequest(client).client.METHOD('path/to/resource', ...)
    where METHOD is replaced by get, post, head, etc.

    Also, if you use an invalid path, too bad. Just be ready to handle a
    bad status code from the upstream API. (Or maybe an
    httplib.error...)

    You can use item access instead of attribute access. This is
    convenient for using variables\' values and is required for numbers.
    >>> GitHub('user','pass').whatever[1][x][y].post()

    To understand the method(...) calls, check out github.client.Client.
    '''
    def __init__(self, client):
        self.client = client
        self.url = ''

    def __getattr__(self, key):
        if key in self.client.http_methods:
            htmlMethod = getattr(self.client, key)
            wrapper = partial(htmlMethod, url=self.url)
            return update_wrapper(wrapper, htmlMethod)
        else:
            self.url += '/' + str(key)
            return self

    __getitem__ = __getattr__

    def __str__(self):
        return self.url

    def __repr__(self):
        return '%s: %s' % (self.__class__, self.url)

class Client(object):
    http_methods = (
            'head',
            'get',
            'post',
            'put',
            'delete',
            'patch',
            )

    default_headers = {}
    headers = None

    def __init__(self, username=None,
            password=None, token=None,
            connection_properties=None
            ):

        # Set up connection properties
        if connection_properties is not None:
            self.setConnectionProperties(connection_properties)

    def setConnectionProperties(self, prop):
        '''
        Initialize the connection properties. This must be called
        (either by passing connection_properties=... to __init__ or
        directly) before any request can be sent.
        '''
        if type(prop) is not ConnectionProperties:
            raise TypeError("Client.setConnectionProperties: Expected ConnectionProperties object")

        if prop.extra_headers is not None:
            prop.filterEmptyHeaders()
            self.default_headers = _default_headers.copy()
            self.default_headers.update(prop.extra_headers)
        self.prop = prop

        # Enforce case restrictions on self.default_headers
        tmp_dict = {}
        for k,v in self.default_headers.items():
            tmp_dict[k.lower()] = v
        self.default_headers = tmp_dict

    def head(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('HEAD', url, None, headers)

    def get(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('GET', url, None, headers)

    def post(self, url, body=None, headers={}, **params):
        url += self.urlencode(params)
        if not 'content-type' in headers:
            # We're doing a json.dumps of body, so let's set the content-type to json
            headers['content-type'] = 'application/json'
        return self.request('POST', url, json.dumps(body), headers)

    def put(self, url, body=None, headers={}, **params):
        url += self.urlencode(params)
        if not 'content-type' in headers:
            # We're doing a json.dumps of body, so let's set the content-type to json
            headers['content-type'] = 'application/json'
        return self.request('PUT', url, json.dumps(body), headers)

    def delete(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('DELETE', url, None, headers)

    def patch(self, url, body=None, headers={}, **params):
        """
        Do a http patch request on the given url with given body, headers and parameters
        Parameters is a dictionary that will will be urlencoded
        """
        url += self.urlencode(params)
        if not 'content-type' in headers:
            # We're doing a json.dumps of body, so let's set the content-type to json
            headers['content-type'] = 'application/json'
        return self.request('PATCH', url, json.dumps(body), headers)

    def request(self, method, url, body, headers):
        '''Low-level networking. All HTTP-method methods call this'''

        headers = self._fix_headers(headers)
        url = self.prop.constructUrl(url)

        #TODO: Context manager
        conn = self.get_connection()
        conn.request(method, url, body, headers)
        response = conn.getresponse()
        status = response.status
        content = ResponseBody(response)
        self.headers = response.getheaders()

        conn.close()
        return status, content.processBody()

    def _fix_headers(self, headers):
        # Convert header names to a uniform case
        tmp_dict = {}
        for k,v in headers.items():
            tmp_dict[k.lower()] = v
        headers = tmp_dict

        # Add default headers (if unspecified)
        for k,v in self.default_headers.items():
            if k not in headers:
                headers[k] = v
        return headers

    def urlencode(self, params):
        if not params:
            return ''
        return '?' + urllib.parse.urlencode(params)

    def get_connection(self):
        if self.prop.secure_http:
            conn = http.client.HTTPSConnection(self.prop.api_url)
        elif self.connection_properties.extra_headers is None \
                or 'authorization' not in self.connection_properties.extra_headers:
            conn = http.client.HTTPConnection(self.prop.api_url)
        else:
            raise ConnectionError(
                'Refusing to send the authorization header over an insecure connection.')

        return conn

class Body(object):
    '''
    Superclass for ResponseBody and RequestBody
    '''
    def parseContentType(self, ctype):
        '''
        Parse the Content-Type header, returning the media-type and any
        parameters
        '''
        if ctype is None:
            self.mediatype = 'application/octet-stream'
            self.ctypeParameters = { 'charset' : 'ISO-8859-1' }
            return

        params = ctype.split(';')
        self.mediatype = params.pop(0).strip()

        # Parse parameters
        if len(params) > 0:
            params = map(lambda s : s.strip().split('='), params)
            paramDict = {}
            for attribute, value in params:
                # TODO: Find out if specifying an attribute multiple
                # times is even okay, and how it should be handled
                attribute = attribute.lower()
                if attribute in paramDict:
                    if type(paramDict[attribute]) is not list:
                        # Convert singleton value to value-list
                        paramDict[attribute] = [paramDict[attribute]]
                    # Insert new value along with pre-existing ones
                    paramDict[attribute] += value
                else:
                    # Insert singleton attribute value
                    paramDict[attribute] = value
            self.ctypeParameters = paramDict
        else:
            self.ctypeParameters = {}

        if 'charset' not in self.ctypeParameters:
            self.ctypeParameters['charset'] = 'ISO-8859-1'
            # NB: INO-8859-1 is specified (RFC 2068) as the default
            # charset in case none is provided

    def mangled_mtype(self):
        '''
        Mangle the media type into a suitable function name
        '''
        return self.mediatype.replace('-','_').replace('/','_')

class ResponseBody(Body):
    '''
    Decode a response from the server, respecting the Content-Type field
    '''
    def __init__(self, response):
        self.response = response
        self.body = response.read()
        self.parseContentType(self.response.getheader('Content-Type'))
        self.encoding = self.ctypeParameters['charset']

    def decode_body(self):
        '''
        Decode (and replace) self.body via the charset encoding
        specified in the content-type header
        '''
        self.body = self.body.decode(self.encoding)

    def processBody(self):
        '''
        Retrieve the body of the response, encoding it into a usuable
        form based on the media-type (mime-type)
        '''
        handlerName = self.mangled_mtype()
        handler = getattr(self, handlerName, self.application_octect_stream)
        return handler()


    ## media-type handlers

    def application_octect_stream(self):
        '''Handler for unknown media-types. It does absolutely no
        pre-processing of the response body, so it cannot mess it up
        '''
        return self.body

    def application_json(self):
        '''Handler for application/json media-type'''
        self.decode_body()

        try:
            pybody = json.loads(self.body)
        except ValueError:
            pybody = self.body

        return pybody

    text_javascript = application_json
    # XXX: This isn't technically correct, but we'll hope for the best.
    # Patches welcome!

    # Insert new media-type handlers here

class ConnectionProperties(object):
    __slots__ = ['api_url', 'url_prefix', 'secure_http', 'extra_headers']

    def __init__(self, **props):
        # Initialize attribute slots
        for key in self.__slots__:
            setattr(self, key, None)

        # Fill attribute slots with custom values
        for key, val in props.items():
            if key not in ConnectionProperties.__slots__:
                raise TypeError("Invalid connection property: " + str(key))
            else:
                setattr(self, key, val)

    def constructUrl(self, url):
        if self.url_prefix is None:
            return url
        return self.url_prefix + "/" + url

    def filterEmptyHeaders(self):
        if self.extra_headers is not None:
            self.extra_headers = self._filterEmptyHeaders(self.extra_headers)

    def _filterEmptyHeaders(self, headers):
        newHeaders = {}
        for header in headers.keys():
            if header is not None and header != "":
                newHeaders[header] = headers[header]

        return newHeaders
