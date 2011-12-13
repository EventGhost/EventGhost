# -*- coding: utf-8 -*-

version="0.0.4"

# plugins/WebsocketSuite/__init__.py
#
# Copyright (C)  2011 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.4 by Pako 2011-10-08 09:50 GMT+1
#     - fixed bug in the action "Stop all servers"
# 0.0.3 by Pako 2011-09-26 12:47 GMT+1
#     - added support for new ("latest") HyBi WebSocket protocol also on client side
# 0.0.2 by Pako 2011-09-25 09:12 GMT+1
#     - added support for new ("latest") HyBi WebSocket protocol (only on server side)
#     - (current websocket protocol used in Chrome: prot. Nr. 8)
# 0.0.1 by Pako 2011-09-18 15:01 GMT+1
#     - initial version
#===============================================================================

doc = u'''<rst>
**Websocket server, websocket client and persistent variables handler.**

In developing this plugin was used GNU library *"websocket" - Websocket client
library for Python, Copyright (C) 2010 Hiroki Ohtani (liris)*.

Was also used code published in the article `Threaded websocket python server
and javascript client <http://www.nublue.co.uk/blog/threaded-python-websocket-
server-and-javascript-client/>`_.

| **Since version 0.0.2:**
| Important information and several smaller pieces of code (especially on a new 
  "latest" WebSocket "HyBi" protocol) was obtained from an amazing project
  `pywebsocket <http://code.google.com/p/pywebsocket/>`_ .
  On that page you can also find a link to the `official detailed specification
  of websocket protocols
  <http://code.google.com/p/pywebsocket/wiki/WebSocketProtocolSpec>`_.

'''

eg.RegisterPlugin(
    name = "Websocket suite",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{A0152A67-1ACF-411C-9E74-CFE4DA54286F}",
    description = doc,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3458",
    icon = (
         "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAAK/INwWK6QAA"
         "ABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAtKSURBVHjaYvz//z/D"
         "QAKAAGJiGGAAEEAsMAZj4B4QycDw7zcDwx8gZmRmYPj9j4HhPxADEcO373oMbCzufNys"
         "xiKi3Bq8vJyi/37/+fP+3deX7169v/ntxc2TDA9W7GHg4LzB8PEiUZaDQh8ggFjwqvgH"
         "jJ6fvw3Z+bjKba3k3LxtZARNlLkY5ITYGXi5mBn+Ah32/ssfuZsvfpgev/Y5Zts+95cX"
         "juzbxPDjex/Dz1s3iHEEQAAxwtIARgj8Y2Rj+seQb2UsXZ8TqsbtrsvNIAB17l+gFmZG"
         "JJ8AMVAHw533DAwbjn9kWLjk6Mtb+5c2MrxcO4fh/8/f+EIAIICwO+DHT04OdvY5yWG6"
         "Uame0gzSHH8Z/vz5x8AIlOZkYwLGBBPDrz//Gb79+gumYYmJjYWR4TcTC8PxZwwM85Ze"
         "Y9g+f9pUhsdzqhgYfn3C5QCAAEKNAkZwsDOyc7D2Z8WZRvmbCTJw//vB8PzDP7A0MxMj"
         "A8cvoAOA3v/26z/QcqCjmJCC4gcDAwvzHwYNPiYGL19NBha2guytU97++fdiZQVEFhMA"
         "BBAiF/z9CwzH3wws/xjygjx10tVluRmYf3xheP3pN8O/f4wMfJysDFIC7AzSgmxAmhUc"
         "8B+//2X4/P0PEEPojz/+MLz7+o/hFzBkJJg+MkhqSTBYhublMHCZJOPKcQABhBD89weY"
         "4H4pWpnJtakq8jOIMH4AWvGfQZCHjUFGmJNBkJuVgY2VCRhsQB8D4+Lnb6DF334yfPr6"
         "k+Hdp28Mn778ZPgNtPjLtx8Mrz9+Z5DkYWCQZn7LoGatzaxgmw2MBh5LbA4ACCCEA4DZ"
         "jVuAq1RLQ4xr6/6TDPycTAwKEnwMfNzsDL+AMfATGEA//0B0vAKGyt2n7xnE+ViAIcPE"
         "wMHKyCDAwwoMwB8MHz59Zvj69SvDtx+/GNh/f2Q4ce4Cg62fqxSLsHksUDcPugMAAgiR"
         "Bn7/VdJTlwh49PQxwwegb65+5mMQ/gYMenYGBqDHwSkflEbuPf/IcPHWM7AFnz9/YmAC"
         "hoYAHxfDu/e/Gb4DxViBCfQnMG3sO3WDYdGuKwyfv/xgMFCRY5AyCvV9tHvvXKApp5Ed"
         "ABBAcAewcrF7yEuxSV6/eYvBxNiY4dVPdobd9xgYVAUZGGT5GRiEuYHZ7PYThmu37zOA"
         "Mg4j0OIfQAbIAZ8+vgO77su37wwPX3xk2HviCsON+68hifr3L4bbl48yaBibSj06qOrE"
         "8Os2qJT6BbMXIIDgDhDk4zBmAmYjFg5uBikleQZGoMxPoEU3gWY//wqMTwEGhuPnHjGc"
         "Pn6aQU5KlIGVlRnskO8/f4HTwKt3nxkePnvD8OHHfwYWVlZwycDMzMLwFxgqLx7cZTD2"
         "tWdg5Fc1+//6tghQ8hnMXoAAgjuAj49Ti4ODk+Hm2RMMz+/dYlDXNWLQM9JlEBHgY/j0"
         "E2gc0CGianoMLw5dYdi76ggDAwc7AxMLK7CU/g8pMYEhwQTMkiysLAzi0ooM34XEGQTF"
         "pRnu373F8PEvE7DU/MHAyisu9es1gzCyAwACCO4AfkEeiSe3LjJ8+/KV4ScwKF8+ecxw"
         "5cxJhuCEBAYZSSGGT8BczMPJwxCbGM9wzdScgZOLg+HcmQsM589fYGBnZwdHwX9wQfaX"
         "4fmjhwxCErIMLKIKDMWSHMAQuMXAyCcALBe4+YBhz4ucBgACCO4AJsb/wOKFmYGNgxdo"
         "IBuomGL48vEzw461GxnsPT0YpGQkGX58ZmBgZ2Vn0DbWZ2DnANUDvxmuXLnJ8J+dFxgI"
         "oJD4x/AHGBIyCkoMeo7ODArPbzKUv81muKWiybCeL5/hL7iGY2BHdgBAAMEd8O3rjw+S"
         "QlyyrOzc4GAEl3xsXAyvn79muHf/GQOfuCQwKwDFgCU103dgov0GNElAmIFJAFhUPzrB"
         "YPH2IgMnMLs8/svGwGZQzmDC9IwhgzWNgc/lMYPaBSYGoQ9PgcXML1C98B3ZAQABBHfA"
         "p3cf7/EoiuuygRzAzAIu6X5+/8Egr63HoGBgBCzhIBUQCIMSN7DEZfjKJsig+PQMQ/nf"
         "MwyhKX4MbD9+Mrx5/pLhwJ5OBjWuJwzC4S8Yvp/gYjjyPZvhHScwFX988d6WlVH28r//"
         "pz78BVfyDAABBC+I3rx7f42bh4+Bh5uXgRkYzIzMHAwiEpIMWvo6DNxsjOByFFT9ggoj"
         "YInL8AUYmCz3zzGUXFrCEOFkx8DOBAzZ528YRH+zM4TmszPoJ31j+HqPhaF0tjXDbIFI"
         "hvO33/2N4LrNv8uTabIDD4sHKOeD7AUIILgDvl/ZuO/l+7+/FRSkgcUsM4OmlipDdKI/"
         "g5qKDAMXUJUgJzChAu3g4wAlRmCt+OcHg968IoaIn1+AIQZMM2/eMPz48ZfhpzOwGRBw"
         "l+HbM06GS7PUGQTuPWUQub2fQePiRsapmXe1OTKZxHUFmTKAVoKyIwNAACGK4heHj525"
         "cPeksb4qAx+/AIOLgy6DEBcLAzcwNvjYIBjkAH4gLQAsmPgv7mXQBDaCwCnq9SsGUKr8"
         "AWxBXed7w/DlKyvD2R5hBrbnAgzlJuoM9ts6GUosW5mEgliZn5xgYzj6BpRvGYRAWgEC"
         "COGA70++PTu6eNrH78wMtqYqDL++/2LgBfkYDYNDARgCgic2MIgBtX1mAhpx+Qq4XBDg"
         "ACbAfVIMd1uEGTieCjOoABUz/fnOEFPPwCAV9J/h/hbW36m9P4/t+/JnA8jLIGsBAgil"
         "MmJ4uHHNmnV79kpLizL8BNZyPKz/GfiBQY6CgZbzAnVxPbvPwMnMxPBBXJzh/7VrwPh/"
         "zvAPGE+qr8UYFJ/IMqgKcwELnv8MHHlPGRh8vjA8283GUNDw6d6OL38WAm3bAsRvQdYC"
         "BBBqHf3n0++P+5pLV2049dhIV5xBhIcR6AighWxIocABCQVmYMsJVA/8FBRk+CYEDM3d"
         "uxkY2dgZ/nOyMIDKJbY/zAy3hN8x/HL7wfDqGBPDzRkSDML/+ASBMfoSFGkwKwECCLOR"
         "8PXm+bsba3PqJx15//ztbwZZYMEpyAWMMCAWAVZIQI8xiALTAIuYGLDR/I+BCYg/Kigw"
         "/P32jYHpxAkGZgFBhv/AaGEGtmy4n3Az3FjAyHCuhZVBnkmQwV9JWhRohCFyYQQQQNj7"
         "Be9Pbbq+MDkxt3b13c3ARiY/0NKvX/8zXLrzg+Htu9/AFs9/Bj5bB4aXwLTE9P07wy9g"
         "SLzX0WH4//QpA/OFCwyswsIMf7nZGMT/sTEIzhVnkPwswCAPTL2yXFyMQAeogUp+mFUA"
         "AYRolDIyYjqEVdyUQSGg3NIv3ldXV52NiYWT4e0nRgZGVg4Gvr8vGfQqDRk8/31mYJKW"
         "Y2CRkGDgBvpc4NUrBmZRUYZ/wFD5DWzi/Xn7nuH/n18MPEBHrTl/niH5+vUlwBZqOahC"
         "AtkNEED4HQABIgxsct7sat4RkupmxlIKKkIS4qLMjLxCDJxbJzGEbG1lMJAQZ/grKMTA"
         "KCDAwAZyxK9fDFzAtMEoCSy+OYGplpmZ4fKNGwz5Bw48PfDnTz/QxtmgwhdkN0AAEeMA"
         "WHsZaBqDJgObpC4DuzDQy5x8IFHPDxd1U5j/mukCaztWHh6Gv6ys4DKWHZg2BPn5GViA"
         "jjgPTB91R48+3/v791Kg1GIgvgxplf9nAAggYh2AEjFADEwVDBwgbcBULWjBwFDgzciY"
         "oMfGxiYJ9C1IwQ9gKDz784fhAjBE1v/7dxPYDNoItGkZUOoqKL/B+gUAAUSOA7ABbmBm"
         "8ZVhYPADZkhFYKDzACvLf8Dy8cMjBoZbXxgYjgLVAFsxDHehHSl4xwQggKjlAFg0gVo7"
         "4tDWL6juB7alGD5AS72v2HpGAAEGAGCU2kazZv+0AAAAAElFTkSuQmCC"
    )
)
#===============================================================================

import socket
import random
from os import urandom
from struct import pack, unpack
from threading import Thread
from hashlib import md5, sha1
import re
from select import select
import _winreg
from urlparse import urlparse
from time import sleep
from copy import deepcopy as cpy
from datetime import datetime as dt
from codecs import open as openFile
from cStringIO import StringIO
from base64 import b64decode, b64encode
from array import array
from wx.lib.mixins.listctrl import TextEditMixin, CheckListCtrlMixin
#===============================================================================

DEBUG = False
if DEBUG:
    log = eg.Print
else:
    def log(dummyMesg):
        pass
#===============================================================================

GUID_KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

OPTIONS = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADFUlEQVR42m2Sa0iTcRTG"
    "n9dN3UXn3JypS9NSUktTnJdSQcO8BElq0Ke8fCgocF8ioQ9hVAgGWZiBWJ8qK7WgQpOW"
    "puVyYlpeIG0aqWk6DZ3zMp3bu84bWqN64fDA4Ty/8/8//5fB5ldZWZlGUkEVRNVLVaZW"
    "qzX4z0ezBSQpVOWMQ7NGpVKdjI6OxuTkJHQ6HYxG4wWCXHGY4XMik8lOBwfvQnf3+zcM"
    "Nb2oGUy1zDBMS1JS0rbQ0FCYzWbU1tYu2O12b4JYNwElSqVfeUZGJrRaLfR6fTkHeCuV"
    "SpNpWzXN3KRqysk5GiiXy1FXV4+lpaWdBPhKc8dFItGjw4ezMDr6BX19fYM0G8cBNoqK"
    "Cvmtra8xMTHxisfjxeTl5cqEQiGd4AGsVqsnDR4ic31WViZ6enowPj7RRL2zBP7MAfS0"
    "MUQsFmNsbBxSqQckEgno6NC2v8G36WktwRIzM9KZ3g8fuSUPyVxA5g3uWhzgnEKhuHow"
    "NQV8Pv9XWDbWhpFiNYzt7ViMiETCrSoMDA2R+RtnLiSzZStYZjOcy3T0YkrXY3l+Htu6"
    "usA8eYzYmvMYu9+MqTVXTOXmmmk0nsyDjk/q+IxiUX9/rFSjuRQQEZQsCfGH1/5wOMlE"
    "6C4sg+hGFfoNswa6WjpBBv4BPHd1FZLU+RyMP+IWpIQrj4GTwh1DlfWAQITdL5thWt9A"
    "p65rwWaz5RGk7TfgjznhiHugEs4rZpiWTBD4e+HTqwGE1N6DUEwjdsBisULbqVuzWCz5"
    "BGlgyCzgzL5pB7IlO/3hvLoO4485CAIUGL3zzDB7Ir9kLTLyWlycysvD3Q0sy4LHd0ZH"
    "xzusrK6e5gAXfTOSSz33hMDFtIr5mRkIlDKM3H5qsLNsSvb6+jDlE0ZLWqOi9vlu9/NB"
    "X/8gYlQxaGx8scgBGiIuqY95+Hhjqk0HF5kb9NUNBruNTSXzkEPI20lehoWFhu8ICABr"
    "Z6HRtMxxgDgXqXvH3tIzLubvBgxX3P3H7ACRkDyRy2Vpi4smE/2luVshJpFcp1qjOvU/"
    "81+gRJIRCnH2J8AhWNbEhpsqAAAAAElFTkSuQmCC"
)

VARIABLES = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBB"
    "ZG9iZSBJbWFnZVJlYWR5ccllPAAAAbNJREFUeNqkk00ohEEYx//v+66QfKyXFeWrsEqt"
    "Qquc5cDVRRxIbdkTDq7OiBtbm6JEOTqIOMhhy1coKXKSj2XZ9bG07Mw7a+Zd3l2n3WXq"
    "aWaenv9/nvk1I0UiEfxnSEsjdjH38hjgYU9Cs83D1TW2u6wbLAw3VcmyfNHc2o5ctSCh"
    "OuC7w8HWBhhjtp7J/ROTprHhalsjsvPy8X57nNAgr8iGmvomnB7siI6d0qyz/s8Q+qeP"
    "JROlGjq6+3C2twG//+V3hZwGMPIrpaq5qLW3YXVxTt+bCNGgcZOb6wd0Do4ZhYfnj7h6"
    "+EBpYQYarDE2K65RVIY+IHS6AeULQhmCryFceub1JGEKTgJ1cDgccLvdyPGtIU2OCkQd"
    "4QfSHwMS5h0QiuBzCPdev3GS8q5gfHwCKrwIEJ+RF3U0TCF0RgeCg9mcjc31o7jbHiHC"
    "GbxxBpdx2bJyCyRZietAGGgMJaX5MFuyEkLMTE/X62MMaBTi03MwaYjhz0+9a+MKTEsN"
    "IouHyF8iRKQEkUY1UQO+4e8aanFZUhArrFbIigKh0z/TUIt55vsnpjpcU56A80uAAQCg"
    "vgjh0h3YTwAAAABJRU5ErkJggg=="
)

CMMNDS = (
    "GetValue",
    "SetValue",
    "ToggleBoolean",
    "IncrementInteger",
    "DecrementInteger",
)

KNOWN_TYPES = (
    'bool',
    'float',
    'int',
    'list',
    'str',
    'tuple',
    'unicode',
)
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================
def Move(lst,index,direction):
    tmpList = lst[:]
    max = len(lst)-1
    #Last to first position, other down
    if index == max and direction == 1:
        tmpList[1:] = lst[:-1]
        tmpList[0] = lst[max]
        index2 = 0
    #First to last position, other up
    elif index == 0 and direction == -1:
        tmpList[:-1] = lst[1:]
        tmpList[max] = lst[0]
        index2 = max
    else:
        index2 = index+direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2,tmpList


def GetInterfaces(txt):    
    cards=[txt.allIfaces,'localhost']
    try:
        y = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards")
        for i in range(_winreg.QueryInfoKey(y)[0]):
            yy = _winreg.OpenKey(y,_winreg.EnumKey(y,i))
            cards.append(_winreg.QueryValueEx(yy, "Description")[0])
            _winreg.CloseKey(yy)
    except:
        raise #ToDo
    _winreg.CloseKey(y)
    return cards


def GetIPAddress(card, txt):
    if card == 'localhost':
        return "127.0.0.1"
    if card == txt.allIfaces:
        return "0.0.0.0"
    cards=[]
    try:
        y = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards")
        for i in range(_winreg.QueryInfoKey(y)[0]):
            yy = _winreg.OpenKey(y,_winreg.EnumKey(y,i))
            desc = _winreg.QueryValueEx(yy, "Description")[0]
            name = _winreg.QueryValueEx(yy, "ServiceName")[0]
            cards.append([desc, name])
            _winreg.CloseKey(yy)
    except:
        raise #ToDo
    _winreg.CloseKey(y)

    guid = cards[[item[0] for item in cards].index(card)][1]
    yy = None
    try: 
        y = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\%s" % guid)
        try:
            yy = _winreg.QueryValueEx(y, "DhcpIPAddress")[0]
        except:
            try:
                yy = _winreg.QueryValueEx(y, "IPAddress")[0][0]
            except:
                pass
        _winreg.CloseKey(y)
    except:
        pass # Key Interface not found
    return yy
#===============================================================================

