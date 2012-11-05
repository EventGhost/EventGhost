# -*- coding: utf-8 -*-
version = "0.1.1"
#
# plugins/HTTPExplorer/__init__.py
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
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
# 0.1.1  by Pako 2012-11-05 11:11 UTC+1
#      - bugfixes - redirect when "All interfaces" is selected
#                 - StopServer really perform stop
# 0.1.0  by Pako 2012-11-02 17:54 UTC+1
#      - extensive reworking for increased stability
#      - added option to open a file using the default application
#      - added the possibility of triggering events for folders
#      - added option to return to any higher level
#      - incorporated limit -  it is impossible to enter below the server root
# 0.0.4  by Pako 2012-10-19 16:45 UTC+1
#      - bugfix (error, when "Start server" is not configured) 
# 0.0.3  by Pako 2012-10-17 10:54 UTC+1
#      - bugfix (border colour) 
#      - added option to select the font size and width of the border 
# 0.0.2  by Pako 2012-10-11 14:08 UTC+1
#      - support url link updated 
# 0.0.1  by Pako 2012-10-11 13:30 UTC+1
#      - initial version 
#===============================================================================

eg.RegisterPlugin(
    name = "HTTP explorer",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{6AF3AF9A-D0F3-4DA8-8508-25BE61FB1914}",
    description = u"""<rst>HTTP explorer.""",
    createMacrosOnAdd = True,
    canMultiLoad = False,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=4048",
    icon = (
        "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"
        "64E+/Bc/aiZBTOJ7EgAAAABJRU5ErkJggg=="
    ),
)

import pythoncom
import _winreg
from os import listdir, startfile
from os.path import abspath, join, dirname, isdir, isfile, split, splitext
from win32api import LoadLibrary, LoadString, GetVolumeInformation
from win32com.shell import shell
from win32file import GetFileAttributesW, GetLogicalDrives
from fnmatch import fnmatch
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from zlib import decompress
from sys import getfilesystemencoding
FSE = getfilesystemencoding()

FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ICON = decompress(
    'x\x9c\x95T\xc9J\xc3P\x14}\xa2\xe0RWnu\xe9_(\x88\x14\x07\x1c7E\xacU\x1cq'
    '\xc0\x19Dl\x14\xad\x1bQ\x91"(\xb8\x11\x07p\xe1\xc2?\x10\x04]\xf8\x01\n'
    '\x82b\x9bjS\x92&)m\xa5U\xdb\xe3\xbd\xa98\xd0\x16\xeb\x0b\'\x90\x9bw\xee='
    '\xf7\xbc\x9b\x08Q@Wi\xa9\xa0{\x85\x18*\x12\xa2L\x08QI\xa0\x10E\xd2qk\x15'
    '\x89\x8c\x05\xe0\x0b\x86$\xc1\\ZB\xe2\xe8\x08\xa9\xbb;\xe9\xe7\xbb|\xf0'
    '\xdc\xd1\x01oM\r\x9e\xedv\x98n7\xde/.\xcea\x18U\xf9\xf2\x03\x9d\x9d\x90[Z'
    '\xe0\xb5\xd9 74@\x1d\x1dE\xfc\xe0\x00\xa9\xfb\xfb\xbc\xb4\x04\x1c\x0e\x04'
    '\x9cN\x04\xfb\xfb\xe1on\x86\xb7\xb6\x16\xac)\xb2\xb1\x81\xf7\xcb\xcb\xf3?'
    '\xf9]]\x08\x0e\x0c 4=\rud\x04O\xd4\x07\xe7\xf056"4;\x8b\xc4\xc9\tR\x9a\x96'
    '\xb3\x1f\x85\xf8\xea\xf00\x8c\x85\x05\xe8\xb4_\x1d\x1b\x83Bz|uuV\x1e\xa5'
    '\xa7\x07\xb1\xedm$\xaf\xaf\xb3j\xe1\xbd\xea\xc4\x04\xc2++0\\.\x84ff\xa0'
    '\x8e\x8fC\xe9\xed\x85\x9f}!o\xfd\xad\xad\x08\xb3\xb7WW\x199\x98\xafMM!'
    '\xb2\xb6\x86\xf0\xeaj:\x07\xeb\xa0\x1c\x96\'\xed\xedx\xac\xae\x86\xbf\xad'
    '\r\xb1\x9d\x1d\xc04\x7f\xf5\xa2twC\xa3\x9a\x91\xcdMD\xd6\xd7\xbfsP,\xd8'
    '\xd7\x07\xb9\xa9\xc9\xea\x83s%\x8e\x8f\x91Q\x9f\xf8\xfa\xdc\x1c\xa2\x1e'
    '\x0f\xa2[[\x96\xef\xe6\xf2\xb2\xe5\xa9L\x1e\xb2\x0f\xecI\xfc\xf0\x10\xd0'
    '\xf5\x0c\x1f\x99\xcf\xde\xc5vw\x11%\x9f\xc2\xcc\xa5\xba\xbe\xfazK;\xcf\xe6'
    '\xdb\xd9\x19r\xcd\x14\xf3\xb9\xde\xcb\xde\x1ex\x96y\x0e\xb9fpp\xd0\xca\x99'
    '\xcb\xf7/>\x9d\x0f\xf3\xb4\xc9I\xc84?\x0c}~\x1e\xaf\xa7\xa7Y\xf5f\x9b?'
    '\x9e;\xd6\xcb\xb3\xc4\x1ed;\xa7\x9c\xf5I?\x9f\r\xd7\x8f\xef\xef#\xf5\xf0'
    '\xf0\xafo0y{+%on\xa4\xff\xf0d\x08\xf1\xc8X$\x94\x13J\x08\x85\x84\x82\x1f'
    '\xe0\xe7\xe2\xcfwU\xe9\xbd^\xf0\xbfC\x88\x0f\xef\x02\xfb\xa2'
)

#global variables:
MY_COMPUTER = None
LOG = False
#===============================================================================

