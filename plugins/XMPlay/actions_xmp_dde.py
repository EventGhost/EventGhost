# -*- coding: utf-8 -*-
#

import eg
import re
import threading
from os import path
from dde_client_eg import DDEError, DMLERR_NOTPROCESSED, CF_TEXT
import utils_xmp



class Execute(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(): return False
        self.plugin.dde_get_conversation().execute("key%i" % self.value)
        return True



class ExecuteEx(eg.ActionBase):
    """Thorough check for extra DDE recovery posibility on essential actions."""
    def __call__(self):
        if self.plugin.is_xmp_off(thorough=True): return False
        self.plugin.dde_get_conversation().execute("key%i" % self.value)
        return True



class ExecuteUniversal(Execute, utils_xmp.IntSetter):
    """Indexing here begins from zero."""
    def __call__(self, value=0, from_eg_result=False):
        if from_eg_result:
            value = int(eg.result) # ValueError expected from users, its OK
        self.value = value
        return super(ExecuteUniversal, self).__call__()



class Request(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(): return
        # for XMPlay DDE requested item is meaningless
        try:
            # using CF_TEXT because XMPlay always returns UTF-8
            # this is incorrect, DDE supports only UTF-16LE unicode,
            # we must avoid CF_UNICODETEXT for XMPlay may be corrected.
            return self.plugin.dde_get_conversation("info%i" % self.value).request("info", format=CF_TEXT).rstrip("\0").decode("utf-8")
        except DDEError as e:
            # XMPlay refuses requests when it has empty info window
            # (i.e. always when playlist is empty XMPlay respond to DDEML with NULL).
            # We gracefuly ignore that one.
            if e.winerror != DMLERR_NOTPROCESSED:
                raise



class StoreMessage(Request):

    def __call__(self):
        # override automatic handling of the argument from actions list
        self.value = 1
        self.plugin.info_message = super(StoreMessage, self).__call__()
        return bool(self.plugin.info_message)



class SearchInMessage(StoreMessage, utils_xmp.TextSetter):

    def __call__(self, value="", from_eg_result=False):
        if from_eg_result:
            value = str(eg.result)
        if (value and (
            self.plugin.info_message or
            super(SearchInMessage, self).__call__()
            )):
            match = re.search(r"^.*?%s\t(.+?)(?:\r|\n|$)" % value, self.plugin.info_message, re.I|re.S)
            if match:
                return match.group(1)



class StoreGeneralDict(Request):

    def __init__(self):
        super(StoreGeneralDict, self).__init__()
        self.lock = threading.Lock()
        self.retval = False

    def __call__(self):
        if self.lock.acquire(False):
            try:
                self.retval = False
                # override automatic handling of the argument from actions list
                self.value = 0
                text = super(StoreGeneralDict, self).__call__()
                self.plugin.lock.acquire()
                try:
                    self.plugin.info_general = dict()
                    if not text:
                        return self.retval
                    # If the current file is resampled or downmixed
                    # to match the settings of the output device,
                    # the Output field will show the file's original
                    # sample rate and channel count between brackets.
                    prev_name = None
                    for line in text.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        # print line
                        # print line.encode("hex")
                        pair = line.split("\t", 1)
                        if len(pair) == 2:
                            name = pair[0].capitalize()
                            prev_name = name
                            if name in self.plugin.info_general:
                                self.plugin.info_general[name] += " " + pair[1]
                            else:
                                self.plugin.info_general[name] = pair[1]
                        else:
                            if prev_name:
                                self.plugin.info_general[prev_name] += " " + line
                            else:
                                self.plugin.info_general[line] = "" # extreme tolerance
                    self.retval = True
                except Exception as e:
                    #self.retval = False already
                    eg.PrintTraceback("Error processing XMPlay General Info text.")
                finally:
                    self.plugin.lock.release()
                return self.retval
            finally:
                self.lock.release()
        else:
            with self.lock:
                return self.retval



class SelectFromGeneral(StoreGeneralDict, utils_xmp.TextSetter):

    def __call__(self, value="", from_eg_result=False):
        if from_eg_result:
            value = str(eg.result)
        if (value and (
            self.plugin.info_general or
            super(SelectFromGeneral, self).__call__()
            )):
            self.plugin.lock.acquire()
            try:
                return self.plugin.info_general[value.capitalize()]
            except(KeyError):
                pass
            finally:
                self.plugin.lock.release()



def dde_command_list():
    file = open(path.join(path.dirname(__file__), 'dde_command_list.html'), 'r')
    r = file.read()
    file.close()
    return r


actions = (
    (ExecuteUniversal,
        "DDECommand",
        "DDE Command",
        dde_command_list(),
        None
    ),
    # contrary to documentation info tabs count begins not from 1, but from 0
    (Request, "GetGeneralInfo", "Get General Info", "Get the content of General tab of Info window.", 0),
    (Request, "GetMessageInfo", "Get Message Info", "Get the content of Message tab of Info window.", 1),
    (Request, "GetSamplesInfo", "Get Samples Info", "Get the content of Samples tab of Info window.", 2),
    (StoreMessage,
        "StoreMessage",
        "Store Message Info",
        "Store the content of Message tab of Info window.",
        None
    ),
    (SearchInMessage,
        "SearchInMessage",
        "Search in Message",
        ("Search value of the first matching item (tag) in the content of Message tab of Info window., "
        "e.g. \"Artist\". Item name is case insensitive. "
        "This action uses the cache of \"Store Message Info\" action - call that to refresh."),
        None),
    (StoreGeneralDict,
        "StoreGeneralDict",
        "Store General Info",
        "Store the content of General tab of Info window.",
        None
    ),
    (SelectFromGeneral,
        "SelectFromGeneral",
        "Select from General",
        ("Select value of the item in the content of General tab of Info window., e.g. \"Title\". "
        "Item name is case insensitive. "
        "This action uses the cache of \"Store General Info\" action - call that to refresh."),
        None),
)