class Persist(eg.PersistentData):
    ccListPos = None
    protServDim = None
    userVariables = []
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class Text:
    prefix = "WebsocketSuite"
    iface = "Interface:"
    port = "TCP/IP port:"
    allIfaces = 'All available interfaces'
    host = "TCP/IP address:"
    mess = "Message to be sent"
    modeHostChoiceLabel = 'Server host address to specify as'
    modeHostChoice = (
        'Server title (or Python expression)',
        'Server title from eg.event.payload[0]',
        'Interface',
        'IP address (or Python expression)',
    )
    modeUserChoiceLabel = 'Client to specify as'
    modeUserChoice = (
        'Client title (or Python expression)',
        'Client title from eg.event.payload[0]',
        'Server IP address (or Python expression)',
    )
    modeClientChoiceLabel = 'Client address to specify as'
    modeClientChoice = (
        'Explicitly (or Python expression)',
        'From eg.event.payload[1]',
    )
    interactSrv = "Assigning server's class"
    interactCln = "Assigning client's class"
    default = "Default (triggering of events)"
    headerServ = "Websocket servers"
    protocolServ = "Server classes ..."
    headerCli = "Websocket clients"
    protocolCli = "Client classes ..."
    colLabelsServ = (
        "Server title",
        "IP address",
        "TCP/IP port",
        "Connected clients",
        "Server class",
    )
    colLabelsCli = (
        "Client title",
        "Local IP",
        "Local port",
        "Server IP",
        "Server port",
        "Client class",
    )
    clients = "Clients"
    abort = "Stop"
    abortAll = "Stop all"
    refresh = "Refresh"
    clientsMenu = "Show details of clients"
    abortMenu = "Stop selected server(s)"
    abortMenuCli = "Stop selected client(s)"
    abortAllMenu = "Stop all servers"
    abortAllMenuCli = "Stop all clients"
    servMessError = 'Server "%s" is not connected with the client %s'
    startError1 = 'Server named "%s" is already running.\nYou can not run two servers with the same name.'
    startError2 = 'You can not run a server of type "%s", when it is already running another server !'
    startError3 = 'If the server type "%s" is running, you can not run no other server !'
    startError5 = "Server %s:%i is already running !"
    servError1 = 'Server named "%s" is not running !'
    servError2 = "Server %s:%i is not running !"
    anotherPort = "You can use a port other than %i"   
    cliError1 = 'Client named "%s" is not running !'
    cliError2 = "Client %s:%i is not running !"
    cliStartErr1 = 'Client named "%s" is already running.\nYou can not run two clients with the same name.'
    cliStartErr3  = "Client %s:%i is already running !"
    ccHeader = (
        "Nr.",
        "IP address",
        "Port",
        "Protocol"
    )
    oldProt = "old"
    ccName = "Websocket-Connected clients"
    ccTitle = 'Server "%s" - connected clients'
    actHeader = (
        "Aut. at connection",
        "Websocket action title",
        "Plugin",
        "Action"
    )
    prot = 'Servers class that contains the selected variable to specify as'
    radioChoices  = (
        "Select from the list",
        "Explicitly (or Python expression)"
    )
    var  = "Variable to specify as"
    valLabel = "New value"
    vrbl = "Variable"
    type = "Type"        
    defVal = "Default value"
    clsList = "List of classes:"
    newCls  = "New/Selected class:"
    delete = "Delete"
    addNew = "Add new" 
    validLabel = "Behaviour on receipt of a known and valid command"
    validOptions = (
        "Just execute the command",
        "Execute the command and trigger an event"
    )
    invalidLabel = "Behaviour on receipt of an unknown or invalid command"
    invalidOptions = (
        "Trigger an event",
        'To relevant client send a message "Unknown / Invalid command"'
    )
    connectEvent = "Trigger an event when a client connect or disconnect"
    clnConnect = "ClientConnect"
    clnDisconnect = "ClientDisconnect"
    logLabel = "Log commands to following logfile:"
    options = "Options"
    userVars = "User variables:"
    colLabelsVars=('Variable name','Variable type','Variable value')  
    persVars = "Persistent variables"
    addNewItem = "Add new item"
    delSel = "Delete selected item"
    clearAll = "Clear all"
    clearAllItm = "Clear all items"
    moveUp = "Move item up"
    moveDown = "Move item down"
    ##refrVal = "Refresh values"
    testRes = "Action test"
    actions = "List of actions:"
    defVals = "Action's variables and its default values:"
    add = "Add"
    actPage = "Actions"
    autPerf = "Automatically perform at client connection"
    notRes = "The result not return to the client"
    srvClss = "Server classes"
    srvRecData = "ServerRecData"
    clnRecData = "ClientRecData"
    cmdRec = 'Command "%s" received from client %s'
    unknVar = u"Unknown variable: %s"
    unknVarMsg = 'Message "Unknown variable: %s" sent to the client %s'
    invCmd = "Invalid command: %s"
    invCmdMsg = 'Message "Invalid command: %s" sent to the client %s'
    broadMsg = 'Broadcast message "%s=%s"'
    unknCmd = u"Unknown command: %s"
    unknCmdMsg = 'Message "Unknown command: %s" sent to the client %s'
    connCln = 'Client connect %s'
    disconnCln = 'Client disconnect %s'
    msgToCln = 'Message "%s=%s" sent to the client %s'
    servStop = 'Server stopped'
    servStart = 'Server started'
    unknSrvCls = 'Unknown server class "%s" !'
    browseFolder = 'Select the folder'
    toolTipFolder = "Press button and browse to select folder ..."
    varTableTip = """This table has two functions:
1. You will find here the names of variables
2. Here you can define default values.
If the client does not send the values of some variables,
will be used here specified default values."""
    testToolTip = '''If you press this button,
in the adjoining box you see a result of the action.'''
    notBool = u'The variable "%s" is not of type "bool" !'
    notInt = u'The variable "%s" is not of type "int" !'
    notVar = 'Class "%s" does not contain a variable named "%s" !'
    invType = u'The variable "%s" is of type "%s", while the specified value "%s" is of type "%s" !'
    notName = 'Class "%s" does not contain a variable named "%s" !'    
#===============================================================================

class TableCtrl(wx.ListCtrl):

    def __init__(self, parent, labels):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.labels = labels
        self.InsertColumns()
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)


    def InsertColumns(self):
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        for i, colLabel in enumerate(self.labels):
            self.InsertColumn(i, colLabel)
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w += self.GetColumnWidth(i)
        self.SetSize((w, -1))


    def OnItemSelected(self, evt):
        self.SetSelection(evt.m_itemIndex)
        evt.Skip()


    def SetSelection(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def GetSelection(self):
        return self.selRow


    def FillData(self, data):
        self.selRow = -1
        self.DeleteAllItems()
        rows = len(data)
        for row in range(rows):
            self.InsertStringItem(row, data[row][0])
            for col in range(1, len(self.labels)):
                self.SetStringItem(row, col, data[row][col])


    def InsertRow(self, ix = None):
        ix = self.GetItemCount() if not ix else ix
        self.InsertStringItem(ix, "")
        self.EnsureVisible(ix)
        self.SetSelection(ix)


    def DeleteRow(self, ix):
        self.DeleteItem(ix)
        if self.GetItemCount():
            if ix:
                ix = ix-1        
            self.SetSelection(ix)
        else:
            self.selRow = -1
#===============================================================================

class CheckListCtrl(TableCtrl, CheckListCtrlMixin):

    def __init__(self, parent, labels):
        TableCtrl.__init__(
            self,
            parent,
            labels
        )
        CheckListCtrlMixin.__init__(self)


    def InsertColumns(self):
        for i  in range(len(self.labels)):
            self.InsertColumn(i, self.labels[i])
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        for i  in range(len(self.labels)-1,-1,-1):
            if i == 0:
                self.SetColumnWidth(i, 20 + self.GetTextExtent(self.labels[i])[0])
            if i == 1:
                self.SetColumnWidth(i, self.GetColumnWidth(3))
            else:
                self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w += self.GetColumnWidth(i)
        self.SetSize((w, -1))


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = eg.ValueChangedEvent(self.GetId(), value = (index, flag))
        wx.PostEvent(self, evt)


    def FillData(self, data):
        self.selRow = -1
        self.DeleteAllItems()
        rows = len(data)
        for row in range(rows):
            self.InsertStringItem(row, "")
            if data[row][0]:
                self.CheckItem(row)
            for col in range(1, len(self.labels)):
                self.SetStringItem(row, col, data[row][col])
#===============================================================================

class VarTable(wx.ListCtrl, TextEditMixin):

    def __init__(self, parent, txt):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_EDIT_LABELS,
        )
        self.edCell = None
        self.Show(False)
        TextEditMixin.__init__(self)
        self.editor.SetBackgroundColour(wx.Colour(135, 206, 255))
        self.SetToolTipString(txt.varTableTip)

        self.InsertColumn(0, txt.vrbl)
        self.InsertColumn(1, txt.type, wx.LIST_FORMAT_LEFT)        
        self.InsertColumn(2, txt.defVal, wx.LIST_FORMAT_LEFT)        
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertStringItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1] #header height
        hi = rect[3] #item height
        self.DeleteAllItems()
        self.w0 = self.GetColumnWidth(0)
        self.w1 = self.GetColumnWidth(1)
        self.w2 = self.GetColumnWidth(2)
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0] + self.w0 + self.w1 + self.w2
        width = self.wk
        rows = 10
        self.SetMinSize((width, 4 + hh + rows * hi))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Show(True)


    def SetWidth(self):
        w = (self.GetSize().width - self.wk)
        w0_ = w/3 + self.w0
        w1_ = w/3 + self.w1
        w2_ = (w - 2*w/3) + self.w2
        self.SetColumnWidth(0, w0_)
        self.SetColumnWidth(1, w1_)
        self.SetColumnWidth(2, w2_)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def FillData(self, data):
        self.DeleteAllItems()
        cnt = len(data)
        for i in range(cnt):
            self.InsertStringItem(i, data[i][0])
            self.SetStringItem(i, 1, data[i][1])
            self.SetStringItem(i, 2, data[i][2])
        self.Enable(cnt > 0)


    def OpenEditor(self, col, row): #Hack of default method
        # Only value and unknown type is editable!!!
        if col == 2 or col == 1 and self.GetItem(row,1).GetText() not in KNOWN_TYPES:
            self.edCell = (row, col, self.GetItem(row, col).GetText()) #Remember pos and value!!!
            TextEditMixin.OpenEditor(self, col, row)


    def CloseEditor(self, event = None): #Hack of default method
        TextEditMixin.CloseEditor(self, event)
        if not event:
            self.SetStringItem(*self.edCell) #WORKAROUND !!!
        elif isinstance(event, wx.CommandEvent):
            row, col, oldVal = self.edCell
            newVal = self.GetItem(row, col).GetText()
            evt = eg.ValueChangedEvent(self.GetId(), value = (row, col, newVal))
            wx.PostEvent(self, evt)


    def OnItemSelected(self, event): #Hack of default method
        self.SetItemState(event.m_itemIndex, 0, wx.LIST_STATE_SELECTED)
        TextEditMixin.OnItemSelected(self, event)


    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            data.append([
                self.GetItemText(row),
                self.GetItem(row, 1).GetText(),
                self.GetItem(row, 2).GetText()
            ])
        return data
#===============================================================================

class Protocol(wx.Frame):
    oldSel = 0

    def __init__(self, parent, plugin, title):
        size = (450, 300)
        self.plugin = plugin
        self.text = self.plugin.text
        wx.Frame.__init__(
            self,
            parent,
            -1,
            title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER|wx.MAXIMIZE_BOX ,
            name = title
        )
        self.panel = parent
        self.dataSet = cpy(self.panel.dataSet)
        if self.dataSet == []:
            self.panel.persist = []
        for p, prot in enumerate(self.panel.persist):
            for v, var in enumerate(prot[1]):
                self.dataSet[p][1][v][2] = unicode(var[1])
        self.plugin.protocolServDialog = self
        self.ctrls = {}
        self.plugins = None
        self.actions = None
        self.data = None
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.SetBackgroundColour(wx.NullColour)
        self.notebook = wx.Notebook(self)
        self.buttonRow = eg.ButtonRow(
            self,
            (wx.ID_OK, wx.ID_CANCEL),
#            (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY),
            True
        )
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(size)
        vgap = 1
        topSizer = wx.GridBagSizer(vgap, 6)
        topSizer.AddGrowableCol(1,1)
        topSizer.AddGrowableCol(4,1)
        listLbl=wx.StaticText(self, -1, self.text.clsList)
        labelLbl=wx.StaticText(self, -1, self.text.newCls)
        labelCtrl=wx.TextCtrl(self,-1,'')
        self.ctrls["labelCtrl"] = labelCtrl
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, -1, bmp)
        btnUP.Enable(False)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, -1, bmp)
        btnDOWN.Enable(False)
        #Buttons 'Delete' and 'Insert new'
        btnDEL=wx.Button(self,-1,self.text.delete)
        btnApp=wx.Button(self,-1,self.text.addNew)
        eg.EqualizeWidths((btnDEL, btnApp))
        btnDEL.Enable(False)
        h = 2 * vgap + labelCtrl.GetSize().height + 2 * btnUP.GetSize().height
        listBoxCtrl=wx.ListBox(
            self,-1,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            size = (-1, h)
        )
        topSizer.Add(listLbl,(0,0))
        topSizer.Add(listBoxCtrl,(1,0),(3,2),flag = wx.EXPAND)
        topSizer.Add(labelLbl,(0,2),(1,2))
        topSizer.Add(labelCtrl,(1,2),(1,3),flag = wx.EXPAND)
        topSizer.Add(btnUP,(2,2))
        topSizer.Add(btnDOWN,(3,2))
        topSizer.Add(btnDEL,(2,3))
        topSizer.Add(btnApp,(3,3))


        def boxEnable(enable):
            self.notebook.Enable(enable)
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)


        def validation():
            flag = True
            label = labelCtrl.GetValue()
            if label == "":
                flag = False
            elif [n[0] for n in self.dataSet].count(label)!=1:
                    flag = False
            btnApp.Enable(flag)


        def OnTxtChange(evt):
            if self.dataSet<>[]:
                ix = self.oldSel
                label = labelCtrl.GetValue()
                self.dataSet[ix][0] = label
                listBoxCtrl.Set([n[0] for n in self.dataSet])
                listBoxCtrl.SetSelection(ix)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)


        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip()<>"":
                if [n[0] for n in self.dataSet].count(label)==1:
                    self.oldSel=sel
                    item = self.dataSet[sel]
                    self.setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)


        def onButtonUp(evt):
            sel = listBoxCtrl.GetSelection()
            newSel,self.dataSet=Move(self.dataSet,sel,-1)
            listBoxCtrl.Set([n[0] for n in self.dataSet])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            sel = listBoxCtrl.GetSelection()
            newSel,self.dataSet=Move(self.dataSet,sel,1)
            listBoxCtrl.Set([n[0] for n in self.dataSet])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)


        def onButtonDelete(evt):
            lngth = len(self.dataSet)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.dataSet=[]
                self.notebook.SetSelection(0)
                self.ctrls["valid_rb1"].SetValue(True)
                self.ctrls["valid_rb2"].SetValue(False)
                self.ctrls["invalid_chb1"].SetValue(True)
                self.ctrls["invalid_chb2"].SetValue(False)
                self.ctrls["connCheckBox"].SetValue(False)
                self.setLogDir(None)
                labelCtrl.ChangeValue("")
                listBoxCtrl.Set([])
                boxEnable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                self.oldSel = -1
                evt.Skip()
                return
            elif lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            if sel == lngth - 1:
                sel -= 1
            ix = listBoxCtrl.GetSelection()
            tmp = self.dataSet.pop(ix)
            listBoxCtrl.Set([n[0] for n in self.dataSet])
            self.oldSel = sel
            listBoxCtrl.SetSelection(sel)
            item = self.dataSet[sel]
            self.setValue(item)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def OnButtonAppend(evt):
            self.Tidy()
            labelCtrl.ChangeValue("")
            item = ['',[],[],[False, True, False, None, False]]
            if len(self.dataSet)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            ix = listBoxCtrl.GetSelection() + 1
            self.oldSel = ix
            self.dataSet.insert(ix, item)
            self.setValue(item)
            listBoxCtrl.Set([n[0] for n in self.dataSet])
            listBoxCtrl.SetSelection(ix)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
        mainSizer.AddMany(
            (
                (topSizer,0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, 5),
                (self.notebook, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, 5),
            )
        )
        self.mainSizer = mainSizer
        self.notebook.SetSizer(self.sizer)
        self.add_Id = wx.NewId() 
        self.optPanel = self.CreateOptionsPanel()
        self.varPanel = self.CreateVarPanel()
        self.actPanel = self.CreateActionPanel()

        il = wx.ImageList(16, 16)
        stream_op = StringIO(b64decode(OPTIONS))
        idx0 = il.Add(wx.BitmapFromImage(wx.ImageFromStream(stream_op)))
        stream_var = StringIO(b64decode(VARIABLES))
        idx1 = il.Add(wx.BitmapFromImage(wx.ImageFromStream(stream_var)))
        idx2 = il.Add(eg.Icons.ACTION_ICON.GetBitmap())
        self.notebook.AssignImageList(il)
        self.notebook.SetPageImage(0, idx0)
        self.notebook.SetPageImage(1, idx1)
        self.notebook.SetPageImage(2, idx2)

        if len(self.dataSet) > 0:
            listBoxCtrl.Set([n[0] for n in self.dataSet])
            listBoxCtrl.SetSelection(0)
            self.setValue(self.dataSet[0])
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)

        self.FinishSetup()
        if Persist.protServDim:
            self.SetDimensions(*Persist.protServDim)
        else:
            self.Center()
        self.MakeModal(True)
        self.Show(True)
#-------------------------------------------------------------------------------
#                         Common functions                                     -
#-------------------------------------------------------------------------------

    def FinishSetup(self):
        # Temporary hack to fix button tabulator ordering problems.
        buttonRow = self.buttonRow
        #buttonRow.applyButton.MoveAfterInTabOrder(self.notebook)
        buttonRow.cancelButton.MoveAfterInTabOrder(self.notebook)
        buttonRow.okButton.MoveAfterInTabOrder(self.notebook)
        self.mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND, 0)
        self.SetSizerAndFit(self.mainSizer)
        self.Fit() # without the addition Fit(), some dialogs get a bad size
        self.SetMinSize(self.GetSize())
        self.CentreOnParent()


    def setValue(self, item):
        self.ctrls["labelCtrl"].ChangeValue (item[0])
        #Page "Options":
        self.ctrls["valid_rb1"].SetValue(not item[3][0])
        self.ctrls["valid_rb2"].SetValue(item[3][0])
        self.ctrls["invalid_chb1"].SetValue(item[3][1])
        self.ctrls["invalid_chb2"].SetValue(item[3][2])
        self.ctrls["connCheckBox"].SetValue(item[3][4])
        self.setLogDir(item[3][3])
        #Page "Actions":
        self.ctrls["grid"].FillData(item[2])
        self.enableActCtrls(len(item[2]))
        if len(item[2]):
            self.onGridClick(sel = 0)
        self.ctrls["btnAdd"].Enable(True)    
        #Page "Variables":
        ix = self.dataSet.index(item)
        self.ctrls["userVars"].FillData(item[1])
        self.enableVarCtrls(len(item[1]))
        if len(item[1]):
            self.onUserVarClick(sel = 0)
        self.enableVarBtnAdd(True)          


    def Tidy(self):
        self.ctrls["grid"].FillData([])
        self.ctrls["varTable"].FillData([])
        self.ctrls["plgnsCtrl"].SetSelection(-1)
        self.ctrls["actnsCtrl"].SetSelection(-1)
        self.ctrls["labelText"].ChangeValue("")
        self.oldSel = 0


    @eg.LogIt
    def OnMaximize(self, event):
        if self.buttonRow.sizeGrip:
            self.buttonRow.sizeGrip.Hide()
        self.Bind(wx.EVT_SIZE, self.OnRestore)
        event.Skip()


    @eg.LogIt
    def OnRestore(self, event):
        if not self.IsMaximized():
            self.Unbind(wx.EVT_SIZE)
            if self.buttonRow.sizeGrip:
                self.buttonRow.sizeGrip.Show()
        event.Skip()


    def OnOK(self, evt):
        self.panel.dataSet = cpy(self.dataSet)
        self.panel.persist = [[item[0], item[1]] for item in self.dataSet]
        for p, prot in enumerate(self.panel.persist):
            for v, var in enumerate(prot[1]):
                if var[1] == 'str':
                    tmp = str(var[2])
                elif var[1] != 'unicode':
                    tmp = eval(var[2])
                else:
                    tmp = var[2]
                var.pop(1)
                var[1] = tmp
            self.panel.persist[p] = prot                
        self.OnCancel(evt)


    def OnCancel(self, evt):
        self.MakeModal(False)
        self.GetParent().Raise()
        selfDim = list(self.GetPosition())
        selfSiz = self.GetSizeTuple()
        selfDim.extend(selfSiz)
        if selfDim != Persist.protServDim:
            Persist.protServDim = selfDim
        self.plugin.protocolServDialog = None
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)
        evt.Skip()