class Text:
    myComp   = u"My computer"
    startMess= u'HTTP explorer: Server "%s" started on host %s'
    stopMess = u'HTTP explorer: Server "%s" on %s stopped'
    listhl = u"Currently enabled servers:"
    colLabels = (
        u"Server name",
        u"Host/Interface",
        u"Port",
        u"Event",
        u"Server state",
    )
    stop = u"Stop"
    stopAll = u"Stop all"
    start = u"Start/Restart"
    startAll = u"Start/Restart all"
    refresh = u"Refresh"
    running = u"Running"
    stopped = u"Stopped"
    txtAllIfaces = u'All available interfaces'    
#===============================================================================

def convertColor(color):
    return "#%02x%02x%02x" % (color[0], color[1], color[2])
#===============================================================================

def GetInterfaces(txtAllIfaces):    
    cards = [txtAllIfaces, 'localhost']
    try:
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards"
        )
        for i in range(_winreg.QueryInfoKey(y)[0]):
            yy = _winreg.OpenKey(y,_winreg.EnumKey(y,i))
            cards.append(_winreg.QueryValueEx(yy, "Description")[0])
            _winreg.CloseKey(yy)
    except:
        raise #ToDo
    _winreg.CloseKey(y)
    return cards


def GetIPAddress(card, txtAllIfaces):
    if card == 'localhost':
        return "127.0.0.1"
    if card == txtAllIfaces:
        return "0.0.0.0"
    cards=[]
    try:
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards"
        )
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
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\%s" % guid
        )
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

class Browser(object):

    def __init__ (
        self,
        prefix,
        suffix,
        patterns,
        hide,
        strt,
        suffixD
    ):
        self.prefix = prefix
        self.suffix = suffix
        self.suffixD = suffixD
        self.patterns = patterns.split(",")
        self.hide = hide
        self.folder = self.start = strt

        self.shortcut = pythoncom.CoCreateInstance (
          shell.CLSID_ShellLink,
          None,
          pythoncom.CLSCTX_INPROC_SERVER,
          shell.IID_IShellLink
        )
        self.persist_file = self.shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        self.GoHome()



    def GoHome(self):
        self.Parents = []
        self.path = ""
        self.folder = self.start
        self.GetFolderItems(self.start)


    def CaseInsensitiveSort(self, list):
        tmp = [(item[0].upper(), item) for item in list] # Schwartzian transform
        tmp.sort()
        return [item[1] for item in tmp]


    def GetFolderItems(self, folder):
        try:
            fldr = folder.decode(FSE) if not isinstance(folder, unicode) else folder
        except eg.Exception, exc:
            eg.PrintError(unicode(exc))
        except:
            eg.PrintTraceback(
                eg.text.Error.InAction % "Start HTTP server", 1, source=self
            )
        self.folder = fldr
        if fldr != MY_COMPUTER:
            ds = []
            fs = []
            try:
                items = list(listdir(fldr))
                for ix,i in enumerate(items):
                    itm = i.decode(FSE) if not isinstance(i, unicode) else i
            except:
                self.ds = ds
                self.fs = fs
            for f in [f for f in items if isdir(join(fldr, f))]:
                if self.hide:
                    attr = GetFileAttributesW(join(fldr, f))
                    if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                        continue
                ds.append((f,u""))
            for f in [f for f in items if isfile(join(fldr, f))]:
                if splitext(f)[1].lower() == ".lnk":
                    shortcut_path = join(fldr, f)
                    self.persist_file.Load(shortcut_path)
                    pth = self.shortcut.GetPath(shell.SLGP_RAWPATH)[0]
                    f = split(shortcut_path)[1][:-4]
                    if self.hide:
                        attr = GetFileAttributesW(pth)
                        if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                            continue
                    if isdir(pth):
                        if not f in ds:
                            ds.append((f,pth))
                            continue
                    elif isfile(pth):
                        for p in self.patterns:
                            if fnmatch(split(pth)[1],p.strip()):
                                if not f in fs:
                                    fs.append((f,pth))
                                break
                else:
                    if self.hide:
                        attr = GetFileAttributesW(join(fldr,f))
                        if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                            continue
                    for p in self.patterns:
                        if fnmatch(f, p.strip()):
                            if not f in fs:
                                fs.append((f, u""))
                            break
            self.ds = self.CaseInsensitiveSort(ds)
            self.fs = self.CaseInsensitiveSort(fs)
        else: #pseudo-folder "My computer"
            self.drives = []
            mask = 1
            ordA = ord('A')
            drivebits = GetLogicalDrives()
            for c in range(26):
                if drivebits & mask:
                    drv = '%c:\\' % chr(ordA+c)
                    if isdir(drv):
                        try:
                            name = GetVolumeInformation(drv)[0]
                            self.drives.append(("%s (%s)" % (
                                name,
                                drv[:2]),
                                u""
                            ))
                        except:
                            pass
                mask = mask << 1
            self.ds = self.drives[:]
            self.fs = []
            self.folder = MY_COMPUTER


    def TriggEvent(self, pth):
        ev = pth.find("/Evnt")
        p = pth[:ev]
        if p == self.path:
            ix = pth[ev+5:]
            if ix:
                ix = int(ix)
                if ix < len(self.ds):
                    itm = self.ds[ix]
                    suffix = self.suffixD
                else:
                    itm = self.fs[ix-len(self.ds)]
                    suffix = self.suffix
                if self.folder == MY_COMPUTER:
                    fl = itm[0][-3:-1] + "\\"
                else:
                    fl = itm[1] if itm[1] else join(self.folder, itm[0])
                eg.TriggerEvent(suffix, prefix = self.prefix, payload = fl)


    def Open(self, pth):
        op = pth.find("/Open")
        p = pth[:op]
        if p == self.path: # open file
            ix = pth[op+5:]
            if ix:
                ix = int(ix)-len(self.ds)
                itm = self.fs[ix]
                fl = itm[1] if itm[1] else join(self.folder, itm[0])
                if isfile(fl):
                    startfile(fl)
        else:
            pList=p.split("/")
            pathList=self.path.split("/")
            if len(pList) > len(pathList):
                if pList[:-1] == pathList: # go to folder (child)
                    self.path=p
                    self.Parents.append(self.folder)
                    ix=int(pth[1+p.rfind("/"):op]) 
                    itm = self.ds[ix]           
                    if self.folder == MY_COMPUTER:
                        fldr = itm[0][-3:-1] + "\\"
                    else:
                        fldr = itm[1] if itm[1] else join(self.folder, itm[0])
                    self.GetFolderItems(fldr)


    def GetTitle(self, fl):
        if not len(fl)==3:
            return split(fl)[1]
        else:   
            ix = [item[0][-3:-1] + "\\" for item in self.drives].index(fl)
            return self.drives[ix][0]
    

    def GoToParent(self, pth):
        p = pth[:pth.find("/Parent")]
        while self.path>p:
            self.folder = self.Parents.pop()
            self.path = self.path[:self.path.rfind("/")]
        self.GetFolderItems(self.folder)
