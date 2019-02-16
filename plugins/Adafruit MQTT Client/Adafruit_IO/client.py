# Copyright (c) 2014 Adafruit Industries
# Authors: Justin Cooper & Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json

import requests

from .errors import RequestError, ThrottlingError
from .model import Data, Feed, Group


class Client(object):
    """Client instance for interacting with the Adafruit IO service using its
    REST API.  Use this client class to send, receive, and enumerate feed data.
    """

    def __init__(self, key, proxies=None, base_url='https://io.adafruit.com'):
        """Create an instance of the Adafruit IO REST API client.  Key must be
        provided and set to your Adafruit IO access key value.  Optionaly
        provide a proxies dict in the format used by the requests library, and
        base_url to point at a different Adafruit IO service (the default is
        the production Adafruit IO service over SSL).
        """
        self.key = key
        self.proxies = proxies
        # Save URL without trailing slash as it will be added later when
        # constructing the path.
        self.base_url = base_url.rstrip('/')

    def _compose_url(self, path):
        return '{0}/{1}'.format(self.base_url, path)

    def _handle_error(self, response):
        # Handle explicit errors.
        if response.status_code == 429:
            raise ThrottlingError()
        # Handle all other errors (400 & 500 level HTTP responses)
        elif response.status_code >= 400:
            raise RequestError(response)
        # Else do nothing if there was no error.

    def _get(self, path):
        response = requests.get(self._compose_url(path),
                                headers={'X-AIO-Key': self.key},
                                proxies=self.proxies)
        self._handle_error(response)
        return response.json()

    def _post(self, path, data):
        response = requests.post(self._compose_url(path),
                                 headers={'X-AIO-Key': self.key,
                                          'Content-Type': 'application/json'},
                                 proxies=self.proxies,
                                 data=json.dumps(data))
        self._handle_error(response)
        return response.json()

    def _delete(self, path):
        response = requests.delete(self._compose_url(path),
                                   headers={'X-AIO-Key': self.key,
                                            'Content-Type': 'application/json'},
                                   proxies=self.proxies)
        self._handle_error(response)

    # Data functionality.
    def send(self, feed_name, value):
        """Helper function to simplify adding a value to a feed.  Will find the 
        specified feed by name or create a new feed if it doesn't exist, then 
        will append the provided value to the feed.  Returns a Data instance 
        with details about the newly appended row of data.
        """
        path = "api/feeds/{0}/data/send".format(feed_name)
        return Data.from_dict(self._post(path, {'value': value}))

    def append(self, feed, value):
        """Helper function to simplify adding a value to a feed.  Will append the
        specified value to the feed identified by either name, key, or ID.
        Returns a Data instance with details about the newly appended row of data.
        Note that unlike send the feed should exist before calling append.
        """
        return self.create_data(feed, Data(value=value))

    def receive(self, feed):
        """Retrieve the most recent value for the specified feed.  Feed can be a
        feed ID, feed key, or feed name.  Returns a Data instance whose value
        property holds the retrieved value.
        """
        path = "api/feeds/{0}/data/last".format(feed)
        return Data.from_dict(self._get(path))

    def receive_next(self, feed):
        """Retrieve the next unread value from the specified feed.  Feed can be 
        a feed ID, feed key, or feed name.  Returns a Data instance whose value
        property holds the retrieved value.
        """
        path = "api/feeds/{0}/data/next".format(feed)
        return Data.from_dict(self._get(path))

    def receive_previous(self, feed):
        """Retrieve the previous unread value from the specified feed.  Feed can
        be a feed ID, feed key, or feed name.  Returns a Data instance whose 
        value property holds the retrieved value.
        """
        path = "api/feeds/{0}/data/previous".format(feed)
        return Data.from_dict(self._get(path))

    def data(self, feed, data_id=None):
        """Retrieve data from a feed.  Feed can be a feed ID, feed key, or feed
        name.  Data_id is an optional id for a single data value to retrieve.  
        If data_id is not specified then all the data for the feed will be 
        returned in an array.
        """
        if data_id is None:
            path = "api/feeds/{0}/data".format(feed)
            return list(map(Data.from_dict, self._get(path)))
        else:
            path = "api/feeds/{0}/data/{1}".format(feed, data_id)
            return Data.from_dict(self._get(path))

    def create_data(self, feed, data):
        """Create a new row of data in the specified feed.  Feed can be a feed
        ID, feed key, or feed name.  Data must be an instance of the Data class
        with at least a value property set on it.  Returns a Data instance with
        details about the newly appended row of data.
        """
        path = "api/feeds/{0}/data".format(feed)
        return Data.from_dict(self._post(path, data._asdict()))

    def delete(self, feed, data_id):
        """Delete data from a feed.  Feed can be a feed ID, feed key, or feed
        name.  Data_id must be the ID of the piece of data to delete.
        """
        path = "api/feeds/{0}/data/{1}".format(feed, data_id)
        self._delete(path)

    # Feed functionality.
    def feeds(self, feed=None):
        """Retrieve a list of all feeds, or the specified feed.  If feed is not
        specified a list of all feeds will be returned.  If feed is specified it
        can be a feed name, key, or ID and the requested feed will be returned.
        """
        if feed is None:
            path = "api/feeds"
            return list(map(Feed.from_dict, self._get(path)))
        else:
            path = "api/feeds/{0}".format(feed)
            return Feed.from_dict(self._get(path))

    def create_feed(self, feed):
        """Create the specified feed.  Feed should be an instance of the Feed
        type with at least the name property set.
        """
        path = "api/feeds/"
        return Feed.from_dict(self._post(path, feed._asdict()))

    def delete_feed(self, feed):
        """Delete the specified feed.  Feed can be a feed ID, feed key, or feed
        name.
        """
        path = "api/feeds/{0}".format(feed)
        self._delete(path)

    # Group functionality.
    def send_group(self, group_name, data):
        """Update all feeds in a group with one call.  Group_name should be the
        name of a group to update.  Data should be a dict with an item for each
        feed in the group, where the key is the feed name and value is the new
        data row value.  For example a group 'TestGroup' with feeds 'FeedOne'
        and 'FeedTwo' could be updated by calling:
        
        send_group('TestGroup', {'FeedOne': 'value1', 'FeedTwo': 10})
        
        This would add the value 'value1' to the feed 'FeedOne' and add the
        value 10 to the feed 'FeedTwo'.

        After a successful update an instance of Group will be returned with
        metadata about the updated group.
        """
        path = "api/groups/{0}/send".format(group_name)
        return Group.from_dict(self._post(path, {'value': data}))

    def receive_group(self, group):
        """Retrieve the most recent value for the specified group.  Group can be
        a group ID, group key, or group name.  Returns a Group instance whose
        feeds property holds an array of Feed instances associated with the group.
        """
        path = "api/groups/{0}/last".format(group)
        return Group.from_dict(self._get(path))

    def receive_next_group(self, group):
        """Retrieve the next unread value from the specified group.  Group can
        be a group ID, group key, or group name.  Returns a Group instance whose
        feeds property holds an array of Feed instances associated with the 
        group.
        """
        path = "api/groups/{0}/next".format(group)
        return Group.from_dict(self._get(path))

    def receive_previous_group(self, group):
        """Retrieve the previous unread value from the specified group.  Group
        can be a group ID, group key, or group name.  Returns a Group instance
        whose feeds property holds an array of Feed instances associated with
        the group.
        """
        path = "api/groups/{0}/previous".format(group)
        return Group.from_dict(self._get(path))

    def groups(self, group=None):
        """Retrieve a list of all groups, or the specified group.  If group is 
        not specified a list of all groups will be returned.  If group is 
        specified it can be a group name, key, or ID and the requested group 
        will be returned.
        """
        if group is None:
            path = "api/groups/"
            return list(map(Group.from_dict, self._get(path)))
        else:
            path = "api/groups/{0}".format(group)
            return Group.from_dict(self._get(path))

    def create_group(self, group):
        """Create the specified group.  Group should be an instance of the Group
        type with at least the name and feeds property set.
        """
        path = "api/groups/"
        return Group.from_dict(self._post(path, group._asdict()))

    def delete_group(self, group):
        """Delete the specified group.  Group can be a group ID, group key, or
        group name.
        """
        path = "api/groups/{0}".format(group)
        self._delete(path)