#*******************************************************************************        
#                              Page "Options"                                  *
#*******************************************************************************        
    def CreateOptionsPanel(self):
        if len(self.dataSet):
            options = self.dataSet[self.oldSel][3]
        else:
            options = [False, True, False, None, False]
        panel = wx.Panel(self.notebook)
        panel.SetBackgroundColour((255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        validSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.validLabel),
            wx.VERTICAL
        )
        valid_rb1 = wx.RadioButton(panel, -1, self.text.validOptions[0], style=wx.RB_GROUP)
        self.ctrls["valid_rb1"] = valid_rb1
        valid_rb1.SetValue(not options[0])
        valid_rb1.Bind(wx.EVT_RADIOBUTTON, self.onValidRadio)
        valid_rb2 = wx.RadioButton(panel, -1, self.text.validOptions[1])
        self.ctrls["valid_rb2"] = valid_rb2
        valid_rb2.SetValue(options[0])
        valid_rb2.Bind(wx.EVT_RADIOBUTTON, self.onValidRadio)
        validSizer.Add(valid_rb1)
        validSizer.Add(valid_rb2,0,wx.TOP,8)
        invalidSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.invalidLabel),
            wx.VERTICAL
        )
        invalid_chb1 = wx.CheckBox(panel, -1, self.text.invalidOptions[0])
        self.ctrls["invalid_chb1"] = invalid_chb1
        invalid_chb1.SetValue(options[1])
        invalid_chb1.Bind(wx.EVT_CHECKBOX, self.onInvalidCheck1)
        invalid_chb2 = wx.CheckBox(panel, -1, self.text.invalidOptions[1])
        self.ctrls["invalid_chb2"] = invalid_chb2
        invalid_chb2.SetValue(options[2])
        invalid_chb2.Bind(wx.EVT_CHECKBOX, self.onInvalidCheck2)
        invalidSizer.Add(invalid_chb1)
        invalidSizer.Add(invalid_chb2,0,wx.TOP,8)
        connCheckBox = wx.CheckBox(panel, -1, self.text.connectEvent)
        connCheckBox.SetValue(options[4])
        self.ctrls["connCheckBox"] = connCheckBox
        connCheckBox.Bind(wx.EVT_CHECKBOX, self.onConnCheckBox)
        logDirCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseFolder,
            buttonText = eg.text.General.browse,
            changeCallback = self.ldcCallback,
            newDirectory = True
        )
        self.ctrls["logDirCtrl"] = logDirCtrl
        editBox = logDirCtrl.GetTextCtrl()
        editBox.SetEditable(False)
        logCheckBox = wx.CheckBox(panel, -1, self.text.logLabel)
        self.ctrls["logCheckBox"] = logCheckBox
        logCheckBox.Bind(wx.EVT_CHECKBOX, self.onLogCheckBox)
        self.setLogDir(options[3])
        sizeLst=[
            valid_rb1.GetTextExtent(
                u"%s\\EventGhost\\Websocket_<<Server title>>_log.txt" % unicode(eg.folderPath.RoamingAppData)
            )[0]
        ]
        for item in self.text.validOptions:
            sizeLst.append(valid_rb1.GetTextExtent(item)[0])
        for item in self.text.invalidOptions:
            sizeLst.append(valid_rb1.GetTextExtent(item)[0])
        w = 50 + max(sizeLst)
        validSizer.SetMinSize((w,-1))
        invalidSizer.SetMinSize((w,-1))
        logDirCtrl.SetMinSize((w,-1))
        sizer.Add((1, 8))
        sizer.Add(validSizer, 0, wx.TOP|wx.LEFT,8)
        sizer.Add((1, 16))
        sizer.Add(invalidSizer, 0, wx.TOP|wx.LEFT,8)
        sizer.Add((1, 8))
        sizer.Add(connCheckBox, 0, wx.TOP|wx.LEFT,8)
        sizer.Add((1, 8))
        sizer.Add(logCheckBox, 0, wx.TOP|wx.LEFT,8)
        sizer.Add(logDirCtrl, 0, wx.LEFT,8)
        self.notebook.AddPage(panel, self.text.options)
        return panel


    def setLogDir(self, logdir):
        logDirCtrl = self.ctrls["logDirCtrl"]
        if logdir is None:
            logDirCtrl.startDirectory = u"%s\\EventGhost" % unicode(eg.folderPath.RoamingAppData)
            logDirCtrl.GetTextCtrl().SetValue("")
        else:
            logDirCtrl.startDirectory = logdir
            logDirCtrl.GetTextCtrl().SetValue(logdir)
        flag = logdir is not None
        self.ctrls["logCheckBox"].SetValue(flag)
        logDirCtrl.Enable(flag)


    def ldcCallback(self, evt):
        logDirCtrl = self.ctrls["logDirCtrl"]
        str = evt.GetString()
        if str:
            end = "\\Websocket_<<Server title>>_log.txt"
            if not str.endswith(end):
                self.dataSet[self.oldSel][3][3] = str
                logDirCtrl.startDirectory = str
                str = u"%s%s" % (evt.GetString(), end)
                logDirCtrl.GetTextCtrl().SetValue(str)
        evt.Skip()


    def onConnCheckBox(self, evt):
        self.dataSet[self.oldSel][3][4] = evt.IsChecked()
        evt.Skip()


    def onLogCheckBox(self, evt):
        logDirCtrl = self.ctrls["logDirCtrl"]
        flag = evt.IsChecked()
        logDirCtrl.Enable(flag)
        if not flag:
            self.dataSet[self.oldSel][3][3] = None
            logDirCtrl.SetValue("")
        else:
            logdir = u"%s\\EventGhost" % unicode(eg.folderPath.RoamingAppData)
            self.dataSet[self.oldSel][3][3] = logdir
            logDirCtrl.startDirectory = logdir
            logDirCtrl.SetValue(logdir)
        evt.Skip()


    def onValidRadio(self, evt):
        self.dataSet[self.oldSel][3][0] = self.ctrls["valid_rb2"].GetValue()
        evt.Skip()


    def onInvalidCheck1(self, evt):
        self.dataSet[self.oldSel][3][1] = self.ctrls["invalid_chb1"].GetValue()
        evt.Skip()

    def onInvalidCheck2(self, evt):
        self.dataSet[self.oldSel][3][2] = self.ctrls["invalid_chb2"].GetValue()
        evt.Skip()

#*******************************************************************************        
#                          Page "Variables"                                    *
#*******************************************************************************        
    def CreateVarPanel(self):
        panel = wx.Panel(self.notebook)
        panel.SetBackgroundColour((255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        userVarsLbl = wx.StaticText(panel, -1, self.text.userVars)
        userVars = TableCtrl(panel, self.text.colLabelsVars)
        self.ctrls["userVars"] = userVars
        w0 = userVars.GetColumnWidth(0)
        w1 = userVars.GetColumnWidth(1)
        w2 = userVars.GetColumnWidth(2)
        userVars.InsertRow(0)
        rect = userVars.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        varName = wx.TextCtrl(panel, -1, "")
        self.ctrls["varName"] = varName
        varName.Bind(wx.EVT_TEXT, self.onVarName)
        varType = wx.Choice(panel, -1, choices = KNOWN_TYPES)
        self.ctrls["varType"] = varType
        varType.Bind(wx.EVT_CHOICE, self.onVarType)
        panel.varDel_Id = wx.NewId()
        panel.varAdd_Id = wx.NewId()
        panel.varClear_Id = wx.NewId()
        ##panel.varRefr_Id = wx.NewId()
        panel.varUp_Id = wx.NewId()
        panel.varDown_Id = wx.NewId()
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUp = wx.BitmapButton(panel, panel.varUp_Id, bmp)
        self.ctrls["btnUp"] = btnUp
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDown = wx.BitmapButton(panel, panel.varDown_Id, bmp)
        self.ctrls["btnDown"] = btnDown
        #Buttons 'Delete', 'Clear all' and 'Insert new'
        btnDel=wx.Button(panel,panel.varDel_Id,self.text.delete)
        self.ctrls["btnDel"] = btnDel
        btnApp=wx.Button(panel,panel.varAdd_Id,self.text.addNew)
        self.ctrls["btnApp"] = btnApp
        btnClear=wx.Button(panel,panel.varClear_Id,self.text.clearAll)
        self.ctrls["btnClear"] = btnClear
        ##btnRefresh=wx.Button(panel,panel.varRefr_Id,self.text.refresh)
        ##self.ctrls["btnRefresh"] = btnRefresh
        ##eg.EqualizeWidths((btnDel, btnApp, btnClear, btnRefresh))
        eg.EqualizeWidths((btnDel, btnApp, btnClear))
        varSizer = wx.GridBagSizer(vgap = 1, hgap = 1)
        varSizer.AddGrowableRow(6)
        varSizer.AddGrowableCol(0,w0)
        varSizer.AddGrowableCol(1,w1)
        varSizer.AddGrowableCol(2,w2)
        sizer.Add(varSizer, 1, wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        varSizer.Add(userVarsLbl, (0,0),(1,3),flag = wx.EXPAND|wx.LEFT,border = 2)
        varSizer.Add(userVars, (1,0),(6,3),flag = wx.EXPAND|wx.LEFT,border = 2)
        varSizer.Add(varName,(8,0),flag = wx.EXPAND|wx.LEFT,border = 2)
        varSizer.Add(varType,(8,1),flag = wx.EXPAND)

        panel.val_Id = wx.NewId()
        wx.EVT_TEXT(panel, panel.val_Id, self.onVarValue)
        wx.EVT_CHOICE(panel, panel.val_Id, self.onVarValue)
        self.CreateVarValCtrl('txt', panel, varSizer)
        
        varSizer.Add((5,5),(7,0))
        varSizer.Add((5+SYS_VSCROLL_X + userVars.GetWindowBorderSize()[0],-1),(5,3),flag = wx.EXPAND)
        varSizer.Add(btnUp,(1,4), flag = wx.TOP, border = rect[1])
        varSizer.Add(btnDown,(2,4),flag = wx.TOP|wx.BOTTOM,border = 5)
        varSizer.Add(btnDel,(3,4),flag = wx.TOP|wx.BOTTOM,border = 5)
        varSizer.Add(btnClear,(4,4),flag = wx.TOP|wx.BOTTOM,border = 5)
        ##varSizer.Add(btnRefresh,(5,4),flag = wx.TOP|wx.BOTTOM,border = 5)
        varSizer.Add(btnApp,(8,4),flag = wx.RIGHT,border = 2)

        btnUp.Bind(wx.EVT_BUTTON, self.OnUserVarsUp)
        btnDown.Bind(wx.EVT_BUTTON, self.OnUserVarsDown)
        btnDel.Bind(wx.EVT_BUTTON, self.OnUserVarsDelButton)
        btnApp.Bind(wx.EVT_BUTTON, self.onVarBtnAdd)
        btnClear.Bind(wx.EVT_BUTTON, self.OnUserVarsClear)
        ##btnRefresh.Bind(wx.EVT_BUTTON, self.OnUserVarsRefresh)
        panel.Bind(wx.EVT_SIZE, self.OnVarSize)
        userVars.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onUserVarClick)
        userVars.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onUserVarRightClick)

        self.notebook.AddPage(panel, self.text.persVars)
        return panel


    def onUserVarRightClick(self, evt): #Right click menu
        panel = evt.GetEventObject().GetParent()
        userVars = self.ctrls["userVars"]
        sel = evt.m_itemIndex
        userVars.SetSelection(sel)
        if not hasattr(userVars, "menu"):
            userVars.menu = None
            userVars.Bind(wx.EVT_MENU, self.OnUserVarsDelButton, id = panel.varDel_Id)
            userVars.Bind(wx.EVT_MENU, self.OnUserVarsUp, id = panel.varUp_Id)
            userVars.Bind(wx.EVT_MENU, self.OnUserVarsDown, id = panel.varDown_Id)
            userVars.Bind(wx.EVT_MENU, self.onVarBtnAdd, id = panel.varAdd_Id)
            userVars.Bind(wx.EVT_MENU, self.OnUserVarsClear, id = panel.varClear_Id)
            ##userVars.Bind(wx.EVT_MENU, self.OnUserVarsRefresh, id = panel.varRefr_Id)
        menu = wx.Menu()
        menu.Append(panel.varAdd_Id, self.text.addNewItem)
        menu.Append(panel.varDel_Id, self.text.delSel)
        menu.Append(panel.varClear_Id, self.text.clearAllItm)
        menu.AppendSeparator()                
        menu.Append(panel.varUp_Id, self.text.moveUp)
        menu.Append(panel.varDown_Id, self.text.moveDown)
        menu.AppendSeparator()                
        ##menu.Append(panel.varRefr_Id, self.text.refrVal)
        userVars.PopupMenu(menu)
        menu.Destroy()
        evt.Skip()


    def onUserVarClick(self, evt = None, sel = 0):
        sel = evt.m_itemIndex if evt else sel
        self.ctrls["userVars"].SetSelection(sel)
        ix = self.oldSel
        data = self.dataSet[ix][1][sel]
        self.ctrls["varName"].ChangeValue(data[0])
        self.ctrls["varName"].Enable(True)
        varType = self.ctrls["varType"]
        varType.SetStringSelection(data[1])
        varType.Enable(True)
        self.onVarType()
        varValue = self.ctrls["varValue"]
        varValue.Enable(True)
        if isinstance(varValue, wx.TextCtrl):
            varValue.ChangeValue(data[2])
        else:
            varValue.SetStringSelection(data[2])
        if evt:
            evt.Skip()


    def onVarBtnAdd(self, evt):
        self.enableVarCtrls(False)
        self.ctrls["varName"].Enable(True)
        self.ctrls["varType"].Enable(True)
        userVars = self.ctrls["userVars"]
        ix = self.oldSel
        sel = userVars.GetSelection() + 1
        userVars.InsertRow(sel)
        item = ["","",""]
        self.dataSet[ix][1].insert(sel, item)
        self.enableVarBtnAdd(False)
        evt.Skip()


    def SetVarWidth(self, panel):        
        w0 = self.ctrls["varName"].GetSize()[0]+1
        w1 = self.ctrls["varType"].GetSize()[0]+1
        w2 = self.ctrls["varValue"].GetSize()[0]+1
        userVars = self.ctrls["userVars"]
        userVars.SetSize((w0 + w1 + w2 + SYS_VSCROLL_X + userVars.GetWindowBorderSize()[0], -1))
        userVars.SetColumnWidth(0, w0)
        userVars.SetColumnWidth(1, w1)
        userVars.SetColumnWidth(2, w2)
        panel.Update()


    def OnVarSize(self, event):
        wx.CallAfter(self.SetVarWidth, event.GetEventObject())
        event.Skip()


    def enableVarBtnAdd(self, flag):
        self.ctrls["btnApp"].Enable(flag)
        flag = flag if not flag else self.ctrls["userVars"].GetItemCount()
        self.ctrls["btnClear"].Enable(flag)
        ##self.ctrls["btnRefresh"].Enable(flag)
        self.ctrls["btnDel"].Enable(flag)
        self.ctrls["btnUp"].Enable(flag)
        self.ctrls["btnDown"].Enable(flag)


    def VarComplete(self):
        flag = True
        if self.ctrls["varName"].GetValue() == "":
            flag = False
        if self.ctrls["varType"].GetSelection() == -1:
            flag = False
        varValue = self.ctrls["varValue"]
        if isinstance(varValue, wx.Choice) and varValue.GetSelection() == -1:
            flag = False
        elif isinstance(varValue, wx.TextCtrl) and varValue.GetValue() == "":
            flag = False       
        btnApp = self.ctrls["btnApp"]
        if flag and not btnApp.IsEnabled():
            self.enableVarBtnAdd(True)
        
    
    def enableVarCtrls(self, flag):
        self.ctrls["varName"].Enable(flag)
        self.ctrls["varType"].Enable(flag)
        varValue = self.ctrls["varValue"]
        varValue.Enable(flag)
        self.ctrls["varName"].ChangeValue("")
        self.ctrls["varType"].SetSelection(-1)
        if isinstance(varValue, wx.Choice):
            varValue.SetSelection(-1)
        else:
            varValue.ChangeValue("")


    def OnUserVarsUpDown(self, dir):
        userVars = self.ctrls["userVars"]
        ix = self.oldSel
        sel = userVars.GetSelection()       
        newSel,self.dataSet[ix][1]=Move(self.dataSet[ix][1],sel,dir)
        userVars.FillData(self.dataSet[ix][1])
        userVars.SetSelection(newSel)


    def OnUserVarsUp(self, dir):
        self.OnUserVarsUpDown(-1)


    def OnUserVarsDown(self, dir):
        self.OnUserVarsUpDown(1)


    def OnUserVarsDelButton(self, evt):
        userVars = self.ctrls["userVars"]
        ix = self.oldSel
        sel = userVars.GetSelection()
        self.dataSet[ix][1].pop(sel)
        userVars.DeleteItem(sel)
        if sel == userVars.GetItemCount():
            sel = 0
        userVars.SetSelection(sel)
        self.onUserVarClick(sel = sel)
        evt.Skip()


    ##def OnUserVarsRefresh(self, evt):
    ##    print "OnUserVarsRefresh"
    ##    evt.Skip()


    def OnUserVarsClear(self, evt):
        self.dataSet[self.oldSel][1] = []
        self.ctrls["userVars"].FillData([])
        self.enableVarCtrls(0)
        evt.Skip()


    def CreateVarValCtrl(self, ctrlType, panel = None, varSizer = None):
        sz = (-1,-1)
        if not varSizer:
            varValue = self.ctrls["varValue"]
            panel = varValue.GetParent()
            varSizer = panel.GetSizer().GetItem(0).GetSizer()
            sz = varValue.GetSizeTuple()
            varSizer.Detach(varValue)
            varValue.Destroy()
        if ctrlType == 'txt':
            ctrl = wx.TextCtrl(panel, panel.val_Id, "", size = sz)
        else:
            ctrl = wx.Choice(panel, panel.val_Id, choices = ("True", "False"), size = sz)
        varSizer.Add(ctrl,(8,2),flag = wx.EXPAND)
        self.ctrls["varValue"] = ctrl
        varSizer.Layout()
        self.SetVarWidth(panel)
        return ctrl


    def onVarName(self, evt):
        name = evt.GetString()
        userVars = self.ctrls["userVars"]
        sel = userVars.GetSelection()
        userVars.SetStringItem(sel, 0, name)
        self.dataSet[self.oldSel][1][sel][0] = name
        self.VarComplete()
        evt.Skip()


    def onVarType(self, evt = None):
        type = self.ctrls["varType"].GetStringSelection()
        varValue = self.ctrls["varValue"]
        if isinstance(varValue, wx.TextCtrl) and type == 'bool':
            varValue = self.CreateVarValCtrl('bool')
        elif isinstance(varValue, wx.Choice) and type != 'bool':
            varValue = self.CreateVarValCtrl('txt')
        if evt:
            varValue.Enable(True)
            userVars = self.ctrls["userVars"]
            sel = userVars.GetSelection()
            userVars.SetStringItem(sel, 1, type)
            self.dataSet[self.oldSel][1][sel][1] = type
            self.VarComplete()
            varValue.SetFocus()
            if evt:
                evt.Skip()


    def onVarValue(self, evt):
        value = evt.GetString()
        userVars = self.ctrls["userVars"]
        sel = userVars.GetSelection()
        userVars.SetStringItem(sel, 2, value)
        type = self.ctrls["varType"].GetStringSelection()
        self.dataSet[self.oldSel][1][sel][2] = value
        self.VarComplete()
        evt.Skip()                    

#   ************************************************************************
#   *                          Page "Actions"                              *
#   ************************************************************************        

    def CreateActionPanel(self):
        panel = wx.Panel(self.notebook)
        panel.SetBackgroundColour((255, 255, 255))
        self.plugins  = dict([(eg.plugins.__dict__[item].plugin.name,item) for item in eg.plugins.__dict__.keys()])
        choices = self.plugins.keys()
        choices.sort()
        grid = CheckListCtrl(panel, self.text.actHeader)
        self.ctrls["grid"] = grid
        varTable = VarTable(panel, self.text)
        self.ctrls["varTable"] = varTable
        plgnsCtrl = wx.Choice(panel, -1, choices = choices)
        self.ctrls["plgnsCtrl"] = plgnsCtrl
        actnsCtrl = wx.Choice(panel, -1, choices = [])
        self.ctrls["actnsCtrl"] = actnsCtrl
        testBtn = wx.Button(panel, -1, self.text.testRes)
        testBtn.SetToolTipString(self.text.testToolTip)
        self.ctrls["testBtn"] = testBtn
        resCtrl = wx.TextCtrl(panel, -1, "")
        resCtrl.Enable(False)
        self.ctrls["resCtrl"] = resCtrl
        w0 = grid.GetColumnWidth(0)
        w1 = grid.GetColumnWidth(1)
        w2 = grid.GetColumnWidth(2)
        w3 = grid.GetColumnWidth(2)
        gridLabel = wx.StaticText(panel, -1, self.text.actions)
        varTableLabel = wx.StaticText(panel, -1, self.text.defVals)
        btnAdd = wx.Button(panel, self.add_Id, self.text.add)
        self.ctrls["btnAdd"] = btnAdd
        btnAdd.Bind(wx.EVT_BUTTON, self.onBtnAdd)
        btnAdd.SetMinSize((w0-1, -1))
        labelText = wx.TextCtrl(panel, -1, "")
        labelText.Bind(wx.EVT_TEXT, self.onLabelText)
        self.ctrls["labelText"] = labelText
        labelText.SetMinSize((w1-1, -1))
        plgnsCtrl.SetMinSize((w2-1, -1))
        actnsCtrl.SetMinSize((w3-1, -1))

        def SetWidth():
            w0 = btnAdd.GetSize()[0]+1
            w1 = labelText.GetSize()[0]+1
            w2 = plgnsCtrl.GetSize()[0]+1
            w3 = actnsCtrl.GetSize()[0]+1
            grid.SetSize((w0+w1+w2+w3+SYS_VSCROLL_X + grid.GetWindowBorderSize()[0], -1))
            grid.SetColumnWidth(1, w1)
            grid.SetColumnWidth(2, w2)
            grid.SetColumnWidth(3, w2)
            panel.Update()


        def OnSize(event):
            wx.CallAfter(SetWidth)
            event.Skip()

        panel.Bind(wx.EVT_SIZE, OnSize)
        grid.Bind(eg.EVT_VALUE_CHANGED, self.onCheckBox)
        grid.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onGridClick)
        grid.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnGridRightClick)
        varTable.Bind(eg.EVT_VALUE_CHANGED, self.onVarTable)
        plgnsCtrl.Bind(wx.EVT_CHOICE, self.onPlgnChoice)
        actnsCtrl.Bind(wx.EVT_CHOICE, self.onActnChoice)
        testBtn.Bind(wx.EVT_BUTTON, self.onTestBtn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        actSizer = wx.GridBagSizer(vgap = 1, hgap = 1)
        sizer.Add(actSizer, 1, wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        actSizer.AddGrowableRow(1)
        actSizer.AddGrowableCol(1,w1)
        actSizer.AddGrowableCol(2,w2)
        actSizer.AddGrowableCol(3,w3)
        actSizer.AddGrowableCol(5,varTable.GetSize().width)
        actSizer.Add(gridLabel,(0,0),(1,4),flag = wx.EXPAND|wx.LEFT, border = 3)
        actSizer.Add(grid,(1,0),(1,4),flag = wx.EXPAND|wx.LEFT, border = 3)
        actSizer.Add(varTable,(1,5),flag = wx.EXPAND|wx.LEFT, border = 16)
        actSizer.Add(varTableLabel,(0,5),flag = wx.EXPAND|wx.LEFT, border = 16)
        actSizer.Add(btnAdd,(3,0),flag = wx.EXPAND|wx.LEFT, border = 3)
        actSizer.Add(labelText,(3,1),flag = wx.EXPAND)
        actSizer.Add(plgnsCtrl, (3,2),flag = wx.EXPAND)
        actSizer.Add(actnsCtrl, (3,3),flag = wx.EXPAND)
        resSizer = wx.BoxSizer(wx.HORIZONTAL)
        actSizer.Add(resSizer, (3,5), flag = wx.EXPAND|wx.LEFT, border = 16)
        actSizer.Add((2,5), (2,6))
        resSizer.Add(testBtn, 0, wx.RIGHT,5)
        resSizer.Add(resCtrl, 1, wx.EXPAND)

        self.notebook.AddPage(panel, self.text.actPage)
        return panel


    def ClearResult(self):
        self.ctrls["resCtrl"].ChangeValue("")


    def onVarTable(self, evt):
        row, col, val = evt.GetValue()
        ix = self.oldSel
        sel = self.ctrls["grid"].GetSelection()
        self.dataSet[ix][2][sel][4][row][col] = val
        self.ClearResult()
        evt.Skip()


    def ActComplete(self):
        flag = True
        name = self.ctrls["labelText"].GetValue()
        self.buttonRow.okButton.Enable(not name in CMMNDS)
        if name == "" or name in CMMNDS:
            flag = False
        if self.ctrls["plgnsCtrl"].GetSelection() == -1:
            flag = False
        if self.ctrls["actnsCtrl"].GetSelection() == -1:
            flag = False   
        btnAdd = self.ctrls["btnAdd"]
        if flag and not btnAdd.IsEnabled():
            self.ctrls["btnAdd"].Enable(True)


    def enableActCtrls(self, flag):
        self.ctrls["grid"].Enable(flag)
        self.ctrls["plgnsCtrl"].Enable(flag)
        self.ctrls["labelText"].Enable(flag)
        self.ctrls["testBtn"].Enable(flag)
        self.ctrls["plgnsCtrl"].SetSelection(-1)
        self.ctrls["actnsCtrl"].SetSelection(-1)
        self.ctrls["labelText"].ChangeValue("")
        self.ctrls["actnsCtrl"].Enable(False)
        self.ctrls["varTable"].FillData([])
        self.ClearResult()


    def OnGridUpDown(self, dir):
        grid = self.ctrls["grid"]
        ix = self.oldSel
        sel = grid.GetSelection()       
        newSel,self.dataSet[ix][2]=Move(self.dataSet[ix][2],sel,dir)
        grid.FillData(self.dataSet[ix][2])
        grid.SetSelection(newSel)


    def OnGridUp(self, dir):
        self.OnGridUpDown(-1)


    def OnGridDown(self, dir):
        self.OnGridUpDown(1)


    def OnGridDelButton(self, evt):
        grid = self.ctrls["grid"]
        ix = self.oldSel
        sel = grid.GetSelection()
        self.dataSet[ix][2].pop(sel)
        grid.DeleteRow(sel)
        if grid.GetItemCount():
            sel = grid.GetSelection()
            self.onGridClick(sel = sel)
        self.ClearResult()
        evt.Skip()


    def onCheckBox(self, evt):
        ix = self.oldSel
        sel, flag = evt.GetValue()
        if self.dataSet[ix][2][sel][0] != int(flag):
            self.dataSet[ix][2][sel][0] = int(flag)
        evt.Skip()


    def onAutConnect(self, evt):
        grid = self.ctrls["grid"] 
        ix = self.oldSel
        sel = grid.GetSelection()
        grid.ToggleItem(sel)
        flag = grid.IsChecked(sel)
        if self.dataSet[ix][2][sel][0] != int(flag):
            self.dataSet[ix][2][sel][0] = int(flag)
        evt.Skip()


    def onRetResMenu(self, evt):
        grid = self.ctrls["grid"] 
        ix = self.oldSel
        sel = grid.GetSelection()
        check = self.dataSet[ix][2][sel][5]
        self.dataSet[ix][2][sel][5] = not check
        evt.Skip()


    def OnGridRightClick(self, evt): #Right click menu
        grid = self.ctrls["grid"]
        sel = evt.m_itemIndex
        grid.SetSelection(sel)
        if not hasattr(self, "del_Id"):
            self.del_Id = wx.NewId()
            self.up_Id = wx.NewId()
            self.down_Id = wx.NewId()
            self.retRes_Id = wx.NewId()
            self.autConn_Id = wx.NewId()
            grid.Bind(wx.EVT_MENU, self.OnGridDelButton, id = self.del_Id)
            grid.Bind(wx.EVT_MENU, self.OnGridUp, id = self.up_Id)
            grid.Bind(wx.EVT_MENU, self.OnGridDown, id = self.down_Id)
            grid.Bind(wx.EVT_MENU, self.onBtnAdd, id = self.add_Id)
            grid.Bind(wx.EVT_MENU, self.onAutConnect, id = self.autConn_Id)
            grid.Bind(wx.EVT_MENU, self.onRetResMenu, id = self.retRes_Id)
        menu = wx.Menu()
        menu.Append(self.add_Id, self.text.addNewItem)
        menu.Append(self.del_Id, self.text.delSel)
        menu.AppendSeparator()                
        menu.Append(self.up_Id, self.text.moveUp)
        menu.Append(self.down_Id, self.text.moveDown)
        menu.AppendSeparator()                
        item = menu.AppendCheckItem(self.autConn_Id, self.text.autPerf)
        if grid.IsChecked(sel):
            item.Check()
        item = menu.AppendCheckItem(self.retRes_Id, self.text.notRes)
        if self.dataSet[self.oldSel][2][sel][5]:
            item.Check()
        grid.PopupMenu(menu)
        menu.Destroy()
        self.ClearResult()
        evt.Skip()


    def onGridClick(self, evt = None, sel = 0):
        sel = evt.m_itemIndex if evt else sel
        self.ctrls["grid"].SetSelection(sel)
        ix = self.oldSel
        data = self.dataSet[ix][2][sel]
        self.ctrls["labelText"].ChangeValue(data[1])
        self.ctrls["labelText"].Enable(True)
        plgnsCtrl = self.ctrls["plgnsCtrl"]
        plgnsCtrl.SetStringSelection(data[2])
        plgnsCtrl.Enable(True)
        self.onPlgnChoice()
        actnsCtrl = self.ctrls["actnsCtrl"]
        actnsCtrl.SetStringSelection(data[3])
        actnsCtrl.Enable(True)
        varTable = self.ctrls["varTable"]
        varTable.FillData(data[4])
        self.ClearResult()
        if evt:
            evt.Skip()


    def onBtnAdd(self, evt):
        self.enableActCtrls(False)
        self.ctrls["plgnsCtrl"].Enable(True)
        self.ctrls["labelText"].Enable(True)
        grid = self.ctrls["grid"]
        ix = self.oldSel
        sel = grid.GetSelection() + 1
        item = [False, "", "", "", [], False]
        self.dataSet[ix][2].insert(sel, item)
        grid.InsertRow(sel)
        grid.SetSelection(sel)
        self.ClearResult()
        self.ctrls["btnAdd"].Enable(False)
        evt.Skip()


    def onLabelText(self, evt):
        grid = self.ctrls["grid"]
        txt = evt.GetString()
        ix = self.oldSel
        sel = grid.GetSelection()
        grid.SetStringItem(sel, 1, txt)
        self.dataSet[ix][2][sel][1] = txt
        self.ActComplete()
        evt.Skip()


    def onTestBtn(self, evt):
        if self.actions:
            plgnsCtrl = self.ctrls["plgnsCtrl"]
            actnsCtrl = self.ctrls["actnsCtrl"]
            varTable = self.ctrls["varTable"]
            plgn = eg.plugins.__dict__[self.plugins[plgnsCtrl.GetStringSelection()]]
            actn = plgn.actions[self.actions[actnsCtrl.GetStringSelection()]]()
            args = []
            for item in varTable.GetData():
                if item[1] == 'NoneType':
                    value = None
                else:
                    if item[1] == 'str' or item[1] == 'unicode':
                        value = eval('%s("%s")' % (item[1], item[2]))
                    else:
                        value = eval(item[2])
                args.append(value)
            result = actn(*args)
            resCtrl = self.ctrls["resCtrl"]
            resCtrl.ChangeValue(str(result))
        evt.Skip()


    def onPlgnChoice(self, evt = None):
        plgnsCtrl = self.ctrls["plgnsCtrl"]
        plgnTitle = plgnsCtrl.GetStringSelection()
        plgn = eg.plugins.__dict__[self.plugins[plgnTitle]]    
        actnsCtrl = self.ctrls["actnsCtrl"]
        testBtn = self.ctrls["testBtn"]
        grid = self.ctrls["grid"]
        sel = grid.GetSelection()
        grid.SetStringItem(sel, 2, plgnTitle)
        ix = self.oldSel
        self.dataSet[ix][2][sel][2] = plgnTitle
        actnsCtrl.Clear()
        self.actions  = dict([(plgn.actions[item].name,item) for item in plgn.actions.keys()])
        choices = self.actions.keys()
        choices.sort()
        actnsCtrl.AppendItems(strings = choices)
        if evt:
            actnsCtrl.SetSelection(0)
            if self.actions:
                self.onActnChoice()
                actnsCtrl.Enable(True)
                testBtn.Enable(True)
            else:
                self.data = []
                actnsCtrl.Enable(False)
                testBtn.Enable(False)
            self.ActComplete()
            evt.Skip()


    def onActnChoice(self, evt = None):
        plgnsCtrl = self.ctrls["plgnsCtrl"]
        actnsCtrl = self.ctrls["actnsCtrl"]
        varTable = self.ctrls["varTable"]
        plgn = eg.plugins.__dict__[self.plugins[plgnsCtrl.GetStringSelection()]]
        actnTitle = actnsCtrl.GetStringSelection()
        grid = self.ctrls["grid"]
        sel = grid.GetSelection()
        grid.SetStringItem(sel, 3, actnTitle)
        grid.Enable(True)
        ix = self.oldSel
        self.dataSet[ix][2][sel][3] = actnTitle
        actn = plgn.actions[self.actions[actnTitle]]()
        argcount = actn.Configure.func_code.co_argcount
        varnames = actn.Configure.func_code.co_varnames[1:argcount]
        defaults = actn.Configure.func_defaults
        if varnames and not defaults:
            defaults = [None for item in varnames]
        if varnames:
            types = [type(item).__name__ for item in defaults]
            defaults = [str(item) for item in defaults]
            self.data = [list(item) for item in zip(varnames, types, defaults)]
        else:
            self.data = []
        testBtn = self.ctrls["testBtn"]
        if not testBtn.IsEnabled():
            testBtn.Enable(True)
        varTable.FillData(self.data)
        self.dataSet[ix][2][sel][4] = self.data
        if evt:
            self.ActComplete()
            evt.Skip()
#===============================================================================

class ConnectedClients(wx.Frame):

    def __init__(self, plugin, title):
        self.plugin = plugin
        text = self.plugin.text
        wx.Frame.__init__(
            self,
            None,
            -1,
            text.ccTitle % title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER ,
            name = text.ccName
        )
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.plugin.connectedClients = self
        self.SetBackgroundColour(wx.NullColour)
        if Persist.ccListPos:
            self.SetPosition(Persist.ccListPos)
        else:
            self.Center()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        ccListCtrl = wx.ListCtrl(
            self,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES
        )
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ccListCtrl, 1, wx.EXPAND)
        # WORKAROUND !!!
        # wx.LIST_FORMAT_RIGHT or wx.LIST_FORMAT_CENTRE for real first column !!!
        ccListCtrl.InsertColumn(0, "", wx.LIST_FORMAT_LEFT) #Dummy column 0 !!!
        ccListCtrl.InsertStringItem(0, "")
        rect = ccListCtrl.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1] #header height
        hi = rect[3] #item height
        for i in range(1, len(text.ccHeader)+1):
            ccListCtrl.InsertColumn(
                i,
                text.ccHeader[i-1],
                wx.LIST_FORMAT_RIGHT
            ) 
        width = SYS_VSCROLL_X + ccListCtrl.GetWindowBorderSize()[0]
        for i in range(len(text.ccHeader)+1):
            if i == 0:
                w = 0
            elif i==1:
                w = ccListCtrl.GetTextExtent("HHHHH")[0]
            elif i==2:
                w = ccListCtrl.GetTextExtent("  255.255.255.255")[0]
            elif i==3:
                w = ccListCtrl.GetTextExtent("HHHHHHH")[0]
            else:
                w = ccListCtrl.GetTextExtent("HHHHHHH")[0]
            ccListCtrl.SetColumnWidth(i, w)
            width += w
        ccListCtrl.SetMinSize((width, 4 + hh + 3 * hi))
        w0,h0=self.GetSize()
        w1,h1=self.GetClientSize()
        b= (w0-w1)/2
        ht= h0-h1-b
        height = 4 + hh + 3 * hi + b + ht
        self.SetMinSize((width+2*b, height))
        self.SetSize((width+2*b, height))


        def FillListCtrl(event=None):
            clnts = [item[2] for item in self.plugin.servers if item[1]==title][0]
            cnt = len(clnts)
            for i in range(cnt):
                ip, port = clnts[i].getpeername()
                ccListCtrl.InsertStringItem(i, "")  #Dummy column 0
                ccListCtrl.SetStringItem(i, 1, str(i+1))
                ccListCtrl.SetStringItem(i, 2, ip)
                ccListCtrl.SetStringItem(i, 3, str(port))
                prot = str(self.plugin.clnProtocols[clnts[i]][0]) if self.plugin.clnProtocols[clnts[i]][0] else text.oldProt
                ccListCtrl.SetStringItem(i, 4, prot)
            if event:
                event.Skip()
        self.SetSizer(mainSizer)
        FillListCtrl()
        self.MakeModal(True)
        self.Show(True)


    def onFrameCharHook(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            evt.Skip()


    def onClose(self, evt):
        self.MakeModal(False)
        ccListPos = self.GetPosition()
        if ccListPos != Persist.ccListPos:
            Persist.ccListPos = ccListPos
        self.plugin.connectedClients = None
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)
        evt.Skip()
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# websocket - Websocket client library for Python
# Copyright (C) 2010 Hiroki Ohtani(liris)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
default_timeout = None