#===============================================================================

class HTTP_handler(BaseHTTPRequestHandler):
    """The user-provided request handler class.
        An instance of this class is created for each request."""

    server_version = "EventGhost_HTTP_explorer/%s" % version
    protocol_version = "HTTP/1.1"

    def __init__(self, request, client_address, server):
        try:
            BaseHTTPRequestHandler.__init__(
                self,
                request,
                client_address,
                server
            )
        except:
            pass


    def log_message(self, format, *args):
        if LOG:
            logName = "HTTPserver_%s.log" % self.server.title.replace(" ", "_")
            try:
                logfile = abspath(join(dirname(__file__), logName))
                open(logfile, "a").write("%s -- %s - %s:  %s\n" % ( 
                    self.log_date_time_string(),
                    self.client_address,
                    self.address_string(),
                    format % args
                ))
            except eg.Exception, exc:
                eg.PrintError(unicode(exc))
            except:
                eg.PrintTraceback(
                    eg.text.Error.InAction % 
                    "BaseHTTPRequestHandler.log_message", 1, source = self
                )


    def InconsistencyCheck(self, browser):
        if self.path.find("/Home")>-1:
            return False
        fndOpn=self.path.find("/Open")
        pth = self.path[:self.path.rfind("/")]
        if len(self.path)-fndOpn == 5:
            if pth.split("/")[:-1] == browser.path.split("/"):
                return False
        if fndOpn > -1 and len(self.path) - fndOpn > 5:
            if pth == browser.path[:len(pth)]:
                return False
        if self.path=='/' and browser.path=="":
            return False
        if self.path.find("/Parent")>-1:
            if pth == browser.path[:len(pth)]:
                return False
        if self.path.find("/Evnt")>-1 and pth==browser.path:
            return False
        return True


    def WriteWfile(self, page):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header("Content-Length", str(len(page)))  
            self.end_headers()
            self.wfile.write(page)
        except:
            pass


    def Reset(self, srvr):
        self.WriteWfile(u'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type"  content="text/html; charset=utf-8">
<title>%s</title>
<script type="text/javascript">
function start()
{document.location.href = "http://%s:%i";}
window.onload = start; 
</script>
</head>''' % (
            srvr.title,
            self.request.getsockname()[0],
            self.request.getsockname()[1]
        ))


    def do_GET (self):
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.send_header("Content-Length", len(ICON))
            self.end_headers()
            self.wfile.write(ICON)
            return    
        srvr = self.server
        browser = srvr.browser
        if self.InconsistencyCheck(browser):
            browser.GoHome()
            self.Reset(srvr)
            return            
        if "/Parent" in self.path:
            browser.GoToParent(self.path)
        elif "/Evnt" in self.path:
            browser.TriggEvent(self.path)
        elif "/Open" in self.path:
            browser.Open(self.path)
        elif "/Home" in self.path:
            browser.GoHome()         
        htmlPage = u'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type"  content="text/html; charset=utf-8">
<title>%s</title>
<style type="text/css">
body {background-color: %s;}
table {border-collapse: collapse; padding: 0px; font-family: Arial, Helvetica, sans-serif; font-size: %ipx;} 
tr {border: %ipx solid %s;}
.evnt {border: %ipx solid %s;  cursor: pointer;}
.open {border-top: %ipx solid %s; border-bottom: %ipx solid %s;  cursor: pointer;}
.filN {background-color: %s; color: %s;}
.filH {background-color: %s; color: %s;} 
.folN {background-color: %s; color: %s;}
.folH {background-color: %s; color: %s;}
.tran {border: 0px; background: transparent; cursor: auto; color: %s}
.trn2 {border-top-style: hidden;border-bottom-style: hidden; border-right: %ipx solid %s; background: transparent; cursor: auto;width: %ipx }
</style>      
<script type="text/javascript">
function start()
{
var table = document.getElementById("myTable");
var clickAction = function(cl){
  r = cl.parentNode.rowIndex;
  pth = "%s";
  if (pth.length>0){
    arPath = pth.split("/");
    path = arPath.slice(0,1+r).join("/");
  }
  else {
    arPath = "";
    path = "";
  }
  if (cl.parentNode.className =="back") {
    ixs=[0,1,2,3];
    cmd = path+"/Parent";
  }
  else {
    r = (r - arPath.length).toString();
    ixs=[2,3];
    cmd=pth+"/"+r+"/Evnt";
    if (ixs.indexOf(cl.cellIndex)>-1){
      if (cl.parentNode.parentNode.className == 'folder'){cmd =pth+"/"+r+"/Open";}
      else {cmd=pth+"/Open"+r;}
    }
    else if (cl.cellIndex==0) {cmd=pth+"/Evnt"+r;} 
  }
    document.location.href = "http://%s:%i"+cmd;
};
var mouseOut = function(cl){
 if (cl.parentNode.className =="back") {ixs=[0,1,2,3];}
 else {ixs=[2,3];}
 if (cl.parentNode.parentNode.className == 'folder'){cls = 'folN ';}
 else {cls = 'filN ';}
 if (ixs.indexOf(cl.cellIndex)>-1)
  {
    cls += 'open';
    row=cl.parentNode;
    for(var i = 0; i < ixs.length; i++){row.cells[ixs[i]].className = cls;}
  }
 else if (cl.cellIndex==0)
  {
    cls += 'evnt';
    cl.className = cls;
  }		  
};   
var mouseOver = function(cl){
 if (cl.parentNode.className =="back") {ixs=[0,1,2,3];}
 else {ixs=[2,3];}
 if (cl.parentNode.parentNode.className == 'folder'){cls = 'folH ';}
 else{cls = 'filH ';}
 if (ixs.indexOf(cl.cellIndex)>-1)
  {
    cls += 'open';
    row=cl.parentNode;
    for(var i = 0; i < ixs.length; i++){row.cells[ixs[i]].className = cls;}
  }
 else if (cl.cellIndex==0)
  {
    cls += 'evnt';
    cl.className = cls;
  }		  
};     
 for(var r = 0; r < table.rows.length; r++){
   var row = table.rows[r];
     for(var c = 0; c < row.cells.length; c++){
       if (row.className != "tran"){
         var	cell = row.cells[c];
         cell.onmouseout  = function() {mouseOut(this);}
         cell.onmouseover = function() {mouseOver(this);}
         cell.onclick = function() {clickAction(this);}   
         cell.onmouseout();
       }
     } 
   }
}
window.onload = start; 
</script>
</head>
<body><table id="myTable">''' % (
    srvr.title, srvr.bckGround, srvr.fontsize, srvr.brdrwdth, srvr.border,
    srvr.brdrwdth, srvr.border, srvr.brdrwdth, srvr.border, srvr.brdrwdth, srvr.border,
    srvr.filIdlBck, srvr.filIdlTxt, srvr.filActBck,srvr.filActTxt,
    srvr.folIdlBck, srvr.folIdlTxt, srvr.folActBck,srvr.folActTxt,
    srvr.border, srvr.brdrwdth, srvr.border, srvr.fontsize/8,
    browser.path, self.request.getsockname()[0], self.request.getsockname()[1]
)
        if browser.Parents:
            parents = [srvr.title]
            for par in browser.Parents[1:]:
                parents.append(browser.GetTitle(par))
            htmlPage += '<tbody class="folder">'
            for par in parents:
                htmlPage += u'<tr class="back"><td>▲&nbsp;</td><td></td><td>%s</td><td>&nbsp;▲</td></tr>' % par
            title = browser.GetTitle(browser.folder)
            htmlPage += '</tbody><tr class="tran"><td></td><td></td><td>%s</td><td></td></tr>' % title
        if browser.ds:
            htmlPage += '<tbody class="folder">'
            for itm in [item[0] for item in browser.ds]:
                htmlPage += u'<tr><td>&nbsp;✈&nbsp;</td><td class="trn2"></td><td>&nbsp;%s</td><td>&nbsp;►</td></tr>' % itm
            htmlPage += '</tbody>'
        if browser.fs:
            htmlPage += '<tbody class="file">'
            for itm in [item[0] for item in browser.fs]:
                htmlPage += u'<tr><td>&nbsp;✈&nbsp;</td><td class="trn2"></td><td>&nbsp;%s</td><td></td></tr>' % itm
            htmlPage += '</tbody>'
        htmlPage += u"</table></body></html>"
        htmlPage = htmlPage.encode("UTF-8")
        self.WriteWfile(htmlPage)
    do_HEAD = do_GET
    do_POST = do_GET       
#===============================================================================

class HTTP_server(HTTPServer):

    def __init__(
        self,
        plugin,
        server_address,
        RequestHandlerClass,
        browser,
        title,
        bckGround,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        strt,
        fontsize,
        brdrwdth,
    ):
        self.browser   = browser
        self.title     = title
        self.bckGround = bckGround
        self.border    = border
        self.filIdlTxt = filIdlTxt
        self.filIdlBck = filIdlBck
        self.filActTxt = filActTxt
        self.filActBck = filActBck
        self.folIdlTxt = folIdlTxt
        self.folIdlBck = folIdlBck
        self.folActTxt = folActTxt
        self.folActBck = folActBck
        self.strt      = strt
        self.fontsize  = fontsize
        self.brdrwdth  = brdrwdth
        plugin.servers[title] = self
        self.req = None
        eg.PrintNotice(plugin.text.startMess % (title,"%s:%i" % server_address))
        HTTPServer.__init__(
            self,
            server_address,
            RequestHandlerClass
        )


    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True


    def get_request(self):
        while self.run:
            try:
                self.req = self.socket.accept()
                self.req[0].settimeout(None)              
                return self.req
            except socket.timeout:
                pass


    def stop(self):
        self.run = False
        if self.req:
            self.req[0].shutdown(2)
            self.req[0].close()
        self.req = None


    def serve(self):
        while self.run:
            self.handle_request()     
#===============================================================================

class HTTP_thread (Thread):

    def __init__ (
        self,
        plugin,
        browser,
        iface,
        port,
        title,
        bckGround,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        strt,
        fontsize,
        brdrwdth,
        ):
        Thread.__init__(self)
        self.plugin    = plugin
        self.handler   = HTTP_handler
        self.browser   = browser
        self.iface     = iface
        self.port      = port
        self.title     = title
        self.bckGround = bckGround
        self.border    = border
        self.filIdlTxt = filIdlTxt
        self.filIdlBck = filIdlBck
        self.filActTxt = filActTxt
        self.filActBck = filActBck
        self.folIdlTxt = folIdlTxt
        self.folIdlBck = folIdlBck
        self.folActTxt = folActTxt
        self.folActBck = folActBck
        self.strt      = strt
        self.fontsize  = fontsize
        self.brdrwdth  = brdrwdth
        self.server    = None


    def run (self):
        self.server = HTTP_server(
            self.plugin,
            (self.iface, self.port),
            self.handler,
            self.browser,
            self.title,
            self.bckGround,
            self.border,
            self.filIdlTxt,
            self.filIdlBck,
            self.filActTxt,
            self.filActBck,
            self.folIdlTxt,
            self.folIdlBck,
            self.folActTxt,
            self.folActBck,
            self.strt,
            self.fontsize,
            self.brdrwdth,
        )
        self.server.serve()
#===============================================================================
#cls types for ACTIONS list :
#===============================================================================

class StartServer(eg.ActionBase):

    class text:
        bckgrnd = u'Background colour'
        border = u'Border colour'
        fontsize = u'Font size (px):'
        brdrwdth = u'Border width (px):'
        filIdleText = u'File idle item text colour'
        filIdleBack = u'File idle item background colour'
        filActivText = u'File active item text colour'
        filActivBack = u'File active item background colour'
        folIdleText = u'Folder idle item text colour'
        folIdleBack = u'Folder idle item background colour'
        folActivText = u'Folder active item text colour'
        folActivBack = u'Folder active item background colour'
        prefixLabel = u'Event prefix:'
        suffixLabel = u'Event suffix (file):'
        suffixLabelD = u'Event suffix (folder):'
        folder = u"Server root:"
        browseTitle = u"Selected folder:"
        hide = u"Ignore system and hidden files and folders"
        patterns = u"Show only the files corresponding to these patterns:"
        compBtnToolTip = u'Press this button to set "%s" as server root'
        patternsToolTip = u'''Here you can enter the patterns of required files, separated by commas.
For example, *.mp3, *.ogg, *.flac or e*.ppt, g*.ppt and the like.u'''
        port = u"TCP/IP port:"
        modeHostChoiceLabel = u'Server host address to specify as'
        modeHostChoice = (
            u'Server title (or Python expression)',
            u'Server title from eg.event.payload[0]',
            u'Interface',
            u'Server IP address (or Python expression)',
        )
        serverName = u"Server name (must be unique !!!) and server root"
        titleLabel = u"Server name:"


    def __call__(
        self,
        title = "",
        mode = 0,
        iFace = "localhost",
        port = "8080",
        bckgrnd   = (245, 215, 255),
        border    = (0, 0, 0),
        filIdlTxt = (74, 74, 74),
        filIdlBck = (183, 183, 255),
        filActTxt = (183, 183, 255),
        filActBck = (74, 74, 74),
        folIdlTxt = (128, 0, 0),
        folIdlBck = (243, 237, 109),
        folActTxt = (243, 237, 109),
        folActBck = (128, 0, 0),
        prefix    = "HTTPE",
        suffix    = "File",
        strt      = u"",
        patterns  = "*.*",
        hide      = True,
        fontsize  = 32,
        brdrwdth  = 1,
        suffixD = "Folder"
    ):
        self.plugin.StartServer(
            title,
            mode,
            iFace,
            port,
            bckgrnd,
            border,
            filIdlTxt,
            filIdlBck,
            filActTxt,
            filActBck,
            folIdlTxt,
            folIdlBck,
            folActTxt,
            folActBck,
            prefix,
            suffix,
            strt,
            patterns,
            hide,
            fontsize,
            brdrwdth,
            suffixD,
        )
 

    def GetLabel(
        self,
        title,
        mode,
        iFace,
        port,
        bckgrnd,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        prefix,
        suffix,
        strt,
        patterns,
        hide,
        fontsize,
        brdrwdth,
        suffixD,
    ):
        if title:
            self.plugin.AddServerName(title)
        return '%s: %s  (%s: %s)' % (self.name, title, iFace, port)


    def Configure(
        self,
        title = "",
        mode = 0,
        iFace = "localhost",
        port = "8080",
        bckgrnd   = (245, 215, 255),
        border    = (0, 0, 0),
        filIdlTxt = (74, 74, 74),
        filIdlBck = (183, 183, 255),
        filActTxt = (183, 183, 255),
        filActBck = (74, 74, 74),
        folIdlTxt = (128, 0, 0),
        folIdlBck = (243, 237, 109),
        folActTxt = (243, 237, 109),
        folActBck = (128, 0, 0),
        prefix = 'HTTPE',
        suffix = 'File',
        strt = u"",
        patterns = "*.*",
        hide = True,
        fontsize = 32,
        brdrwdth = 1,
        suffixD = "Folder",
    ):
        panel = eg.ConfigPanel(self)
        mainSizer = panel.sizer
        text = self.text
        if not patterns:
            patterns = "*.*"
        if not isdir(strt) and strt != MY_COMPUTER:
            strt = eg.folderPath.Documents
        titleLabel = wx.StaticText(panel,-1,self.text.titleLabel)
        titleCtrl = wx.TextCtrl(panel, -1, title)
        folderLabel = wx.StaticText(panel, -1, text.folder)
        folderCtrl = eg.DirBrowseButton(
            panel, 
            dialogTitle = text.browseTitle,
            buttonText = eg.text.General.browse,
        )
        compBtn = wx.Button(panel, -1, MY_COMPUTER)
        compBtn.SetToolTip(wx.ToolTip(text.compBtnToolTip % MY_COMPUTER))
        folderCtrl.SetValue(strt)
        folderCtrl.startDirectory = strt       
        folderSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderSizer.Add(folderCtrl,1,wx.EXPAND)
        folderSizer.Add(compBtn,0,wx.LEFT,20)
        topSizer = wx.FlexGridSizer(2, 2, 10, 5)
        topSizer.AddGrowableCol(1)
        topSizer.Add(titleLabel,0,wx.TOP,3)
        topSizer.Add(titleCtrl, 0, wx.EXPAND)
        topSizer.Add(folderLabel,0,wx.TOP,3)
        topSizer.Add(folderSizer,0,wx.EXPAND) 
        statSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.serverName),
            wx.VERTICAL
        )
        statSizer.Add(topSizer,1,wx.EXPAND)
        mainSizer.Add(statSizer, 0, wx.EXPAND)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice[2:],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(self.plugin.text.txtAllIfaces)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxMode,0,wx.LEFT)
        middleSizer.Add((10,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        mainSizer.Add(middleSizer, 0, wx.EXPAND|wx.TOP, 8)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id = wx.NewId()
        id2 = wx.NewId()

        def OnHostChoice(evt = None):
            middleSizer = mainSizer.GetItem(1).GetSizer()
            dynamicSizer = middleSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            middleSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            middleSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            iFaceLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode+2]+":")
            if mode ==0:
                ifaces = GetInterfaces(self.plugin.text.txtAllIfaces)
                ifaceCtrl = wx.Choice(panel,id,choices = ifaces)
                if not evt:
                    ifaceCtrl.SetStringSelection(iFace)        
            elif mode == 1:
                ifaceCtrl = wx.TextCtrl(panel,id,"")
                ifaceCtrl.SetMinSize(minSize)
                if not evt:
                    ifaceCtrl.ChangeValue(iFace)
            portLabel = wx.StaticText(panel,-1,text.port)
            portCtrl = wx.TextCtrl(panel,id2,"")
            portCtrl.ChangeValue(port)
            dynamicSizer.Add(iFaceLabel,(0,0),(1,1),flag = wx.TOP, border = 10)
            dynamicSizer.Add(ifaceCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(0,1),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(1,1),(1,1))
            mainSizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()

        prefixLbl=wx.StaticText(panel, -1, text.prefixLabel)
        prefixCtrl = wx.TextCtrl(panel,-1,prefix)
        suffixLbl=wx.StaticText(panel, -1, text.suffixLabel)
        suffixLblD=wx.StaticText(panel, -1, text.suffixLabelD)
        suffixCtrl = wx.TextCtrl(panel,-1,suffix)
        suffixCtrlD = wx.TextCtrl(panel,-1,suffixD)
        bckgrndLbl   = wx.StaticText(panel, -1, text.bckgrnd+':')
        borderLbl    = wx.StaticText(panel, -1, text.border+':')
        fontsizeLbl  = wx.StaticText(panel, -1, text.fontsize)
        brdrwdthLbl  = wx.StaticText(panel, -1, text.brdrwdth)
        filIdlTxtLbl = wx.StaticText(panel, -1, text.filIdleText+':')
        filIdlBckLbl = wx.StaticText(panel, -1, text.filIdleBack+':')
        filActTxtLbl = wx.StaticText(panel, -1, text.filActivText+':')
        filActBckLbl = wx.StaticText(panel, -1, text.filActivBack+':')
        folIdlTxtLbl = wx.StaticText(panel, -1, text.folIdleText+':')
        folIdlBckLbl = wx.StaticText(panel, -1, text.folIdleBack+':')
        folActTxtLbl = wx.StaticText(panel, -1, text.folActivText+':')
        folActBckLbl = wx.StaticText(panel, -1, text.folActivBack+':')
        fontsizeCtrl = eg.SpinIntCtrl(panel, -1, fontsize, max = 999, min = 16)
        brdrwdthCtrl = eg.SpinIntCtrl(panel, -1, brdrwdth, max = 9, min = 0)
        bckgrndColourButton = eg.ColourSelectButton(
            panel,
            bckgrnd,
            title = text.bckgrnd,
            size = (100, -1)
        )
        borderColourButton = eg.ColourSelectButton(
            panel,
            border,
            title = text.border,
            size = (100, -1)
        )
        filIdlTxtColourButton = eg.ColourSelectButton(
            panel,
            filIdlTxt,
            title = text.filIdleText,
            size = (100, -1)
        )
        filIdlBckColourButton = eg.ColourSelectButton(
            panel,
            filIdlBck,
            title = text.filIdleBack,
            size = (100, -1)
        )
        filActTxtColourButton = eg.ColourSelectButton(
            panel,
            filActTxt,
            title = text.filActivText,
            size = (100, -1)
        )
        filActBckColourButton = eg.ColourSelectButton(
            panel,
            filActBck,
            title = text.filActivBack,
            size = (100, -1)
        )

        folIdlTxtColourButton = eg.ColourSelectButton(
            panel,
            folIdlTxt,
            title = text.folIdleText,
            size = (100, -1)
        )
        folIdlBckColourButton = eg.ColourSelectButton(
            panel,
            folIdlBck,
            title = text.folIdleBack,
            size = (100, -1)
        )
        folActTxtColourButton = eg.ColourSelectButton(
            panel,
            folActTxt,
            title = text.folActivText,
            size = (100, -1)
        )
        folActBckColourButton = eg.ColourSelectButton(
            panel,
            folActBck,
            title = text.folActivBack,
            size = (100, -1)
        )

        eg.EqualizeWidths((
            fontsizeCtrl,
            brdrwdthCtrl,
            prefixCtrl,
            suffixCtrl,
            suffixCtrlD,
            bckgrndColourButton,
            borderColourButton,
            filIdlTxtColourButton,
            filIdlBckColourButton,
            filActTxtColourButton,
            filActBckColourButton,
            folIdlTxtColourButton,
            folIdlBckColourButton,
            folActTxtColourButton,
            folActBckColourButton,
            ))

        patternsLabel = wx.StaticText(panel, -1, text.patterns)
        patternsCtrl = wx.TextCtrl(panel,-1,patterns)
        patternsCtrl.SetToolTip(wx.ToolTip(text.patternsToolTip))
        hideSystem = wx.CheckBox(panel, -1, text.hide)
        hideSystem.SetValue(hide)
        #Sizers
        colorSizer=wx.FlexGridSizer(7, 4, 10, 5)
        mainSizer.Add(colorSizer,0,wx.TOP,10)
        colorSizer.Add(fontsizeLbl,0)
        colorSizer.Add(fontsizeCtrl,0,wx.TOP,-2)
        colorSizer.Add(brdrwdthLbl,0,wx.LEFT,30)
        colorSizer.Add(brdrwdthCtrl,0,wx.TOP,-2)
        colorSizer.Add(bckgrndLbl,0)
        colorSizer.Add(bckgrndColourButton,0,wx.TOP,-2)
        colorSizer.Add(borderLbl,0,wx.LEFT,30)
        colorSizer.Add(borderColourButton,0,wx.TOP,-2)
        colorSizer.Add(filIdlTxtLbl,0)
        colorSizer.Add(filIdlTxtColourButton,0,wx.TOP,-2)
        colorSizer.Add(folIdlTxtLbl,0,wx.LEFT,30)
        colorSizer.Add(folIdlTxtColourButton,0,wx.TOP,-2)
        colorSizer.Add(filIdlBckLbl,0)
        colorSizer.Add(filIdlBckColourButton,0,wx.TOP,-2)
        colorSizer.Add(folIdlBckLbl,0,wx.LEFT,30)
        colorSizer.Add(folIdlBckColourButton,0,wx.TOP,-2)
        colorSizer.Add(filActTxtLbl,0)
        colorSizer.Add(filActTxtColourButton,0,wx.TOP,-2)
        colorSizer.Add(folActTxtLbl,0,wx.LEFT,30)
        colorSizer.Add(folActTxtColourButton,0,wx.TOP,-2)
        colorSizer.Add(filActBckLbl,0)
        colorSizer.Add(filActBckColourButton,0,wx.TOP,-2)
        colorSizer.Add(folActBckLbl,0,wx.LEFT,30)
        colorSizer.Add(folActBckColourButton,0,wx.TOP,-2)
        colorSizer.Add(prefixLbl,0)
        colorSizer.Add(prefixCtrl,0,wx.TOP,-2)
        colorSizer.Add(suffixLbl,0,wx.LEFT,30)
        colorSizer.Add(suffixCtrl,0,wx.TOP,-2)
        colorSizer.Add((-1, -1))
        colorSizer.Add((-1, -1))
        colorSizer.Add(suffixLblD,0,wx.LEFT,30)
        colorSizer.Add(suffixCtrlD,0,wx.TOP,-2)
        mainSizer.Add(patternsLabel)
        mainSizer.Add(patternsCtrl,1,wx.TOP|wx.EXPAND,2)
        mainSizer.Add(hideSystem,0,wx.TOP,10)

        def OnCompBtn(evt):
            folderCtrl.textControl.ChangeValue(MY_COMPUTER)
            evt.Skip()


        def OnTitleChange(evt = None):
            val = titleCtrl.GetValue()
            flag = val != "" and\
                (val == title or val not in self.plugin.servers.iterkeys())
            panel.dialog.buttonRow.okButton.Enable(flag)
            colour = "yellow" if not flag else prefixCtrl.GetBackgroundColour()
            titleCtrl.SetBackgroundColour(colour)
            titleCtrl.Refresh()
            if evt:
                evt.Skip()
        titleCtrl.Bind(wx.EVT_TEXT, OnTitleChange)
        OnTitleChange()


        def OnTextChange(evt):
            folder = folderCtrl.GetValue()
            patterns = patternsCtrl.GetValue()
            if not patterns:
                patterns = "*.*"
            if folder:
                folderCtrl.startDirectory=folderCtrl.GetValue()
            evt.Skip()

        compBtn.Bind(wx.EVT_BUTTON, OnCompBtn)
        folderCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        patternsCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        panel.dialog.buttonRow.testButton.Show(False)

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                iFace = wx.FindWindowById(id).GetStringSelection()
            elif mode == 1:
                iFace = wx.FindWindowById(id).GetValue()
            port = wx.FindWindowById(id2).GetValue()
            bckgrnd = bckgrndColourButton.GetValue()
            border = borderColourButton.GetValue()
            filIdlTxt = filIdlTxtColourButton.GetValue()
            filIdlBck = filIdlBckColourButton.GetValue()
            filActTxt = filActTxtColourButton.GetValue()
            filActBck = filActBckColourButton.GetValue()
            folIdlTxt = folIdlTxtColourButton.GetValue()
            folIdlBck = folIdlBckColourButton.GetValue()
            folActTxt = folActTxtColourButton.GetValue()
            folActBck = folActBckColourButton.GetValue()
            prefix = prefixCtrl.GetValue()
            suffix = suffixCtrl.GetValue()
            folder = folderCtrl.GetValue()
            patterns = patternsCtrl.GetValue()
            hide = hideSystem.GetValue()
            fontsize = fontsizeCtrl.GetValue()
            brdrwdth = brdrwdthCtrl.GetValue()
            suffixD = "Folder"

            newTitle = titleCtrl.GetValue()
            flag = False
            if title and self.plugin.servers.has_key(title):
                if self.plugin.servers[title]:
                    self.plugin.StopServer(title)
                    flag = True
                del self.plugin.servers[title]
            self.plugin.AddServerName(newTitle)
            if flag:
                self.plugin.StartServer(
                    newTitle,
                    mode,
                    iFace,
                    port,
                    bckgrnd,
                    border,
                    filIdlTxt,
                    filIdlBck,
                    filActTxt,
                    filActBck,
                    folIdlTxt,
                    folIdlBck,
                    folActTxt,
                    folActBck,
                    prefix,
                    suffix,
                    strt,
                    patterns,
                    hide,
                    fontsize,
                    brdrwdth,
                    suffixD,
                )
            panel.SetResult(
            newTitle,
            mode,
            iFace,
            port,
            bckgrnd,
            border,
            filIdlTxt,
            filIdlBck,
            filActTxt,
            filActBck,
            folIdlTxt,
            folIdlBck,
            folActTxt,
            folActBck,
            prefix,
            suffix,
            folder,
            patterns,
            hide,
            fontsize,
            brdrwdth,
            suffixD,
        )
