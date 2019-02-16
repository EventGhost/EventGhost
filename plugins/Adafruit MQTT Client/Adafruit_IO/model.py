# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

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
from collections import namedtuple
# Handle python 2 and 3 (where map functions like itertools.imap)
try:
    from itertools import imap as map
except ImportError:
    # Ignore import error on python 3 since map already behaves as expected.
    pass


# List of fields/properties that are present on a data object from IO.
DATA_FIELDS   = [ 'created_epoch', 
                  'created_at',
                  'updated_at',
                  'value',
                  'completed_at',
                  'feed_id',
                  'expiration',
                  'position',
                  'id' ]

STREAM_FIELDS = [ 'completed_at',
                  'created_at',
                  'id',
                  'value' ]

FEED_FIELDS   = [ 'last_value_at',
                  'name',
                  'stream',
                  'created_at',
                  'updated_at',
                  'unit_type',
                  'mode',
                  'key',
                  'unit_symbol',
                  'fixed',
                  'last_value',
                  'id' ]

GROUP_FIELDS  = [ 'description',
                  'source_keys',
                  'id',
                  'source',
                  'key',
                  'feeds',
                  'properties',
                  'name' ]


# These are very simple data model classes that are based on namedtuple.  This is
# to keep the classes simple and prevent any confusion around updating data
# locally and forgetting to send those updates back up to the IO service (since
# tuples are immutable you can't change them!).  Depending on how people use the
# client it might be prudent to revisit this decision and consider making these
# full fledged classes that are mutable.
Data   = namedtuple('Data', DATA_FIELDS)
Stream = namedtuple('Stream', STREAM_FIELDS)
Feed   = namedtuple('Feed', FEED_FIELDS)
Group  = namedtuple('Group', GROUP_FIELDS)


# Magic incantation to make all parameters to the initializers optional with a
# default value of None.
Data.__new__.__defaults__   = tuple(None for x in DATA_FIELDS)
Stream.__new__.__defaults__ = tuple(None for x in STREAM_FIELDS)
Feed.__new__.__defaults__   = tuple(None for x in FEED_FIELDS)
Group.__new__.__defaults__  = tuple(None for x in GROUP_FIELDS)


# Define methods to convert from dicts to the data types.
def _from_dict(cls, data):
    # Convert dict to call to class initializer (to work with the data types
    # base on namedtuple).  However be very careful to preserve forwards
    # compatibility by ignoring any attributes in the dict which are unknown
    # by the data type.
    #params = {x: data.get(x, None) for x in cls._fields}
    #
    #Modified to support Python 2.6 by krambriw 2015-02-19
    params = {}
    for x in cls._fields:
        params[x] = data.get(x, None)
    return cls(**params)


def _feed_from_dict(cls, data):
    #params = {x: data.get(x, None) for x in cls._fields}
    #
    #Modified to support Python 2.6 by krambriw 2015-02-19
    params = {}
    for x in cls._fields:
        params[x] = data.get(x, None)
     # Parse the stream if provided and generate a stream instance.
    params['stream'] = Stream.from_dict(data.get('stream', {}))
    return cls(**params)


def _group_from_dict(cls, data):
    #params = {x: data.get(x, None) for x in cls._fields}
    #
    #Modified to support Python 2.6 by krambriw 2015-02-19
    params = {}
    for x in cls._fields:
        params[x] = data.get(x, None)
    # Parse the feeds if they're provided and generate feed instances.
    params['feeds'] = tuple(map(Feed.from_dict, data.get('feeds', [])))
    return cls(**params)


# Now add the from_dict class methods defined above to the data types.
Data.from_dict   = classmethod(_from_dict)
Stream.from_dict = classmethod(_from_dict)
Feed.from_dict   = classmethod(_feed_from_dict)
Group.from_dict  = classmethod(_group_from_dict)