def setdefaulttimeout(timeout):
    """
    Set the global timeout setting to connect.
    """
    global default_timeout
    default_timeout = timeout


def getdefaulttimeout():
    """
    Return the global timeout setting to connect.
    """
    return default_timeout

def _parse_url(url):
    """
    parse url and the result is tuple of
    (hostname, port, resource path and the flag of secure mode)
    """
    parsed = urlparse(url)
    if parsed.hostname:
        hostname = parsed.hostname
    else:
        raise ValueError("hostname is invalid")
    port = 0
    if parsed.port:
        port = parsed.port

    is_secure = False
    if parsed.scheme == "ws":
        if not port:
            port = 80
    elif parsed.scheme == "wss":
        is_secure = True
        if not port:
            port  = 443
    else:
        raise ValueError("scheme %s is invalid" % parsed.scheme)

    if parsed.path:
        resource = parsed.path
    else:
        resource = "/"

    return (hostname, port, resource, is_secure)


_MAX_INTEGER = (1 << 32) -1
_AVAILABLE_KEY_CHARS = range(0x21, 0x2f + 1) + range(0x3a, 0x7e + 1)
_MAX_CHAR_BYTE = (1<<8) -1

# ref. Websocket gets an update, and it breaks stuff.
# http://axod.blogspot.com/2010/06/websocket-gets-update-and-it-breaks.html

def _create_sec_websocket_key():
    spaces_n = random.randint(1, 12)
    max_n = _MAX_INTEGER / spaces_n
    number_n = random.randint(0, max_n)
    product_n = number_n * spaces_n
    key_n = str(product_n)
    for i in range(random.randint(1, 12)):
        c = random.choice(_AVAILABLE_KEY_CHARS)
        pos = random.randint(0, len(key_n))
        key_n = key_n[0:pos] + chr(c) + key_n[pos:]
    for i in range(spaces_n):
        pos = random.randint(1, len(key_n)-1)
        key_n = key_n[0:pos] + " " + key_n[pos:]
    return number_n, key_n


def _create_new_sec_websocket_key():
    key = urandom(16)
    return b64encode(key)


def _create_key3():
    return "".join([chr(random.randint(0, _MAX_CHAR_BYTE)) for i in range(8)])


def GetHash(key):
    buffer = key + GUID_KEY
    buffer = sha1(buffer)
    return b64encode(buffer.digest())


def XorMask(mask, bytes):
    if not mask:
        return bytes
    mask_size = len(mask)
    mask = map(ord, mask)
    count = 0
    result = array('B')
    result.fromstring(bytes)
    for i in xrange(len(result)):
        result[i] ^= mask[count]
        count = (count + 1) % mask_size
    return result.tostring()


def GetFragment(peer, maskOption):
    try:
        first, second = [ord(byte) for byte in peer.recv(2)]

        fin = (first >> 7) & 1
        rsv1 = (first >> 6) & 1
        rsv2 = (first >> 5) & 1
        rsv3 = (first >> 4) & 1
        opcode = first & 0xf

        mask = (second >> 7) & 1
        payload_len = second & 0x7f

        if mask != maskOption:
            return None # invalid frame
        if payload_len == 127:
            extended_payload_len = peer.recv(8)
            payload_len = unpack('!Q', extended_payload_len)[0]
            if payload_len > 0x7FFFFFFFFFFFFFFF:
                return None # invalid frame
        elif payload_len == 126:
            extended_payload_len = peer.recv(2)
            payload_len = unpack('!H', extended_payload_len)[0]
        if mask == 1:
            mask = peer.recv(4)
        payload = None if not payload_len else XorMask(mask, peer.recv(payload_len))
        return fin, opcode, payload
        #return fin, (rsv1, rsv2, rsv3, opcode), payload
    except:
        return None


def createTextFrame(bytes, maskOption):
    if maskOption:
        mask_bit = 1 << 7
        masking_key = urandom(4)
        bts = masking_key + XorMask(masking_key, bytes.encode('utf-8'))
    else:
        mask_bit = 0
        bts = bytes.encode('utf-8')
    header = chr(0b10000001) #((fin<<7)|(rsv1<<6)|(rsv2<<5)|(rsv3<<4)|opcode)
    payload_len = len(bts)
    if payload_len < 0:
        return None
    elif payload_len <= 125:
        header += chr(mask_bit | payload_len)
    elif payload_len < (1 << 16):
        header += chr(mask_bit | 126) + pack('!H', payload_len)
    elif payload_len < (1 << 63):
        header += chr(mask_bit | 127) + pack('!Q', payload_len)
    else:
        return None
    return header+pack(str(len(bts))+'s', bts)



HEADERS_TO_CHECK = {
    "upgrade": "websocket",
    "connection": "upgrade",
    }

HEADERS_TO_EXIST_FOR_HYBIlast = [
    "sec-websocket-accept",
]

HEADERS_TO_EXIST_FOR_HYBI00 = [
    "sec-websocket-origin",
    "sec-websocket-location",
]

HEADERS_TO_EXIST_FOR_HIXIE75 = [
    "websocket-origin",
    "websocket-location",
]

class _SSLSocketWrapper(object):
    def __init__(self, sock):
        self.ssl = socket.ssl(sock)

    def recv(self, bufsize):
        return self.ssl.read(bufsize)

    def send(self, payload):
        return self.ssl.write(payload)