#===============================================================================

class StopServer(eg.ActionBase):

    class text:
        label = u"Server name:"


    def __call__(self, title = ""):
        self.plugin.StopServer(title)


    def Configure(self, title = ""):
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel, -1, self.text.label)
        titleCtrl = wx.Choice(
            panel,
            -1,
            choices = tuple(self.plugin.servers.iterkeys())
        )              
        titleCtrl.SetStringSelection(title)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.TOP, 2)
        sizer.Add(titleCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL, 20)
        while panel.Affirmed():
            panel.SetResult(titleCtrl.GetStringSelection())
#===============================================================================

class StopAllServers(eg.ActionBase):

    def __call__(self):
        self.plugin.StopAllServers()
#===============================================================================

class StartAllServers(eg.ActionBase):

    def __call__(self):
        self.plugin.StartAllServers()
#===============================================================================

class HTTPExplorer(eg.PluginBase):

    servers = {}
    text = Text

    def __init__(self):
        global MY_COMPUTER
        MY_COMPUTER = self.MyComputer()
        self.AddActionsFromList(ACTIONS)


    def __start__(self):
        servActions = self.GetActions(self.text.StartServer.name)
        for title in [item.args[0] for item in servActions]:
            self.AddServerName(title)
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        except pythoncom.com_error:
            pass # already initialized    


    def __stop__(self):
        for title in tuple(self.servers.iterkeys()):
            self.StopServer(title)


    def StopServer(self, title):
        if self.servers.has_key(title) and self.servers[title]:
            address ="%s:%i" % self.servers[title].server_address
            self.servers[title].stop()
            self.servers[title] = None
            eg.PrintNotice(self.text.stopMess % (title, address))    


    def StopAllServers(self):
        for title in tuple(self.servers.iterkeys()):
            self.StopServer(title)


    def StartAllServers(self):
        srvActions = self.GetActions(self.text.StartServer.name)
        for args in [itm.args for itm in srvActions if self.IsEnabled(itm)]:
            self.StartServer(*args)


    def StartServer(
        self,
        title,
        mode,
        iFace,
        port,
        bckgrnd,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        prefix,
        suffix,
        strt,
        patterns,
        hide,
        fontsize,
        brdrwdth,
        suffixD,
    ):  
        iFace = eg.ParseString(iFace)
        port = int(eg.ParseString(port))
        if not mode :            
            iFace = GetIPAddress(iFace, self.text.txtAllIfaces)
        br = Browser(prefix, suffix, patterns, hide, strt, suffixD)
        if self.servers.has_key(title) and self.servers[title]:
            self.StopServer(title)
        wit = HTTP_thread(
            self,
            br,
            iFace,
            port,
            title,
            convertColor(bckgrnd),
            convertColor(border),
            convertColor(filIdlTxt),
            convertColor(filIdlBck),
            convertColor(filActTxt),
            convertColor(filActBck),
            convertColor(folIdlTxt),
            convertColor(folIdlBck),
            convertColor(folActTxt),
            convertColor(folActBck),
            strt,               
            fontsize,
            brdrwdth,
        )
        wit.start()


    def AddServerName(self, title):
        if not self.servers.has_key(title):
            self.servers[title] = None


    def MyComputer(self):
        mc_reg = None
        try:
            mc_reg = _winreg.OpenKey(
                _winreg.HKEY_CLASSES_ROOT,
                "CLSID\\{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
            )
            value, type = _winreg.QueryValueEx(mc_reg, "LocalizedString")
            dll = split(value.split(",")[0][1:])[1]
            index = -1*int(value.split(",")[1])
            myComputer = LoadString(LoadLibrary(dll), index)
        except:
            myComputer = self.text.myComp
        if mc_reg:
            _winreg.CloseKey(mc_reg)
        return myComputer


    def GetActions(self, actName):
        def Traverse(item):
            if item.__class__ == eg.document.ActionItem:
                if item.executable.name == actName and\
                item.executable.plugin.name == self.name and item.args:
                    actions.append(item)
            elif item and item.childs:
                    for child in item.childs:
                        Traverse(child)
        actions = []
        Traverse(eg.document.__dict__['root'])
        return actions


    def IsEnabled(self, item):
        def Traverse(item):
            if not item.isEnabled:
                return True
            elif item.parent:
                result = Traverse(item.parent)
                if result:
                    return result
        result = Traverse(item)
        return False if result else True


    def Configure(self, *args):
        panel = eg.ConfigPanel()
        servActions = self.GetActions(self.text.StartServer.name)
        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
       
        serverListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES
        )
        for i, colLabel in enumerate(self.text.colLabels):
            serverListCtrl.InsertColumn(i, colLabel)

        def maxStr(lst):
            lngs = [len(item) for item in lst]
            return lst[lngs.index(max(lngs))]
        if servActions:
            serverListCtrl.InsertStringItem(0, maxStr([item.args[0] for item in servActions]))
            serverListCtrl.SetStringItem(0, 1, maxStr([item.args[2] for item in servActions]))
            serverListCtrl.SetStringItem(0, 2, "65535")
            serverListCtrl.SetStringItem(0, 3, maxStr(["%s.%s" % (item.args[14],item.args[15]) for item in servActions]))
            serverListCtrl.SetStringItem(0, 4, maxStr((self.text.running, self.text.stopped)))
        width = SYS_VSCROLL_X + serverListCtrl.GetWindowBorderSize()[0]
        for i in range(5):
            serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width += serverListCtrl.GetColumnWidth(i)
        serverListCtrl.SetMinSize((width, -1))
        mySizer.Add(serverListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, self.text.stop)
        mySizer.Add(abortButton, (1,0))
       
        abortAllButton = wx.Button(panel, -1, self.text.stopAll)
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
       
        restartButton = wx.Button(panel, -1, self.text.start)
        mySizer.Add(restartButton, (1,2), flag = wx.ALIGN_CENTER_HORIZONTAL)
       
        restartAllButton = wx.Button(panel, -1, self.text.startAll)
        mySizer.Add(restartAllButton, (1,3), flag = wx.ALIGN_CENTER_HORIZONTAL)
       
        refreshButton = wx.Button(panel, -1, self.text.refresh)
        mySizer.Add(refreshButton, (1,4), flag = wx.ALIGN_RIGHT)
       
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
       
        def PopulateList (event):
            servActions = self.GetActions(self.text.StartServer.name)
            serverListCtrl.DeleteAllItems()
            row = 0
            for args in [item.args for item in servActions if self.IsEnabled(item)]:
                serverListCtrl.InsertStringItem(row, args[0])
                serverListCtrl.SetStringItem(row, 1, args[2])
                serverListCtrl.SetStringItem(row, 2, args[3])
                serverListCtrl.SetStringItem(row,
                    3, "%s.%s" % (args[14], args[15]))
                serverListCtrl.SetStringItem(row,
                    4, (self.text.running, self.text.stopped)[int(self.servers[args[0]] is None)])
                row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = serverListCtrl.GetFirstSelected()
            while item != -1:
                name = serverListCtrl.GetItemText(item)
                self.StopServer(name)
                item = serverListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.StopAllServers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartButton(event):
            item = serverListCtrl.GetFirstSelected()
            while item != -1:
                self.StartServer(*[i.args for i in servActions][item])
                item = serverListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.StartAllServers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = serverListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            restartButton.Enable(flag)
            event.Skip()
           

        def OnSize(event):
            for i in range(5):
                serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()
        PopulateList(wx.CommandEvent())
  
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartButton.Bind(wx.EVT_BUTTON, OnRestartButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Show(False)
        panel.dialog.buttonRow.cancelButton.Show(False)

        while panel.Affirmed():
            panel.SetResult(*args)
#===============================================================================

ACTIONS = (
    (
        StartServer,
        'StartServer',
        'Start HTTP server',
        'Starts HTTP server.',
        None
    ),
    (
        StartAllServers,
        'StartAllServers',
        'Start all enabled HTTP servers',
        'Starts all enabled HTTP servers.',
        None
    ),
    (
        StopServer,
        'StopServer',
        'Stop HTTP server',
        'Stops HTTP server.',
        None
    ),
    (
        StopAllServers,
        'StopAllServers',
        'Stop all HTTP servers',
        'Stops all HTTP servers.',
        None
    ),
)
#===============================================================================