class Websocket(object):
    """
    Low level Websocket interface.
    This class is based on
      The Websocket protocol draft-hixie-thewebsocketprotocol-76
      http://tools.ietf.org/html/draft-hixie-thewebsocketprotocol-76

    We can connect to the websocket server and send/recieve data.
    The following example is a echo client.

    >>> import websocket
    >>> ws = websocket.Websocket()
    >>> ws.Connect("ws://localhost:8080/echo")
    >>> ws.send("Hello, Server")
    >>> ws.recv()
    'Hello, Server'
    >>> ws.close()
    """

    def __init__(self, prot):
        """
        Initalize Websocket object.
        """
        self.connected = False
        self.prot = prot
        self.io_sock = self.sock = socket.socket()


    def settimeout(self, timeout):
        """
        Set the timeout to the websocket.
        """
        self.sock.settimeout(timeout)


    def gettimeout(self):
        """
        Get the websocket timeout.
        """
        return self.sock.gettimeout()


    def connect(self, url, **options):
        """
        Connect to url. url is websocket url scheme. ie. ws://host:port/resource
        """
        hostname, port, resource, is_secure = _parse_url(url)
        # TODO: we need to support proxy
        self.sock.connect((hostname, port))
        if is_secure:
            self.io_sock = _SSLSocketWrapper(self.sock)
        return self._handshake(hostname, port, resource, **options)


    def _handshake(self, host, port, resource, **options):        
        sock = self.io_sock
        headers = []
        if "header" in options:
            headers.extend(options["header"])
        headers.append("GET %s HTTP/1.1" % resource)
        headers.append("Upgrade: Websocket")
        headers.append("Connection: Upgrade")
        if port == 80:
            hostport = host
        else:
            hostport = "%s:%d" % (host, port)
        headers.append("Host: %s" % hostport)
        if self.prot:
            headers.append("Sec-WebSocket-Origin: http://%s" % hostport)
            key = _create_new_sec_websocket_key()
            headers.append("Sec-WebSocket-Key: %s" % key)
            headers.append("Sec-WebSocket-Version: 8\r\n\r\n")
        else:
            headers.append("Origin: %s" % hostport)
            number_1, key_1 = _create_sec_websocket_key()
            headers.append("Sec-WebSocket-Key1: %s" % key_1)
            number_2, key_2 = _create_sec_websocket_key()
            headers.append("Sec-WebSocket-Key2: %s" % key_2)
            headers.append("")
            key3 = _create_key3()
            headers.append(key3)
        log("headers = %s" % headers)
        header_str = "\r\n".join(headers)
        sock.send(header_str)
        log("--- request header ---")
        log(header_str)
        log("-----------------------")
        status, resp_headers = self._read_headers()
        log("status = %i" % status)
        log("resp_headers = %s" % resp_headers)
        if status != 101:
            self.close()
            return "Handshake Status %d" % status
        success, secure = self._validate_header(resp_headers)
        if not success:
            self.close()
            return "Invalid Websocket Header"
        if secure:
            if self.prot:
                if GetHash(key) != resp_headers['sec-websocket-accept']:
                    self.close()
                    return "challenge-response error"
            else:
                resp = self._get_resp()
                if not self._validate_resp(number_1, number_2, key3, resp):
                    self.close()
                    return "challenge-response error"
        self.connected = True


    def _validate_resp(self, number_1, number_2, key3, resp):
        challenge = pack("!I", number_1)
        challenge += pack("!I", number_2)
        challenge += key3
        digest = md5(challenge).digest()
        log('hi')
        log(digest)
        return  resp == digest


    def _get_resp(self):
        result = self._recv(16)
        log("--- challenge response result ---")
        log(repr(result))
        log("---------------------------------")
        return result


    def _validate_header(self, headers):
        #TODO: check other headers
        for key, value in HEADERS_TO_CHECK.iteritems():
            v = headers.get(key, None)
            if value != v.lower():
                return False, False
        success = 0
        existList = HEADERS_TO_EXIST_FOR_HYBIlast if self.prot else HEADERS_TO_EXIST_FOR_HYBI00
        for key in existList:
            if key in headers:
                success += 1
        if success == len(existList):
            return True, True
        elif success != 0:
            return False, True
        success = 0
        for key in HEADERS_TO_EXIST_FOR_HIXIE75:
            if key in headers:
                success += 1
        if success == len(HEADERS_TO_EXIST_FOR_HIXIE75):
            return True, False
        return False, False


    def _read_headers(self):
        status = None
        headers = {}
        log("--- response header ---")
        while True:
            line = self._recv_line()
            if line == "\r\n":
                break
            line = line.strip()
            if not status:
                status_info = line.split(" ", 2)
                status = int(status_info[1])
            else:
                kv = line.split(":", 1)
                if len(kv) == 2:
                    key, value = kv
                    headers[key.lower()] = value.strip()
                else:
                    eg.PrintError("Invalid header")
        log("-----------------------")
        return status, headers


    def send(self, payload):
        """
        Send the data as string. payload must be utf-8 string or unicode.
        """
        if isinstance(payload, unicode):
            payload = payload.encode("utf-8")
        if self.prot:
            data = createTextFrame(payload, 1)
        else:
            data = "".join(["\x00", payload, "\xff"])
        log('client send "%s"' % payload)
        self.io_sock.send(data)


    def recv(self):
        """
        Reeive utf-8 string data from the server.
        """
        if self.prot:
            bytes = GetFragment(self.io_sock, 0)
            if bytes is not None:
                return bytes[2]
        else:
            b = self._recv(1)
            log("recv frame: " + repr(b))
            frame_type = ord(b)
            if frame_type == 0x00:
                bytes = []
                while True:
                    b = self._recv(1)
                    if b == "\xff":
                        break
                    else:
                        bytes.append(b)
                return "".join(bytes)
            elif 0x80 < frame_type < 0xff:
                # which frame type is valid?
                length = self._read_length()
                bytes = self._recv_strict(length)
                return bytes
            elif frame_type == 0xff:
                n = self._recv(1)
                self._closeInternal()
                return None
            else:
                eg.PrintError("Invalid frame type")


    def _read_length(self):
        length = 0
        while True:
            b = ord(self._recv(1))
            length = length * (1 << 7) + (b & 0x7f)
            if b < 0x80:
                break
        return length


    def close(self):
        """
        Close Websocket object
        """
        if self.connected:
            try:
                self.io_sock.send("\xff\x00")
                timeout = self.sock.gettimeout()
                self.sock.settimeout(1)
                try:
                    result = self._recv(2)
                    if result != "\xff\x00":
                        log("bad closing Handshake")
                except:
                    pass
                self.sock.settimeout(timeout)
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
        self._closeInternal()


    def _closeInternal(self):
        self.connected = False
        self.sock.close()
        self.io_sock = self.sock


    def _recv(self, bufsize):
        bytes = self.io_sock.recv(bufsize)
        if not bytes:
            raise ConnectionClosedException()
        return bytes


    def _recv_strict(self, bufsize):
        remaining = bufsize
        bytes = ""
        while remaining:
            bytes += self._recv(remaining)
            remaining = bufsize - len(bytes)
        return bytes


    def _recv_line(self):
        line = []
        while True:
            c = self._recv(1)
            line.append(c)
            if c == "\n":
                break
        return "".join(line)
#===============================================================================

class WebsocketSuite(eg.PluginBase):

    text = Text
    serverHandler = None
    clientHandler = None
    servers = []
    clients = []
    clientsWs = {}
    serverToStop = []
    clientToStop = []
    connectedClients = None
    clnProtocols = {}
    protocolServDialog = None
    dataSet = None


    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        

    def __start__(self, dataSet = []):
        self.dataSet = dataSet
        self.info.eventPrefix = self.text.prefix


    def __stop__(self):
        self.StopAllServers()
        if self.connectedClients:
            self.connectedClients.onClose(wx.CommandEvent())


    def Configure(self, dataSet = []):
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.dataSet = cpy(dataSet)
        panel.persist = cpy(Persist.userVariables)
        del dataSet
        refr_Id = wx.NewId()
        refreshButton = wx.Button(panel.dialog, refr_Id, text.refresh)
        panel.dialog.buttonRow.Add(refreshButton)

        serverSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.headerServ),
            wx.HORIZONTAL
        )
        servSizer = wx.GridBagSizer(5, 5)
        servSizer.AddGrowableRow(0)
        servSizer.AddGrowableCol(3)
        serverListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES
        )
        formats = (
            wx.LIST_FORMAT_LEFT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_LEFT,
        )
        for i, colLabel in enumerate(text.colLabelsServ):
            serverListCtrl.InsertColumn(i, colLabel, format = formats[i])
        #setting cols width
        serverListCtrl.InsertStringItem(0, 30*"X")
        serverListCtrl.SetStringItem(0, 1, " 255.255.255.255")
        serverListCtrl.SetStringItem(0, 2, "HHHHHHH")
        serverListCtrl.SetStringItem(0, 3, "X")
        serverListCtrl.SetStringItem(0, 4, 16*"X")
        width_s = SYS_VSCROLL_X + serverListCtrl.GetWindowBorderSize()[0]
        for i in range(len(text.colLabelsServ)):
            serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width_s += serverListCtrl.GetColumnWidth(i)
        ws0 = serverListCtrl.GetColumnWidth(0)
        ws4 = serverListCtrl.GetColumnWidth(4)
        #buttons
        cl_Id = wx.NewId()
        ab_Id = wx.NewId()
        abAll_Id = wx.NewId()
        abCli_Id = wx.NewId()
        abAllCli_Id = wx.NewId()

        clntButton = wx.Button(panel, cl_Id, text.clients)
        abortButtonServ = wx.Button(panel, ab_Id, text.abort)
        abortAllButtonServ = wx.Button(panel, abAll_Id, text.abortAll)    
        protocolButtonServ = wx.Button(panel, refr_Id, text.protocolServ)
        servSizer.Add(serverListCtrl, (0,0), (1, 5), flag = wx.EXPAND)
        servSizer.Add(protocolButtonServ, (1,4), flag = wx.ALIGN_RIGHT)
        servSizer.Add(abortAllButtonServ, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
        servSizer.Add(abortButtonServ, (1,0))
        servSizer.Add(clntButton, (1,2))
        serverSizer.Add(servSizer, 1, wx.EXPAND)
        panel.sizer.Add(serverSizer, 1, wx.EXPAND)
       
        clientSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.headerCli),
            wx.HORIZONTAL
        )
        cliSizer = wx.GridBagSizer(5, 5)
        cliSizer.AddGrowableRow(0)
        cliSizer.AddGrowableCol(2)
        clientListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES
        )
        formats = (
            wx.LIST_FORMAT_LEFT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_RIGHT,
            wx.LIST_FORMAT_LEFT,
        )
        for i, colLabel in enumerate(text.colLabelsCli):
            clientListCtrl.InsertColumn(i, colLabel, format = formats[i])
        #setting cols width
        clientListCtrl.InsertStringItem(0, 30*"X")
        clientListCtrl.SetStringItem(0, 1, " 255.255.255.255")
        clientListCtrl.SetStringItem(0, 2, "HHHHHHH")
        clientListCtrl.SetStringItem(0, 3, " 255.255.255.255")
        clientListCtrl.SetStringItem(0, 4, "HHHHHHH")
        clientListCtrl.SetStringItem(0, 5, 16*"X")
        width_c = SYS_VSCROLL_X + clientListCtrl.GetWindowBorderSize()[0]
        for i in range(6):
            clientListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width_c += clientListCtrl.GetColumnWidth(i)
        width = max((width_s, width_c))
        wc0 = clientListCtrl.GetColumnWidth(0)
        wc5 = clientListCtrl.GetColumnWidth(5)
        serverListCtrl.SetMinSize((width, -1))
        clientListCtrl.SetMinSize((width, -1))
        #buttons
        abortButtonCli = wx.Button(panel, abCli_Id, text.abort)
        abortAllButtonCli = wx.Button(panel, abAllCli_Id, text.abortAll)    
        protocolButtonCli = wx.Button(panel, -1, text.protocolCli)
        cliSizer.Add(clientListCtrl, (0,0), (1, 4), flag = wx.EXPAND)
        cliSizer.Add(protocolButtonCli, (1,3), flag = wx.ALIGN_RIGHT)
        cliSizer.Add(abortAllButtonCli, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
        cliSizer.Add(abortButtonCli, (1,0))
        clientSizer.Add(cliSizer, 1, wx.EXPAND)
        panel.sizer.Add(clientSizer, 1, wx.EXPAND|wx.TOP, 10)


        def PopulateListServ(event = None, toStop = ()):
            serverListCtrl.DeleteAllItems()
            i = 0
            for item in self.servers:
                if item[0] not in toStop:
                    cls = u"DEFAULT" if item[3] == -1 else self.dataSet[item[3]][0]
                    serverListCtrl.InsertStringItem(i, item[1])
                    serverListCtrl.SetStringItem(i, 1, item[0].getsockname()[0])
                    serverListCtrl.SetStringItem(i, 2, str(item[0].getsockname()[1]))
                    serverListCtrl.SetStringItem(i, 3, str(len(item[2])))
                    serverListCtrl.SetStringItem(i, 4, cls)
                    i+=1
            ListSelectionServ(wx.CommandEvent())
            abortAllButtonServ.Enable(serverListCtrl.GetItemCount() > 0)


        def PopulateListCli(event = None, toStop = ()):
            clientListCtrl.DeleteAllItems()
            i = 0
            for item in self.clients:
                if item[0] not in toStop:
                    clientListCtrl.InsertStringItem(i, item[1])
                    clientListCtrl.SetStringItem(i, 1, item[0].getsockname()[0])
                    clientListCtrl.SetStringItem(i, 2, str(item[0].getsockname()[1]))
                    clientListCtrl.SetStringItem(i, 3, item[0].getpeername()[0])
                    clientListCtrl.SetStringItem(i, 4, str(item[0].getpeername()[1]))
                    clientListCtrl.SetStringItem(i, 5, str(item[2]))
                    i+=1
            ListSelectionCli(wx.CommandEvent())
            abortAllButtonCli.Enable(clientListCtrl.GetItemCount() > 0)


        def OnRefresh(event):
            PopulateListServ()
            PopulateListCli()
            event.Skip()
        refreshButton.Bind(wx.EVT_BUTTON, OnRefresh)


        def OnClntButton(event):
            item = serverListCtrl.GetFirstSelected()
            title = serverListCtrl.GetItem(item, 0).GetText()
            wx.CallAfter(ConnectedClients, self, title)
        #    event.Skip()


        def OnAbortButtonServ(event):
            item = serverListCtrl.GetFirstSelected()
            toStop = []
            while item != -1:
                title = serverListCtrl.GetItem(item, 0).GetText()
                titles = [i[1] for i in self.servers]
                ix = titles.index(title)
                serv = self.servers[ix][0]
                host, port = serv.getsockname()
                toStop.append(serv)
                self.StopServer(host, str(port), modeHost = 3)
                item = serverListCtrl.GetNextSelected(item)
            PopulateListServ(toStop = toStop)
        #    event.Skip()


        def OnAbortButtonCli(event):
            item = clientListCtrl.GetFirstSelected()
            toStop = []
            while item != -1:
                title = clientListCtrl.GetItem(item, 0).GetText()
                titles = [i[1] for i in self.clients]
                ix = titles.index(title)
                clnt = self.clients[ix][0]
                host, port = clnt.getpeername()
                toStop.append(clnt)
                self.StopClient(host, str(port), modeClient = 2)
                item = clientListCtrl.GetNextSelected(item)
            PopulateListCli(toStop = toStop)
        #    event.Skip()


        def OnAbortAllButtonServ(event):
            toStop = []
            for serv in [item[0] for item in self.servers]:
                host, port = serv.getsockname()
                toStop.append(serv)
                self.StopServer(host, str(port), modeHost = 3)
            PopulateListServ(toStop = toStop)
        #    event.Skip()


        def OnAbortAllButtonCli(event):
            toStop = []
            for clnt in [item[0] for item in self.clients]:
                host, port = clnt.getpeername()
                toStop.append(clnt)
                self.StopClient(host, str(port), modeClient = 2)
            PopulateListCli(toStop = toStop)
        #    event.Skip()


        def OnRightClickServ(evt):
            if not hasattr(panel, "menuServ"):
                panel.menuServ = None
                serverListCtrl.Bind(wx.EVT_MENU, OnClntButton, id = cl_Id)
                serverListCtrl.Bind(wx.EVT_MENU, OnAbortButtonServ, id = ab_Id)
                serverListCtrl.Bind(wx.EVT_MENU, OnAbortAllButtonServ, id = abAll_Id)
                serverListCtrl.Bind(wx.EVT_MENU, OnRefresh, id = refr_Id)
            menu = wx.Menu()
            if serverListCtrl.GetSelectedItemCount() == 1:
                menu.Append(cl_Id, text.clientsMenu)
                menu.AppendSeparator()                
            if serverListCtrl.GetSelectedItemCount() > 0:
                menu.Append(ab_Id, text.abortMenu)
            if serverListCtrl.GetItemCount() > 0:
                menu.Append(abAll_Id, text.abortAllMenu)
            menu.AppendSeparator()                
            menu.Append(refr_Id, text.refresh)
            serverListCtrl.PopupMenu(menu)
            menu.Destroy()
        #    evt.Skip()
        serverListCtrl.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, OnRightClickServ)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, OnRightClickServ)


        def OnRightClickCli(evt):
            if not hasattr(panel, "menuCli"):
                panel.menuCli = None
                clientListCtrl.Bind(wx.EVT_MENU, OnAbortButtonCli, id = abCli_Id)
                clientListCtrl.Bind(wx.EVT_MENU, OnAbortAllButtonCli, id = abAllCli_Id)
                clientListCtrl.Bind(wx.EVT_MENU, OnRefresh, id = refr_Id)
            menu = wx.Menu()            
            if clientListCtrl.GetSelectedItemCount() > 0:
                menu.Append(abCli_Id, text.abortMenuCli)
            if clientListCtrl.GetItemCount() > 0:
                menu.Append(abAllCli_Id, text.abortAllMenuCli)
            menu.AppendSeparator()                
            menu.Append(refr_Id, text.refresh)
            clientListCtrl.PopupMenu(menu)
            menu.Destroy()
            evt.Skip()
        clientListCtrl.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, OnRightClickCli)
        clientListCtrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, OnRightClickCli)


        def ListSelectionServ(event):
            flag = serverListCtrl.GetFirstSelected() != -1
            abortButtonServ.Enable(flag)
            clntButton.Enable(serverListCtrl.GetSelectedItemCount() == 1)
            event.Skip()


        def ListSelectionCli(event):
            flag = clientListCtrl.GetFirstSelected() != -1
            abortButtonCli.Enable(flag)
            event.Skip()
           

        def SetWidth():
            wsDelta = (serverListCtrl.GetSize()[0] - width)/2
            serverListCtrl.SetColumnWidth(0, ws0 + wsDelta)
            serverListCtrl.SetColumnWidth(4, ws4 + wsDelta)
            wcDelta = (clientListCtrl.GetSize()[0] - width)/2
            clientListCtrl.SetColumnWidth(0, wc0 + wcDelta)
            clientListCtrl.SetColumnWidth(5, wc5 + wcDelta)


        def OnSize(event):
            wx.CallAfter(SetWidth)
            event.Skip()


        def ProtocolServ(event):
            if not self.protocolServDialog:
                wx.CallAfter(Protocol, panel, self, self.text.srvClss)
            event.Skip()


        def ProtocolCli(event):
            print '"Client classes" button pressed - Unfortunately procedure still is not done'
            event.Skip()

        OnRefresh(wx.CommandEvent())       
        clntButton.Bind(wx.EVT_BUTTON, OnClntButton)
        abortButtonServ.Bind(wx.EVT_BUTTON, OnAbortButtonServ)
        abortButtonCli.Bind(wx.EVT_BUTTON, OnAbortButtonCli)
        abortAllButtonServ.Bind(wx.EVT_BUTTON, OnAbortAllButtonServ)
        abortAllButtonCli.Bind(wx.EVT_BUTTON, OnAbortAllButtonCli)
        protocolButtonServ.Bind(wx.EVT_BUTTON, ProtocolServ)
        protocolButtonCli.Bind(wx.EVT_BUTTON, ProtocolCli)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelectionServ)
        clientListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelectionCli)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelectionServ)
        clientListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelectionCli)

        while panel.Affirmed():
            Persist.userVariables = panel.persist
            panel.SetResult(
                panel.dataSet,
        )


    def get_headers(self, data):
        log("get_headers - data: %s" % repr(data))
        bytes = data[len(data)-8:]
        key1 = re.compile("Sec-WebSocket-Key1: (.*)\r\n").findall(data)
        key2 = re.compile("Sec-WebSocket-Key2: (.*)\r\n").findall(data)        
        data = data.decode('utf-8', 'ignore')
        resource = re.compile("GET (.*) HTTP").findall(data)
        host = re.compile("Host: (.*)\r\n").findall(data)
        origin = re.compile("Origin: (.*)\r\n").findall(data)
        cookie = re.compile("Cookie: (.*)\r\n").findall(data)
        return [resource[0],host[0],origin[0],key1[0],key2[0],bytes]


    def part(self, token):
        digits=""
        for d in re.compile('[0-9]').findall(token):
            digits = digits + str(d)
        count=0
        for s in re.compile(' ').findall(token):
            count = count + 1
        return int(int(digits)/count)


    def handshake(self, client, msg):
        if "Sec-WebSocket-Key2" in msg:
            try:
                headers = self.get_headers(msg)
                challenge = pack('>II', self.part(headers[3]), self.part(headers[4]))
                challenge = challenge + ''.join([ pack('>B', ord( x )) for x in headers[5] ])
                hash = md5(challenge).digest()
                our_handshake = "\r\n".join((
                    "HTTP/1.1 101 WebSocket Protocol Handshake",
                    "Upgrade: WebSocket",
                    "Connection: Upgrade",
                    "Sec-Websocket-Origin: %s",
                    "Sec-Websocket-Location: ws://%s%s\r\n\r\n"
                )) % (headers[2],headers[1],headers[0])
                client.send(our_handshake.encode('latin-1') + hash)
                return 0
            except:
                return None
        elif "Sec-WebSocket-Key:" in msg and "Sec-WebSocket-Version:" in msg:
            try:
                key = re.compile("Sec-WebSocket-Key: (.*)\r\n").findall(msg)[0]
                prot = re.compile("Sec-WebSocket-Version: (.*)\r\n").findall(msg)[0]
                hash = GetHash(key)
                our_handshake = "\r\n".join((
                    "HTTP/1.1 101 Switching Protocols",
                    "Upgrade: WebSocket",
                    "Connection: Upgrade",
                    "Sec-WebSocket-Accept: %s\r\n\r\n")) % hash
                client.send(our_handshake)
                #client.send(our_handshake.encode('latin-1'))
                return int(prot)
            except:
                return None


    def send_data(self, client, bytes, newStr = None):
        prot = self.clnProtocols[client][0]
        if not prot:
            bytes = b"\x00" + bytes.encode('utf-8') + b"\xff"
        else:
            bytes = newStr or createTextFrame(bytes, 0)
        try:
            return client.send(bytes)
        except IOError, e:
            if e.errno == 32:
                log("pipe error")


    def send_data_all(self, bytes, client = None, indx = None):
        ix = indx if indx is not None else [item[0] for item in self.servers].index(self.clientsServers[client])
        for client in self.servers[ix][2]:
            self.send_data(client, bytes, createTextFrame(bytes, 0))


    def updateLogFile(self, folder, title, line, blank = False):
        if not folder:
            return
        logfile = folder + "\\Websocket_%s_log.txt" % title
        f = openFile(logfile, encoding='utf-8', mode='a')
        if blank:
            f.write("\r\n")
        try:
            f.write("%s  %s\r\n" % (str(dt.now())[:19], line.decode('utf-8')))
        except:
            try:
                f.write("%s  %s\r\n" % (str(dt.now())[:19], line))
            except:
                f.write("%s  %s\r\n" % (str(dt.now())[:19], repr(line)))
        f.close()


    def PerformAction(self, action, kwargs):
        tmpKwargs = [v[0] for v in kwargs]
        plgns  = dict([(eg.plugins.__dict__[item].plugin.name,item) for item in eg.plugins.__dict__.keys()])
        plgn = eg.plugins.__dict__[plgns[action[2]]]
        actns  = dict([(plgn.actions[item].name,item) for item in plgn.actions.keys()])
        actn = plgn.actions[actns[action[3]]]()
        args = []
        for item in action[4]:
            if item[1] == 'NoneType':
                value = None
            else:
                if item[0] not in tmpKwargs:
                    val_ = item[2]
                else: #When exists non-default value
                    val_ = kwargs[tmpKwargs.index(item[0])][1]
                if item[1] == 'unicode' or item[1] == 'str':
                    value = val_.replace(u'\xab\u2039\u2022\u203a\xbb', ",") # replace("«‹•›»", ",")
                else:
                    value = eval(val_)
            args.append(value)
        return  actn(*args)


    def InteractServer(self, data, client, indx):
        title   = self.servers[indx][1]
        fn      = self.servers[indx][3]
        if not self.clnProtocols[client][0]:
            data = data[1:]
        data = data.decode('utf-8', 'ignore')
        if data == "I'm leaving":
            return True
        if fn == -1: # DEFAULT
            self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))
        else:
            actions = self.dataSet[fn][2]
            flags = self.dataSet[fn][3]
            line = self.text.cmdRec % (data, client.getpeername())
            self.updateLogFile(flags[3], title, line)
            pos = data.find("(")
            key = data[:pos]
            tmpList = [i[1] for i in actions]
            kwargs = data[pos+1:-1].split(",")
            kwargs = [v.split("=") for v in kwargs]
            for i, itm in enumerate(kwargs):
                for j, jtm in enumerate(itm):
                    kwargs[i][j] = jtm.strip()
            nonsFlag = False
            if key in CMMNDS:
                var = kwargs[0][0]
                persVars = Persist.userVariables[fn][1]
                tmpPersVars = [p[0] for p in persVars]
                if var in tmpPersVars:
                    ix = tmpPersVars.index(var)
                    val = persVars[ix][1]
                    tp = self.dataSet[fn][1][ix][1]
                    if key == "ToggleBoolean":
                        if tp == 'bool':
                            persVars[ix][1] = not val
                        else:
                            nonsFlag = True            
                    elif key == "IncrementInteger":
                        if tp == 'int':
                            persVars[ix][1] = val + 1
                        else:
                            nonsFlag = True            
                    elif key == "DecrementInteger":
                        if tp == 'int':
                            persVars[ix][1] = val - 1
                        else:
                            nonsFlag = True            
                    elif key == "SetValue":
                        if tp =='str':
                            newVal = str(data[:-1].split("=")[1])
                        elif tp =='unicode':
                            newVal = data[:-1].split("=")[1]
                        else:
                            newVal = eval(kwargs[0][1])
                        if tp == type(newVal).__name__:
                            persVars[ix][1] = newVal
                        else:
                            nonsFlag = True
                else:
                    if flags[2]:
                        self.send_data(client, self.text.unknVar % var)
                        line = self.text.unknVarMsg % (var, client.getpeername())
                        self.updateLogFile(flags[3], title, line)
                    if flags[1]:
                        self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))
                    return
                if nonsFlag:
                    if flags[2]:
                        self.send_data(client, self.text.invCmd % data)
                        line = self.text.invCmdMsg % (data, client.getpeername())
                        self.updateLogFile(flags[3], title, line)
                    if flags[1]:
                        self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))
                else:
                    self.send_data_all(u"%s=%s" % (var, unicode(persVars[ix][1])), client)
                    line = self.text.broadMsg % (var, unicode(persVars[ix][1]))
                    self.updateLogFile(flags[3], title, line)
                    if flags[0]:
                        self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))
            elif key in tmpList:
                ix = tmpList.index(key)
                result = self.PerformAction(actions[ix], kwargs)
                if not actions[ix][5]:
                    self.send_data_all(u"%s=%s" % (key, unicode(result)), client)
                    line = self.text.broadMsg % (key, unicode(result))
                    self.updateLogFile(flags[3], title, line)
                if flags[0]:
                    self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))
            else:
                if flags[2]:
                    try:
                        self.send_data(client, self.text.unknCmd % data)
                    except:
                        self.send_data(client, self.text.unknCmd % repr(data))
                    line = self.text.unknCmdMsg % (data, client.getpeername())
                    self.updateLogFile(flags[3], title, line)
                if flags[1]:
                    self.TriggerEvent(self.text.srvRecData, payload = (title, client.getpeername(), data))


    def InteractClient(self, data, client, title):
        if True: # ToDo .....
            self.TriggerEvent(self.text.clnRecData, payload = (title, client.getpeername(), data))


    def ClientHandler(self): #Thread
        clnts = [clnt[0] for clnt in self.clients]
        while clnts:
            readable, _, exceptional = select(clnts, [], clnts, 1)
            for r in readable:
                ws = self.clientsWs[r]
                ix = clnts.index(r)
                try:
                    data = ws.recv()
                except:
                    data = None
                if data:
                    # A readable client socket has data
                    fn = self.clients[ix][2]
                    fn = self.InteractClient if not fn else self.InteractClient # ############## ToDo !!! ###########
                    fn(data,r,self.clients[ix][1])
                else: #A readable socket without data available is from a client that has disconnected
                    log('closing after reading no data [server %s disconnected]' % str(r.getpeername()))
                    self.clients.pop(ix)
                    del self.clientsWs[r]
                    del ws
                    r.close()
            # Handle "exceptional conditions"
            for e in exceptional:
                log('handling exceptional condition for %s' % str(e.getpeername()))
                # Stop listening for input on the connection
                self.clients.pop(ix)
                ws = self.clientsWs[e]
                del self.clientsWs[e]
                del ws
                e.close()

            # Stop client, if any request
            for i in range(len(self.clientToStop)-1,-1,-1):
                client = self.clientToStop[i]
                ix = [item[0] for item in self.clients].index(client)
                ws = ws = self.clientsWs[client]
                title = self.clients[ix][1]
                self.clients.pop(ix)
                del self.clientsWs[client]
                del ws                
                client.close()
                self.clientToStop.pop(i)
                log("client %s stopped" % title)
            clnts = [clnt[0] for clnt in self.clients]
        #End of thread run
        self.clientHandler = None


    def StartClient(
        self,
        host,
        port,
        title,
        interact,
        prot
    ):
        title = eg.ParseString(title)
        host = eg.ParseString(host)
        port = int(eg.ParseString(port))
        if title in [i[1] for i in self.clients]:
            eg.PrintError(self.text.cliStartErr1 % title)
            return 1
        tmpLst = [item[0].getpeername() for item in self.clients]
        if not (host, port) in tmpLst:
            try:
                websock = Websocket(prot)
                websock.settimeout(default_timeout)
                res = websock.connect(str("ws://%s:%i" % (host, port)))
                if res:
                    eg.PrintError(res)
                    return 4
            except socket.error, exc:
                eg.PrintError(exc[1])
                if websock:
                    del websock
                return 2
            self.clients.append([websock.sock, title, interact, prot])
            self.clientsWs[websock.sock] = websock
            if len(self.clients) == 1:
                self.clientHandler = Thread(target = self.ClientHandler, name = "WebsocketClientHandler")
                self.clientHandler.start()
            return 0
        else:
            eg.PrintError(self.text.cliStartErr3 % (host, port))
            return 3


    def StopClient(self, txt, port, modeClient):
        txt = eg.ParseString(txt)
        port = int(eg.ParseString(port))
        ix = None
        if modeClient < 2:
            titles = [i[1] for i in self.clients]
            if txt in titles:
                ix = titles.index(txt)
                srvr = self.clients[ix][0].getpeername()
                host = srvr[0]
                port = srvr[1]
            else:
                eg.PrintError(self.text.cliError1 % txt)
                return 1
        elif modeClient == 2:
            host = txt
            tmpLst = [item[0].getpeername() for item in self.clients]
            if (host,port) in tmpLst:
                ix = tmpLst.index((host, port))
        if ix is not None:
            try:
                sock = self.clients[ix][0]
                ws = self.clientsWs[sock]
                self.clientToStop.append(sock)
                return 0
            except socket.error, exc:
                eg.PrintError(exc[1])
                return 3
        else:
            eg.PrintError(self.text.cliError2 % (host, port))
            return 2


    def ClientSendMessage(self, txt, port, modeClient, message):
        txt = eg.ParseString(txt)
        port = int(eg.ParseString(port))
        if modeClient < 2:
            titles = [i[1] for i in self.clients]
            if txt in titles:
                ix = titles.index(txt)
                srvr = self.clients[ix][0].getpeername()
                host = srvr[0]
                port = srvr[1]
            else:
                eg.PrintError(self.text.cliError1 % txt)
                return 1
        elif modeClient == 2:
            host = txt
        tmpLst = [item[0].getpeername() for item in self.clients]
        if (host, port) in tmpLst:
            try:
                ix = tmpLst.index((host, port))
                sock = self.clients[ix][0]
                ws = self.clientsWs[sock]
                ws.send(message)
                return 0
            except socket.error, exc:
                raise self.Exception(exc[1])
                return 1
        else:
            eg.PrintError(self.text.cliError2 % (host, port))
            return 2


    def ServerHandler(self):
        while self.inputs:
            readable, _, exceptional = select(self.inputs, [], self.inputs, 1)
            for r in readable:
                srvrs = [item[0] for item in self.servers]
                if r in srvrs:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = r.accept()                
                    ix = srvrs.index(r)
                    self.clientsServers[connection] = r
                    connection.setblocking(0)
                    self.inputs.append(connection)
                else: #client
                    data = None
                    cl_close = False
                    s = self.clientsServers[r]
                    srvrTitle = [item[1] for item in self.servers][srvrs.index(s)]
                    ix = srvrs.index(s) #server index
                    if r not in self.connected: #first data => handshake
                        log('Server %s: New client %s tries to connect' % (srvrTitle, str(r.getpeername())))
                        try:
                            data = r.recv(1024)
                            prot = self.handshake(r, data)
                            self.clnProtocols[r] = [prot, []]
                            if prot is not None: #CONNECT ?
                                #Add client to list:
                                self.servers[ix][2].append(connection) 
                                self.connected.append(r)
                                if self.dataSet[self.servers[ix][3]][3][4]:
                                    self.TriggerEvent(self.text.clnConnect, payload = (srvrTitle, r.getpeername()))
                                line = self.text.connCln % str(r.getpeername())
                                folder = self.dataSet[self.servers[ix][3]][3][3]
                                self.updateLogFile(folder, self.servers[ix][1], line)
                                vars = Persist.userVariables[self.servers[ix][3]][1]
                                for v in vars:
                                    self.send_data(r, "%s=%s" % (v[0], v[1]))
                                    line = self.text.msgToCln % (unicode(v[0]), unicode(v[1]), r.getpeername())
                                    self.updateLogFile(folder, self.servers[ix][1], line)
                                actns = [item for item in self.dataSet[self.servers[ix][3]][2] if item[0]]
                                for actn in actns:
                                    result = self.PerformAction(actn, [])
                                    self.send_data(r, "%s=%s" % (actn[1], result))
                                    line = self.text.msgToCln % (actn[1], unicode(result), r.getpeername())
                                    self.updateLogFile(folder, self.servers[ix][1], line)
                        except:
                            del self.clientsServers[r]
                            self.inputs.remove(r)
                            r.close()
                    else: #if r in self.connected:
                        prot = self.clnProtocols[r][0]
                        if prot >= 7:
                            frgmnt = GetFragment(r, 1)
                            if frgmnt is not None:
                                if frgmnt[0]: # ToDo frgmnt[1] == 0x09 (Ping) or 0x0A (Pong)
                                    if frgmnt[1] == 8: # CLOSE frame
                                        data = '\xff\x00'
                                    elif frgmnt[1] == 1: #text frame
                                        self.clnProtocols[r][1].append(frgmnt[2])
                                        data =  "".join(self.clnProtocols[r][1])
                                        self.clnProtocols[r][1] = []
                                elif frgmnt[1] == 1: # Not fin and text frame
                                    self.clnProtocols[r][1].append(frgmnt[2])
                                    continue
                            else: 
                                data = None # after exception
                        else:
                            try:
                                data = r.recv(1024)
                            except:
                                pass
                        if data and data != '\xff\x00':
                            # A readable client socket has data
                            if self.InteractServer(data, r, ix):
                                log('closing after reading "I\'m leaving" [peer %s disconnected]' % str(r.getpeername()))
                                cl_close = True
                        # if no data or data == '\xff\x00':
                        else: #A readable socket without data available (or with data "\xff\x00") is from a client that has disconnected
                            if data == '\xff\x00':
                                log('closing after "Close frame" from client [peer %s disconnected]' % str(r.getpeername()))
                            else:
                                log('closing after reading no data or invalid data [peer %s disconnected]' % str(r.getpeername()))
                            cl_close = True
                        if cl_close:
                            # Stop listening for input on the connection
                            ix = srvrs.index(s)
                            if r in self.connected:
                                self.connected.remove(r)
                                del self.clnProtocols[r]
                                if self.dataSet[self.servers[ix][3]][3][4]:
                                    self.TriggerEvent(self.text.clnDisconnect, payload = (srvrTitle, r.getpeername()))
                                line = self.text.disconnCln % str(r.getpeername())
                                folder = self.dataSet[self.servers[ix][3]][3][3]
                                self.updateLogFile(folder, self.servers[ix][1], line)
                            self.servers[ix][2].remove(r)
                            del self.clientsServers[r]
                            self.inputs.remove(r)
                            r.close()

            # Handle "exceptional conditions" UNTESTED - I NOT KNOW HOW CAUSE IT !!!!!!!!!!!
            for e in exceptional:
                log('handling exceptional condition for %s' % str(e.getpeername()))
                # Stop listening for input on the connection
                srvrs = [item[0] for item in self.servers]
                if not e in srvrs:
                    s = self.clientsServers[e]
                    ix = srvrs.index(s)
                    srvrTitle = [item[1] for item in self.servers][ix]
                    if e in self.connected:
                        self.connected.remove(e)
                        del self.clnProtocols[e]
                        if self.dataSet[self.servers[ix][3]][3][4]:
                            self.TriggerEvent(self.text.clnDisconnect, payload = (srvrTitle, e.getpeername()))
                        line = self.text.disconnCln % str(e.getpeername())
                        folder = self.dataSet[self.servers[ix][3]][3][3]
                        self.updateLogFile(folder, self.servers[ix][1], line)
                    self.servers[ix][2].remove(e)
                    del self.clientsServers[e]
                self.inputs.remove(e)
                e.close()

            # Stop server, if any request
            for i in range(len(self.serverToStop)-1,-1,-1):
                srvr = self.serverToStop[i]
                srvrs = [item[0] for item in self.servers]
                ix = srvrs.index(srvr)
                title = self.servers[ix][1]
                self.inputs.remove(srvr)
                for client in self.servers[ix][2]:
                    self.inputs.remove(client)
                    client.shutdown(socket.SHUT_RDWR)
                    self.connected.remove(client)
                    del self.clnProtocols[client]
                    line = self.text.disconnCln % str(client.getpeername())
                    folder = self.dataSet[self.servers[ix][3]][3][3]
                    self.updateLogFile(folder, self.servers[ix][1], line)
                    del self.clientsServers[client]
                    client.close()
                folder = self.dataSet[self.servers[ix][3]][3][3]
                self.updateLogFile(folder, title, self.text.servStop)
                self.servers.pop(ix)
                srvr.close()
                self.serverToStop.pop(i)
            if self.servers == []:
                self.clientsServers = {}
                self.connected = []
                self.clnProtocols = {}
                self.serverHandler = None            

    #switch off all servers:
        for item in [item[2] for item in self.servers]:
            for client in item:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
        for s in [item[0] for item in self.servers]:
            s.close()
        self.clientsServers = {}
        self.servers = []
        self.connected = []
        self.clnProtocols = {}
        self.serverHandler = None


    def SetPersistVar(self, protType, prot, varType, variable, val):
        prot = eg.ParseString(prot)
        var = eg.ParseString(variable)
        val = eg.ParseString(val)
        tmpList = [item[0] for item in Persist.userVariables]
        if prot in tmpList:
            ix = tmpList.index(prot)
            vars = Persist.userVariables[ix][1]
            tmpList = [i[0] for i in vars]
            if var in tmpList:
                iy = tmpList.index(var)
                var = vars[iy][1]
                if type(var) is str:
                    val = str(val)
                elif type(var) is not unicode:
                    val = eval(val)
                if type(var) == type(val):
                    vars[iy][1] = val
                    srvrs = [item[0] for item in self.servers if item[3]==ix]
                    newVal = val if type(var).__name__ == 'unicode' else str(val)
                    msg = "%s=%s" % (variable, newVal)
                    for srvr in srvrs:
                        self.send_data_all(msg, indx=[i[0] for i in self.servers].index(srvr))
                    return val
                else:
                    eg.PrintError(
                        self.text.invType % (
                            variable,
                            type(var).__name__,
                            unicode(val),
                            type(val).__name__
                        )
                    )
            else:
                eg.PrintError(self.text.notName % (prot,var))
        else:
            eg.PrintError(self.text.unknSrvCls % prot)


    def ChangePersistVar(self, protType, prot, varType, variable, value):
        prot = eg.ParseString(prot)
        var = eg.ParseString(variable)
        tmpList = [item[0] for item in Persist.userVariables]
        if prot in tmpList:
            ix = tmpList.index(prot)
            vars = Persist.userVariables[ix][1]
            tmpList = [i[0] for i in vars]
            if var in tmpList:
                iy = tmpList.index(var)
                var = vars[iy][1]
                if value == 2: # 2 ~ Toggle boolean
                    if type(var) is bool:
                        vars[iy][1] = not var
                    else:
                        eg.PrintError(self.text.notBool % variable)
                elif abs(value) == 1: # 1/-1 ~ Increment/Decrement integer
                    if type(var) is int:
                        vars[iy][1] = var + value
                    else:
                        eg.PrintError(self.text.notInt % variable)
                if abs(value):
                    srvrs = [item[0] for item in self.servers if item[3]==ix]
                    msg = "%s=%s" % (variable, str(vars[iy][1]))
                    for srvr in srvrs:
                        self.send_data_all(msg, indx=[i[0] for i in self.servers].index(srvr))  
                return vars[iy][1]
            else:
                eg.PrintError(self.text.notVar % (prot,var))
        else:
            eg.PrintError(self.text.unknSrvCls % prot)


    def BroadcastMessage(self, txt, port, message, modeHost):
        host = eg.ParseString(txt)
        port = int(eg.ParseString(port))
        if modeHost < 2:
            titles = [item[1] for item in self.servers]
            if host in titles:
                ix = titles.index(host)
                srvr = self.servers[ix][0].getsockname()
                host = srvr[0]
                port = srvr[1]
            else:
                eg.PrintError(self.text.servError1 % host)
                return 1
        elif modeHost == 2:
            host = GetIPAddress(host, self.text)
        tmpLst = [item[0].getsockname() for item in self.servers]
        if (host, port) in tmpLst:
            ix = tmpLst.index((host, port))
            for client in self.servers[ix][2]:
                self.send_data(client, message)
            return 0
        else:
            eg.PrintError(self.text.servError2 % (host, port))
            return 2


    def ServerSendMessage(self, txt, port, message, modeHost, cl_ip, cl_port, modeClient):
        host = eg.event.payload[0] if modeHost == 1 else eg.ParseString(txt)
        port = int(eg.ParseString(port))
        message = eg.ParseString(message)
        client = eg.event.payload[1] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if modeHost < 2:
            titles = [item[1] for item in self.servers]
            if host in titles:
                ix = titles.index(host)
                srvr = self.servers[ix][0].getsockname()
                host = srvr[0]
                port = srvr[1]
            else:
                eg.PrintError(self.text.servError1 % host)
                return 1
        elif modeHost == 2:
            host = GetIPAddress(host, self.text)
        tmpLst = [item[0].getsockname() for item in self.servers]
        if (host, port) in tmpLst:
            ix = tmpLst.index((host, port))
            tmpList = [i.getpeername() for i in self.servers[ix][2]]
            if client in tmpList:
                iy = tmpList.index(client)
                self.send_data(self.servers[ix][2][iy], message)
                return 0
            else:
                eg.PrintError(self.text.servMessError % (self.servers[ix][1], str(client)))
                return 2


    def StartServer(
        self,
        ipaddress,
        port,
        maxCon,
        title,
        interact
    ):
        if title in [item[1] for item in self.servers]:
            eg.PrintError(self.text.startError1 % title)
            return 1
        tmpLst = [item[0].getsockname() for item in self.servers]
        tmpList = [item[0] for item in tmpLst if item[0] == port]
        if ipaddress == "0.0.0.0" and tmpList:
            eg.PrintError(self.text.startError2 % self.text.allIfaces)
            eg.PrintError(self.text.anotherPort % port)
            return 2
        if tmpList and tmpList[0] == "0.0.0.0":
            eg.PrintError(self.text.startError3 % self.text.allIfaces)
            eg.PrintError(self.text.anotherPort % port)
            return 3
        if not (ipaddress, port) in tmpLst:
            try:
                srvr = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                srvr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                srvr.bind ((ipaddress, port))
                srvr.listen(maxCon)
                if not self.serverHandler:
                    self.clientsServers = {}
                    self.servers = [[srvr,title,[],interact],]
                    self.connected = []
                    self.clnProtocols = {}
                    self.inputs = [srvr,]
                    self.serverHandler = Thread(target = self.ServerHandler, name = "WebsocketServerHandler")
                    self.serverHandler.start()
                else:
                    self.servers.append([srvr, title, [], interact])
                    self.inputs.append(srvr)
                folder = self.dataSet[interact][3][3]
                self.updateLogFile(folder, title, self.text.servStart, True)
                return 0

            except socket.error, exc:
                raise self.Exception(exc[1])
                return 4
        else:
            address = ipaddress if ipaddress else self.text.allIfaces
            eg.PrintError(self.text.startError5 % (address, port))
            return 5


    def StopAllServers(self):
        if self.serverHandler:
            self.inputs = []
            return 0
        else:
            return 1


    def StopServer(self, txt, port, modeHost):
        host = eg.ParseString(txt)
        port = int(eg.ParseString(port))
        if modeHost < 2:
            titles = [item[1] for item in self.servers]
            if host in titles:
                ix = titles.index(host)
                srvr = self.servers[ix][0].getsockname()
                host = srvr[0]
                port = srvr[1]
            else:
                eg.PrintError(self.text.servError1 % host)
                return 1
        elif modeHost == 2:
            host = GetIPAddress(host, self.text)
        tmpLst = [item[0].getsockname() for item in self.servers]
        if (host, port) in tmpLst:
            ix = tmpLst.index((host, port))
            srvr = self.servers[ix][0]
            self.serverToStop.append(srvr)
            return 0
        else:
            eg.PrintError(self.text.servError2 % (host, port))
            return 2
#===============================================================================

class StartServer(eg.ActionBase):

    class text:
        maxCon = "Max number of connections"
        serverName = "Server title"
        

    def __call__(self, txt="0.0.0.0", port="1234", maxCon=100, title = "Server", mode = 0, interact=-1):
        title = eg.ParseString(title)
        txt = eg.ParseString(txt)
        port = int(eg.ParseString(port))
        if not mode :            
            txt = GetIPAddress(txt, self.plugin.text)
        return self.plugin.StartServer(txt, port, maxCon, title, interact)


    def GetLabel(self, txt, port, maxCon, title, mode, interact):
        return "%s: %s: %s:%s" % (self.name, title, txt, port)


    def Configure(self, txt="", port="1234", maxCon=100, title = "Server", mode = 0, interact=-1):
        port = str(port)
        text = self.plugin.text
        panel = eg.ConfigPanel()

        titleCtrl = wx.TextCtrl(panel,-1,title)
        titleSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.serverName),
            wx.HORIZONTAL
        )
        titleSizer.Add(titleCtrl, 0, wx.EXPAND)
        panel.sizer.Add(titleSizer, 0, wx.EXPAND)

        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice[2:],
            style=wx.RA_SPECIFY_ROWS
        )

        radioBoxMode.SetSelection(mode)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(text)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxMode,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((10,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.EXPAND|wx.TOP, 8)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id = wx.NewId()
        id2 = wx.NewId()

        def OnHostChoice(evt = None):
            text = self.plugin.text
            middleSizer = panel.sizer.GetItem(1).GetSizer()
            dynamicSizer = middleSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            middleSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            middleSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            txtLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode+2]+":")
            if mode ==0:
                ifaces = GetInterfaces(text)
                txtCtrl = wx.Choice(panel,id,choices = ifaces)
                if not evt:
                    txtCtrl.SetStringSelection(txt)        
            elif mode == 1:
                txtCtrl = wx.TextCtrl(panel,id,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            portLabel = wx.StaticText(panel,-1,text.port)
            portCtrl = wx.TextCtrl(panel,id2,"")
            portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        maxConCtrl = eg.SpinIntCtrl(panel,-1,maxCon, max=1000)
        staticBox = wx.StaticBox(panel, -1, self.text.maxCon)
        maxConnSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        maxConnSizer.Add(maxConCtrl, 0, wx.TOP, 10)
        eg.EqualizeWidths((titleCtrl, radioBoxMode))
        width = titleCtrl.GetMinSize()[0]
        maxConnSizer.SetMinSize((width+4, -1))
        bottomSizer.Add(maxConnSizer, 0, wx.EXPAND)

        staticBox = wx.StaticBox(panel, -1, text.interactSrv)
        interactSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        bagSizer = wx.GridBagSizer(9, 6)
        defLabel = wx.StaticText(panel, -1, self.plugin.text.default)
        w, h = defLabel.GetSize()
        protocols = [i[0] for i in Persist.userVariables]
        interactChoice = wx.Choice(panel, -1, choices = protocols, size = (w, -1))
        rb1 = wx.RadioButton(panel, -1, "", style=wx.RB_GROUP)
        rb1.SetValue(interact == -1)
        rb2 = wx.RadioButton(panel, -1, "")
        rb2.SetValue(interact > -1)
        bagSizer.Add(rb1,(0,0),(1,1),flag = wx.TOP, border = 8)
        bagSizer.Add(rb2,(1,0),(1,1),flag = wx.TOP, border = 2)
        bagSizer.Add(defLabel,(0,1),(1,1),flag = wx.TOP, border = 8)
        bagSizer.Add(interactChoice,(1,1),(1,1))
        interactSizer.Add(bagSizer, 0, wx.EXPAND)
        bottomSizer.Add(interactSizer, 1, wx.EXPAND|wx.LEFT, 10)
        panel.sizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 8)

        def onChangeMode(evt=None):
            enbl = rb2.GetValue()
            defLabel.Enable(not enbl)
            interactChoice.Enable(enbl)
            sel = -1
            if enbl and interactChoice.GetStrings():
                if interact == -1:
                    sel = 0
                else:
                    sel = interact
            interactChoice.SetSelection(sel)                
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        onChangeMode()        

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id).GetStringSelection()
            elif mode == 1:
                txt = wx.FindWindowById(id).GetValue()

            panel.SetResult(
                txt,
                wx.FindWindowById(id2).GetValue(),
                maxConCtrl.GetValue(),
                titleCtrl.GetValue(),
                mode,
                -1 if rb1.GetValue() else interactChoice.GetSelection()
            )
#===============================================================================

class BroadcastMessage(eg.ActionBase):

    def __call__(self, txt = "0.0.0.0", port = "1234", message = "Test", modeHost = 0):
        message = eg.ParseString(message)
        return self.plugin.BroadcastMessage(txt, port, message, modeHost)


    def GetLabel(self, txt, port, message, modeHost):
        if modeHost == 0:
            return "%s: %s: %s" % (self.name, txt, message)
        elif modeHost == 1:
            return "%s: {eg.event.payload[0]}: %s" % (self.name, message)
        else:
            return "%s: %s:%s: %s" % (self.name, txt, port, message)


    def Configure(self, txt = "", port = "1234", message = "Test", modeHost = 0):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(modeHost)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(text)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(radioBoxMode,0,wx.LEFT|wx.EXPAND)
        topSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        topSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id = wx.NewId()
        id2 = wx.NewId()

        def OnHostChoice(evt = None):
            text = self.plugin.text
            topSizer = panel.sizer.GetItem(0).GetSizer()
            dynamicSizer = topSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            topSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            topSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode]+":")
            if mode ==2:
                ifaces = GetInterfaces(text)
                txtCtrl = wx.Choice(panel,id,choices = ifaces)
                if not evt:
                    txtCtrl.SetStringSelection(txt)        
            elif mode in (0,3):
                txtCtrl = wx.TextCtrl(panel,id,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            if mode > 1:
                portLabel = wx.StaticText(panel,-1,text.port)
                portCtrl = wx.TextCtrl(panel,id2,"")
                if not evt:
                    portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()

        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()

        messCtrl = wx.TextCtrl(panel, -1, message)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )        
        panel.sizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 15)
        messSizer.Add(messCtrl, 0, wx.EXPAND)

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id).GetValue()
                port = "1234"
            elif mode == 1:
                txt = "{eg.event.payload[0]}"
                port = "1234"
            elif mode == 2:
                txt = wx.FindWindowById(id).GetStringSelection()
                port = wx.FindWindowById(id2).GetValue()
            else: #mode == 3
                txt = wx.FindWindowById(id).GetValue()
                port = wx.FindWindowById(id2).GetValue()
            panel.SetResult(
                txt,
                port,
                messCtrl.GetValue(),
                mode
            )
#===============================================================================

class ServerSendMessage(eg.ActionBase):

    def __call__(
        self,
        txt = "127.0.0.1",
        port = "1234",
        message = "Test",
        modeHost = 0,
        cl_ip="127.0.0.1",
        cl_port = "1234",
        modeClient = 1
    ):
        return self.plugin.ServerSendMessage(
            txt,
            port,
            message,
            modeHost,
            cl_ip,
            cl_port,
            modeClient
        )


    def GetLabel(self, txt, port, message, modeHost, cl_ip, cl_port, modeClient):
        if modeHost == 0:
            return "%s: %s: %s" % (self.name, txt, message)
        elif modeHost == 1:
            return "%s: {eg.event.payload[0]}: %s" % (self.name, message)
        else:
            return "%s: %s:%s: %s" % (self.name, txt, port, message)


    def Configure(
        self,
        txt = "",
        port = "",
        message = "Test",
        modeHost = 0,
        cl_ip="127.0.0.1",
        cl_port = "1234",
        modeClient = 1
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(modeHost)
        ifaces = GetInterfaces(text)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        staticBox = wx.StaticBox(panel, -1, "")
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(radioBoxMode,0,wx.LEFT|wx.EXPAND)
        topSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        topSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id1 = wx.NewId()
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()

        def OnHostChoice(evt = None):
            text = self.plugin.text
            topSizer = panel.sizer.GetItem(0).GetSizer()
            dynamicSizer = topSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            topSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            topSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode]+":")
            if mode ==2:
                ifaces = GetInterfaces(text)
                txtCtrl = wx.Choice(panel,id1,choices = ifaces)
                if not evt:
                    txtCtrl.SetStringSelection(txt)        
            elif mode in (0,3):
                txtCtrl = wx.TextCtrl(panel,id1,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            if mode > 1:
                portLabel = wx.StaticText(panel,-1,text.port)
                portCtrl = wx.TextCtrl(panel,id2,"")
                if not evt:
                    portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()

        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()

        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            text.modeClientChoiceLabel,
            choices = text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetMinSize((radioBoxMode.GetSize()[0], -1))
        radioBoxModeClient.SetSelection(modeClient)

        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        txtCtrl.SetMinSize(minSize)
        portLabel = wx.StaticText(panel,-1,text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        panel.sizer.Layout()            
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            text = self.plugin.text
            middleSizer = panel.sizer.GetItem(1).GetSizer()
            dynamicSizer = middleSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            middleSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size2)
            middleSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxModeClient.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.host)
            txtCtrl = wx.TextCtrl(panel, id3, cl_ip)
            txtCtrl.SetMinSize(minSize)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            portLabel = wx.StaticText(panel,-1,text.port)
            portCtrl = wx.TextCtrl(panel, id4, cl_port)
            dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
            dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        messCtrl = wx.TextCtrl(panel, -1, message)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )        
        panel.sizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 8)
        messSizer.Add(messCtrl, 0, wx.EXPAND)


        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id1).GetValue()
            elif mode == 2:
                txt = wx.FindWindowById(id1).GetStringSelection()
                port = wx.FindWindowById(id2).GetValue()
            elif mode == 3:
                txt = wx.FindWindowById(id1).GetValue()
                port = wx.FindWindowById(id2).GetValue()
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            panel.SetResult(
                txt,
                port,
                messCtrl.GetValue(),
                mode,
                cl_ip,
                cl_port,
                modeClient
            )
#===============================================================================

class StopServer(eg.ActionBase):

    def __call__(self, txt="0.0.0.0", port="1234", modeHost = 1):
        return self.plugin.StopServer(txt, port, modeHost)


    def GetLabel(self, txt, port, modeHost):
        if modeHost == 0:
            return "%s: %s" % (self.name, txt)
        elif modeHost == 1:
            return "%s: {eg.event.payload[0]}" % self.name
        else:
            return "%s: %s:%s" % (self.name, txt, port)


    def Configure(self, txt="", port="1234", modeHost = 1):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(modeHost)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(text)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(radioBoxMode,0,wx.LEFT|wx.EXPAND)
        topSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        topSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id = wx.NewId()
        id2 = wx.NewId()

        def OnHostChoice(evt = None):
            text = self.plugin.text
            topSizer = panel.sizer.GetItem(0).GetSizer()
            dynamicSizer = topSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            topSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            topSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode]+":")
            if mode ==2:
                ifaces = GetInterfaces(text)
                txtCtrl = wx.Choice(panel,id,choices = ifaces)
                if not evt:
                    txtCtrl.SetStringSelection(txt)        
            elif mode in (0,3):
                txtCtrl = wx.TextCtrl(panel,id,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            if mode > 1:
                portLabel = wx.StaticText(panel,-1,text.port)
                portCtrl = wx.TextCtrl(panel,id2,"")
                if not evt:
                    portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()


        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id).GetValue()
                port = "1234"
            elif mode == 1:
                txt = "{eg.event.payload[0]}"
                port = "1234"
            elif mode == 2:
                txt = wx.FindWindowById(id).GetStringSelection()
                port = wx.FindWindowById(id2).GetValue()
            else: #mode == 3
                txt = wx.FindWindowById(id).GetValue()
                port = wx.FindWindowById(id2).GetValue()
            panel.SetResult(
                txt,
                port,
                mode
            )
#===============================================================================

class StopAllServers(eg.ActionBase):

    def __call__(self):
        return self.plugin.StopAllServers()
#===============================================================================

class StartClient(eg.ActionBase):

    class text:
        clientName = "Client title"
        netBoxClient = "Host network settings"
        protLabel = "Websocket protocol"
        protocols = (
            "Old hixie 75 or 76",
            "New ietf hybi 7 or above"
        )


    def __call__(self, host, port, title, interact, prot):
        return self.plugin.StartClient(host, port, title, interact, prot)


    def GetLabel(self, host, port, title, interact):
        return "%s: %s: %s:%s: %i" % (self.name, title, host, port, interact, prot)


    def Configure(self, host="0.0.0.0", port="1234", title="Client", interact=0, prot = 0):
        text = self.plugin.text
        panel = eg.ConfigPanel()

        titleCtrl = wx.TextCtrl(panel,-1,title)
        titleSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.clientName),
            wx.HORIZONTAL
        )

        hostLabel = wx.StaticText(panel,-1,text.host)
        hostCtrl = wx.TextCtrl(panel,-1,host)
        portLabel = wx.StaticText(panel,-1,text.port)
        portCtrl = wx.TextCtrl(panel,-1,port)
        netSizer = wx.GridBagSizer(10, 8)
        topSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.netBoxClient),
            wx.HORIZONTAL
        )

        staticBox = wx.StaticBox(panel, -1, text.interactCln)
        interactSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        bagSizer = wx.GridBagSizer(9, 6)
        defLabel = wx.StaticText(panel, -1, self.plugin.text.default)
        interactChoice = wx.Choice(panel, -1, choices = [])
        interactChoice.SetSelection(interact-1)
        rb1 = wx.RadioButton(panel, -1, "", style=wx.RB_GROUP)
        rb1.SetValue(interact == 0)
        rb2 = wx.RadioButton(panel, -1, "")
        rb2.SetValue(interact > 0)

        titleSizer.Add(titleCtrl, 0, wx.EXPAND)
        netSizer.Add(hostLabel,(0,0),(1,1),flag = wx.TOP, border = 3)
        netSizer.Add(hostCtrl,(0,1),(1,1))
        netSizer.Add(portLabel,(1,0),(1,1),flag = wx.TOP, border = 3)
        netSizer.Add(portCtrl,(1,1),(1,1))
        bagSizer.Add(rb1,(0,0),(1,1),flag = wx.TOP, border = 8)
        bagSizer.Add(rb2,(1,0),(1,1),flag = wx.TOP, border = 2)
        bagSizer.Add(defLabel,(0,1),(1,1),flag = wx.TOP, border = 8)
        bagSizer.Add(interactChoice,(1,1),(1,1))
        topSizer.Add(netSizer, 0, wx.EXPAND)
        interactSizer.Add(bagSizer, 0, wx.EXPAND)
        panel.sizer.Add(titleSizer, 0, wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.TOP,8)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        radioBoxProt = wx.RadioBox(
            panel,
            -1,
            self.text.protLabel,
            choices = self.text.protocols,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxProt.SetSelection(prot)
        bottomSizer.Add(radioBoxProt, 1, wx.EXPAND)
        bottomSizer.Add(interactSizer, 1, wx.LEFT|wx.EXPAND, 10)
        panel.sizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP,8)
        panel.sizer.Layout()
        rect = hostCtrl.GetRect()
        xr = rect[0]+rect[2]
        xl = titleCtrl.GetRect()[0]
        titleCtrl.SetMinSize((xr-xl, -1))
        xl = interactChoice.GetRect()[0]
        interactChoice.SetMinSize((xr-xl, -1))

        def onChangeMode(evt=None):
            enbl=rb1.GetValue()
            defLabel.Enable(enbl)
            interactChoice.Enable(not enbl)
            if enbl:
                interactChoice.SetSelection(-1)
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        onChangeMode()

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                titleCtrl.GetValue(),
                0 if rb1.GetValue() else 1 + interactChoice.GetSelection(),
                radioBoxProt.GetSelection()
            )
#===============================================================================

class StopClient(eg.ActionBase):

    def __call__(self, txt, port, modeClient):
        return self.plugin.StopClient(txt, port, modeClient)


    def GetLabel(self, txt, port, modeClient):
        if modeClient == 0:
            return "%s: %s" % (self.name, txt)
        elif modeClient == 1:
            return "%s: {eg.event.payload[0]}" % self.name
        else:
            return "%s: %s:%s" % (self.name, txt, port)


    def Configure(self, txt="", port="1234", modeClient = 1):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeUserChoiceLabel,
            choices = text.modeUserChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        id = wx.NewId()
        id2 = wx.NewId()
        tmpSizer = wx.GridBagSizer(2, 10)
        dummyCtrl = wx.StaticText(panel,-1,text.modeUserChoice[2]+":")
        txtCtrl = wx.TextCtrl(panel,id,"")
        portLabel = wx.StaticText(panel,-1,text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(dummyCtrl,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(radioBoxMode,1,wx.LEFT|wx.EXPAND)
        topSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        topSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        size = (tmpSizer.GetMinSize()[0]+10, tmpSizer.GetMinSize()[1]+1)
        minSize = (dummyCtrl.GetSize()[0]+10, -1)

        def OnClientChoice(evt = None):
            text = self.plugin.text
            topSizer = panel.sizer.GetItem(0).GetSizer()
            dynamicSizer = topSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            topSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            topSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.modeUserChoice[mode]+":")      
            if mode in (0, 2):
                txtCtrl = wx.TextCtrl(panel,id,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            if mode == 2:
                portLabel = wx.StaticText(panel,-1,text.port)
                portCtrl = wx.TextCtrl(panel,id2,"")
                if not evt:
                    portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id).GetValue()
                port = "1234"
            elif mode == 1:
                txt = "{eg.event.payload[0]}"
                port = "1234"
            else: #mode == 2
                txt = wx.FindWindowById(id).GetValue()
                port = wx.FindWindowById(id2).GetValue()
            panel.SetResult(
                txt,
                port,
                mode
            )
#===============================================================================
class ClientSendMessage(eg.ActionBase):

    def __call__(self, txt, port, modeClient, message):
        return self.plugin.ClientSendMessage(txt, port, modeClient, message)


    def GetLabel(self, txt, port, modeClient, message):
        if modeClient == 0:
            return "%s: %s: %s" % (self.name, txt, message)
        elif modeClient == 1:
            return "%s: {eg.event.payload[0]}: %s" % (self.name, message)
        else:
            return "%s: %s:%s: %s" % (self.name, txt, port, message)


    def Configure(self, txt="", port="1234", modeClient=0, message = "Test"):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeUserChoiceLabel,
            choices = text.modeUserChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(text)
        id = wx.NewId()
        id2 = wx.NewId()
        tmpSizer = wx.GridBagSizer(2, 10)
        dummyCtrl = wx.StaticText(panel,-1,text.modeUserChoice[2]+":")
        txtCtrl = wx.TextCtrl(panel,id,"")
        portLabel = wx.StaticText(panel,-1,text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(dummyCtrl,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(radioBoxMode,0,wx.LEFT|wx.EXPAND)
        topSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        topSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        panel.sizer.Layout()
        size = (tmpSizer.GetMinSize()[0]+10,tmpSizer.GetMinSize()[1]+1)
        minSize = (dummyCtrl.GetSize()[0]+10, -1)

        def OnClientChoice(evt = None):
            text = self.plugin.text
            topSizer = panel.sizer.GetItem(0).GetSizer()
            dynamicSizer = topSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            topSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            topSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            if mode == 1:
                if evt:
                    evt.Skip()
                return
            txtLabel = wx.StaticText(panel,-1,text.modeUserChoice[mode]+":")
            if mode in (0,2):
                txtCtrl = wx.TextCtrl(panel,id,"")
                txtCtrl.SetMinSize(minSize)
                if not evt:
                    txtCtrl.ChangeValue(txt)
            if mode == 2:
                portLabel = wx.StaticText(panel,-1,text.port)
                portCtrl = wx.TextCtrl(panel,id2,"")
                if not evt:
                    portCtrl.ChangeValue(port)
            dynamicSizer.Add(txtLabel,(0,0),(1,1))
            dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(3,0),(1,1))
            panel.sizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        messCtrl = wx.TextCtrl(panel, -1, message)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )        
        panel.sizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 15)
        messSizer.Add(messCtrl, 0, wx.EXPAND)

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                txt = wx.FindWindowById(id).GetValue()
                port = "1234"
            elif mode == 1:
                txt = "{eg.event.payload[0]}"
                port = "1234"
            else: #mode == 2
                txt = wx.FindWindowById(id).GetValue()
                port = wx.FindWindowById(id2).GetValue()
            panel.SetResult(
                txt,
                port,
                mode,
                messCtrl.GetValue(),
            )
#===============================================================================

class GetValue(eg.ActionBase):

    def __call__(self, protType=1, prot="", varType = 1, variable=""):
        return self.plugin.ChangePersistVar(protType, prot, varType, variable, self.value)


    def GetLabel(self, protType, prot, varType, var):
        return u"%s(%s, %s)" % (self.name, prot, var)


    def Configure(self, protType=1, prot="", varType = 1, var=""):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        panel.prot = prot
        panel.var = var
        protSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.prot),
            wx.HORIZONTAL
        )
        varSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.var),
            wx.HORIZONTAL
        )
        panel.sizer.Add(protSizer, 0, wx.LEFT, 15)
        panel.sizer.Add(varSizer, 0, wx.LEFT|wx.TOP, 15)

        rb3 = wx.RadioButton(panel, -1, text.radioChoices[0], style=wx.RB_GROUP)
        rb3.SetValue(varType)
        rb4 = wx.RadioButton(panel, -1, text.radioChoices[1])
        rb4.SetValue(not varType)
        varLeftSizer = wx.BoxSizer(wx.VERTICAL)
        varLeftSizer.Add(rb3,0,flag = wx.TOP|wx.BOTTOM, border = 6)
        varLeftSizer.Add((1,6))
        varLeftSizer.Add(rb4,0,flag = wx.TOP|wx.BOTTOM, border = 3)
        varSizer.Add(varLeftSizer,1,wx.EXPAND)

        rb1 = wx.RadioButton(panel, -1, text.radioChoices[0], style=wx.RB_GROUP)
        rb1.SetValue(protType)
        rb2 = wx.RadioButton(panel, -1, text.radioChoices[1])
        rb2.SetValue(not protType)
        protLeftSizer = wx.BoxSizer(wx.VERTICAL)
        protLeftSizer.Add(rb1,0,flag = wx.TOP|wx.BOTTOM, border = 6)
        protLeftSizer.Add((1,6))
        protLeftSizer.Add(rb2,0,flag = wx.TOP|wx.BOTTOM, border = 3)
        protSizer.Add(protLeftSizer,1,wx.EXPAND)

        def onVarChoice(evt):
            if isinstance(self.varCtrl, wx.Choice):
                panel.var = self.varCtrl.GetStringSelection()
            else:
                panel.var = self.varCtrl.GetValue()
            evt.Skip()


        def onProtChoice(evt = None):
            if isinstance(self.protCtrl, wx.Choice):
                panel.prot = self.protCtrl.GetStringSelection()
            else:
                panel.prot = self.protCtrl.GetValue()
            tmpList = [i[0] for i in Persist.userVariables]
            if panel.prot in tmpList:
                rb3.Enable(True)
                onChangeModeVar()
            else:
                rb3.SetValue(False)
                rb3.Enable(False)
                rb4.SetValue(True)
                onChangeModeVar()
            if evt:
                evt.Skip()


        def onChangeModeVar(evt = None):
            if len(varSizer.GetChildren()) == 2:
                dynSizer = varSizer.GetItem(1).GetSizer()
                dynSizer.Clear(True)
                varSizer.Detach(dynSizer)
                dynSizer.Destroy()
            dynSizer = wx.BoxSizer(wx.VERTICAL)
            varSizer.Add(dynSizer,0,wx.LEFT|wx.EXPAND,10)
            tmpList = [i[0] for i in Persist.userVariables]
            if panel.prot in tmpList:
                ix = tmpList.index(panel.prot)
                tmpList = Persist.userVariables[ix][1]
                choices = [item[0] for item in tmpList]
                if self.value == 2:  #2 ~ Toggle boolean 
                    choices = [item[0] for item in tmpList if type(item[1]) is bool]
                elif abs(self.value) == 1:  #1/-1 ~ Increment/Decrement integer 
                    choices = [item[0] for item in tmpList if type(item[1]) is int]
                else:           #0 ~ Get value
                    choices = [item[0] for item in tmpList]
            else:
                choices = []
            ctrl_0 = wx.Choice(
                    panel,
                    -1,
                    choices = choices,
                    size = (200,-1)
                )
            ctrl_1 = wx.TextCtrl(
                    panel,
                    -1,
                    size = ctrl_0.GetSize()
                )
            if rb3.GetValue():
                self.varCtrl = ctrl_0
                dummyCtrl = ctrl_1
                self.varCtrl.SetStringSelection(panel.var)
                self.varCtrl.Bind(wx.EVT_CHOICE, onVarChoice)
            else:
                self.varCtrl = ctrl_1
                dummyCtrl = ctrl_0
                self.varCtrl.ChangeValue(panel.var)
                self.varCtrl.Bind(wx.EVT_TEXT, onVarChoice)
            dynSizer.Add(ctrl_0,0,wx.TOP)
            dynSizer.Add((1,8),1,wx.EXPAND)
            dynSizer.Add(ctrl_1,0,wx.BOTTOM)
            varSizer.Layout()
            dummyCtrl.Show(False)
            if evt is not None:
                evt.Skip()


        def onChangeModeProt(evt = None):
            if len(protSizer.GetChildren()) == 2:
                dynSizer = protSizer.GetItem(1).GetSizer()
                dynSizer.Clear(True)
                protSizer.Detach(dynSizer)
                dynSizer.Destroy()
            dynSizer = wx.BoxSizer(wx.VERTICAL)
            protSizer.Add(dynSizer,0,wx.LEFT|wx.EXPAND,10)
            ctrl_0 = wx.Choice(
                    panel,
                    -1,
                    choices = [item[0] for item in Persist.userVariables],
                    size = (200,-1)
                )
            ctrl_1 = wx.TextCtrl(
                    panel,
                    -1,
                    size = ctrl_0.GetSize()
                )
            if rb1.GetValue():
                self.protCtrl = ctrl_0
                dummyCtrl = ctrl_1
                self.protCtrl.SetStringSelection(panel.prot)
                self.protCtrl.Bind(wx.EVT_CHOICE, onProtChoice)
            else:
                self.protCtrl = ctrl_1
                dummyCtrl = ctrl_0
                self.protCtrl.ChangeValue(panel.prot)
                self.protCtrl.Bind(wx.EVT_TEXT, onProtChoice)
            dynSizer.Add(ctrl_0,0,wx.TOP)
            dynSizer.Add((1,8),1,wx.EXPAND)
            dynSizer.Add(ctrl_1,0,wx.BOTTOM)
            protSizer.Layout()
            dummyCtrl.Show(False)
            onProtChoice()
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeModeProt)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeModeProt)
        rb3.Bind(wx.EVT_RADIOBUTTON, onChangeModeVar)
        rb4.Bind(wx.EVT_RADIOBUTTON, onChangeModeVar)
        onChangeModeProt()

        while panel.Affirmed():
            panel.SetResult(
                rb1.GetValue(),
                panel.prot,
                rb3.GetValue(),
                panel.var
            )
#===============================================================================

class SetValue(eg.ActionBase):

    def __call__(self, protType=1, prot="", varType = 1, variable="", val = u""):
        return self.plugin.SetPersistVar(protType, prot, varType, variable, val)


    def GetLabel(self, protType, prot, varType, var, val):
        return u"%s(%s, %s) = %s" % (self.name, prot, var, val)


    def Configure(self, protType=1, prot="", varType = 1, var="", val = u""):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        panel.prot = prot
        panel.var = var
        panel.val = val
        protSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.prot),
            wx.HORIZONTAL
        )
        varSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.var),
            wx.HORIZONTAL
        )
        valSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.valLabel),
            wx.HORIZONTAL
        )
        valCtrl = wx.TextCtrl(panel, -1, panel.val, size = (200,-1))
        valSizer.Add(valCtrl)
        panel.sizer.Add(protSizer, 0, wx.LEFT|wx.EXPAND|wx.RIGHT, 15)
        panel.sizer.Add(varSizer, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.EXPAND|wx.RIGHT, 15)
        panel.sizer.Add(valSizer, 0, wx.LEFT|wx.EXPAND|wx.RIGHT, 15)

        rb3 = wx.RadioButton(panel, -1, text.radioChoices[0], style=wx.RB_GROUP)
        rb3.SetValue(varType)
        rb4 = wx.RadioButton(panel, -1, text.radioChoices[1])
        rb4.SetValue(not varType)
        varLeftSizer = wx.BoxSizer(wx.VERTICAL)
        varLeftSizer.Add(rb3,0,flag = wx.TOP|wx.BOTTOM, border = 6)
        varLeftSizer.Add((1,6))
        varLeftSizer.Add(rb4,0,flag = wx.TOP|wx.BOTTOM, border = 3)
        varSizer.Add(varLeftSizer,1,wx.EXPAND)

        rb1 = wx.RadioButton(panel, -1, text.radioChoices[0], style=wx.RB_GROUP)
        rb1.SetValue(protType)
        rb2 = wx.RadioButton(panel, -1, text.radioChoices[1])
        rb2.SetValue(not protType)
        protLeftSizer = wx.BoxSizer(wx.VERTICAL)
        protLeftSizer.Add(rb1,0,flag = wx.TOP|wx.BOTTOM, border = 6)
        protLeftSizer.Add((1,6))
        protLeftSizer.Add(rb2,0,flag = wx.TOP|wx.BOTTOM, border = 3)
        protSizer.Add(protLeftSizer,1,wx.EXPAND)

        def onValChoice(evt):
            panel.val = evt.GetString()
            evt.Skip()
        valCtrl.Bind(wx.EVT_TEXT, onValChoice)

        def onVarChoice(evt = None):
            if isinstance(self.varCtrl, wx.Choice):
                panel.var = self.varCtrl.GetStringSelection()
            else:
                panel.var = self.varCtrl.GetValue()
            value = None
            tmpList = [i[0] for i in Persist.userVariables]
            if panel.prot in tmpList:
                ix = tmpList.index(panel.prot)
                tmpList = [item[0] for item in Persist.userVariables[ix][1]]
                if panel.var in tmpList:
                    iy = tmpList.index(panel.var)
                    value = Persist.userVariables[ix][1][iy][1]
            valCtrl = valSizer.GetItem(0).GetWindow()
            if isinstance(valCtrl, wx.Choice):
                valCtrl.Unbind(wx.EVT_CHOICE)
            else:
                valCtrl.Unbind(wx.EVT_TEXT)
            valSizer.Detach(valCtrl)
            valCtrl.Destroy()
            if type(value) is bool:
                choices = (u"True", u"False")
                valCtrl = wx.Choice(panel, -1, choices = choices, size = (200,-1))
                valCtrl.Bind(wx.EVT_CHOICE, onValChoice)
                if panel.val in choices:
                    valCtrl.SetStringSelection(panel.val)
            else:
                valCtrl = wx.TextCtrl(panel, -1, "", size = (200,-1))
                valCtrl.Bind(wx.EVT_TEXT, onValChoice)
                flg = True
                if panel.val and not type(value) in (unicode, str):
                    try:
                        flg = type(eval(panel.val)) == type(value)
                    except:
                        flg = False
                if flg:
                    valCtrl.ChangeValue(panel.val)
            valSizer.Add(valCtrl)
            valSizer.Layout()
            if evt:        
                evt.Skip()


        def onProtChoice(evt = None):
            if isinstance(self.protCtrl, wx.Choice):
                panel.prot = self.protCtrl.GetStringSelection()
            else:
                panel.prot = self.protCtrl.GetValue()
            tmpList = [i[0] for i in Persist.userVariables]
            if panel.prot in tmpList:
                rb3.Enable(True)
                onChangeModeVar()
            else:
                rb3.SetValue(False)
                rb3.Enable(False)
                rb4.SetValue(True)
                onChangeModeVar()
            if evt:
                evt.Skip()


        def onChangeModeVar(evt = None):
            if len(varSizer.GetChildren()) == 2:
                dynSizer = varSizer.GetItem(1).GetSizer()
                dynSizer.Clear(True)
                varSizer.Detach(dynSizer)
                dynSizer.Destroy()
            dynSizer = wx.BoxSizer(wx.VERTICAL)
            varSizer.Add(dynSizer,0,wx.LEFT|wx.EXPAND,10)
            tmpList = [i[0] for i in Persist.userVariables]
            if panel.prot in tmpList:
                ix = tmpList.index(panel.prot)
                tmpList = Persist.userVariables[ix][1]
                choices = [item[0] for item in tmpList]
            else:
                choices = []
            ctrl_0 = wx.Choice(
                    panel,
                    -1,
                    choices = choices,
                    size = (200,-1)
                )
            ctrl_1 = wx.TextCtrl(
                    panel,
                    -1,
                    size = ctrl_0.GetSize()
                )
            if rb3.GetValue():
                self.varCtrl = ctrl_0
                dummyCtrl = ctrl_1
                self.varCtrl.SetStringSelection(panel.var)
                self.varCtrl.Bind(wx.EVT_CHOICE, onVarChoice)
            else:
                self.varCtrl = ctrl_1
                dummyCtrl = ctrl_0
                self.varCtrl.ChangeValue(panel.var)
                self.varCtrl.Bind(wx.EVT_TEXT, onVarChoice)
            dynSizer.Add(ctrl_0,0,wx.TOP)
            dynSizer.Add((1,8),1,wx.EXPAND)
            dynSizer.Add(ctrl_1,0,wx.BOTTOM)
            varSizer.Layout()
            dummyCtrl.Show(False)
            onVarChoice()
            if evt is not None:
                evt.Skip()


        def onChangeModeProt(evt = None):
            if len(protSizer.GetChildren()) == 2:
                dynSizer = protSizer.GetItem(1).GetSizer()
                dynSizer.Clear(True)
                protSizer.Detach(dynSizer)
                dynSizer.Destroy()
            dynSizer = wx.BoxSizer(wx.VERTICAL)
            protSizer.Add(dynSizer,0,wx.LEFT|wx.EXPAND,10)
            ctrl_0 = wx.Choice(
                    panel,
                    -1,
                    choices = [item[0] for item in Persist.userVariables],
                    size = (200,-1)
                )
            ctrl_1 = wx.TextCtrl(
                    panel,
                    -1,
                    size = ctrl_0.GetSize()
                )
            if rb1.GetValue():
                self.protCtrl = ctrl_0
                dummyCtrl = ctrl_1
                self.protCtrl.SetStringSelection(panel.prot)
                self.protCtrl.Bind(wx.EVT_CHOICE, onProtChoice)
            else:
                self.protCtrl = ctrl_1
                dummyCtrl = ctrl_0
                self.protCtrl.ChangeValue(panel.prot)
                self.protCtrl.Bind(wx.EVT_TEXT, onProtChoice)
            dynSizer.Add(ctrl_0,0,wx.TOP)
            dynSizer.Add((1,8),1,wx.EXPAND)
            dynSizer.Add(ctrl_1,0,wx.BOTTOM)
            protSizer.Layout()
            dummyCtrl.Show(False)
            onProtChoice()
            if evt is not None:
                evt.Skip()

        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeModeProt)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeModeProt)
        rb3.Bind(wx.EVT_RADIOBUTTON, onChangeModeVar)
        rb4.Bind(wx.EVT_RADIOBUTTON, onChangeModeVar)
        onChangeModeProt()

        while panel.Affirmed():
            panel.SetResult(
                rb1.GetValue(),
                panel.prot,
                rb3.GetValue(),
                panel.var,
                panel.val
            )
#===============================================================================

ACTIONS = (
    ( eg.ActionGroup, 'ServerActions', 'Server actions', 'Server actions',(
        (StartServer, 'StartServer', 'Start server', 'Starts server.', None),
        (StopServer, 'StopServer', 'Stop server', 'Stops server.', None),
        (StopAllServers, 'StopAllServers', 'Stop all servers', 'Stops all servers.', None),
        (BroadcastMessage, 'BroadcastMessage', 'Broadcast message', 'Broadcasts message to all clients.', None),
        (ServerSendMessage, 'ServerSendMessage', 'Server send message', 'Server sends message to one client.', None),
        )),
    ( eg.ActionGroup, 'ClientActions', 'Client actions', 'Client actions',(
        (StartClient, 'StartClient', 'Start client', 'Starts client.', None),
        (StopClient, 'StopClient', 'Stop client', 'Stops client.', None),
        (ClientSendMessage, 'ClientSendMessage', 'Client send message', 'Client sends message.', None),
        )),
    ( eg.ActionGroup, 'PersistentVariables', 'Persistent variables', 'Persistent variables',(
        (GetValue, 'GetValue', 'Get value', 'Gets value of persistent variable.', 0),
        (SetValue, 'SetValue', 'Set value', 'Sets value of persistent variable.', None),
        (GetValue, 'ToggleBoolean', 'Toggle boolean', 'Toggle boolean value.', 2),
        (GetValue, 'IncrementInteger', 'Increment integer value', 'Increment integer value.', 1),
        (GetValue, 'DecrementInteger', 'Decrement integer value', 'Decrement integer value.', -1),
        )),
)

            