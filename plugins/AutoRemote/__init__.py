# -*- coding: utf-8 -*-


import eg

eg.RegisterPlugin(
    name = "AutoRemote",
    author = "joaomgcd",
    version = "1.991007",
    guid = "{C18A174E-71E3-4C74-9A2B-8653CE9991E1}",
    description = (
        "Send and receive messages to and from AutoRemote on Android."
    ),
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH3AgXChElQdwgkgAAA2NJREFUOMuFkktsVGUYht9zm3Pm2pkOzPQylKGFTsWCNCrBUCuYtEhjrVQ04oY00WjcuSExISEKJizcGOKaeKlau6jBpAEheCm9oNQ2LdbpWNopQy8znUudc5n/nDnn/C5MSVnx7Z/nTd73Y/CYuzg+CZgmt564R6WaWubCsVarvfdCJJ7M9D4ZEr/kHyewJY/AWNY5YVs4UZbc0Q9/ntXdseZn6w/t7Vamf2EYALj52y282Nb6CHjt1xEce+EweoqUb8nLqeL6xlqR8kE1b/B6kcxWmWrqCT85z2wClFLcnpqpUxXVo+Syie5Xu8zRiclWT2Uw00+kd6cX1RPbYed11azJZWSDplNnr3184mtuUxBrfnpnciVzKV2QT9ngbg4OfGP8eH1kaD2TOyK5g/0JTeow/lVlLVtaVu4vO4r3k/Hw7tY7DzugHGvplrWtbOI5j8c50H/llmmYbKNByo2t09/e9dqS67PcYWcpueSSSH6OKhsLllak/NjY+A5eEusfZOQGr8UdpGAgOvgW2ynCtbSGyql+qmjZk02nz3/RwSkTN+4VatOpB20BobTHJfIM89XAlcHVvPKKz+uzwDFCVTiECiKDzAxilz4Jj9+PO0I7XfU2MLKs3Ihsr3jnrZ5LqX0v7WdcDpj86npBkInFuj0VrBcGaue+RzX3D8JtzZBnAxh19iDPR5lCdg12SYUg+CgwZM1cHQIAsGfeP/1yY/2Oy5wggJNzqJDnEdxdB1vfAFlRwaXmoZY1RAKe4bMfvN3+elfn0uXvBh/Ozf9w9XrDhma5wXBAaQOWJoPRCTiXD5peABvbA6pZ0B28c/jPeGR5cW71zde6rU0Bm0ytfF6UtTcI0eELB2gwVgdZNrGWAZTYSawbTvA8D4WQZ6Zn5/sUQuq2PhyvaiRtEboQY/JGZbyvKe6W6IJrH0P8UdDKKC2zNlyClcrn5WUNkA/s3VV+RLAzEj7j11Z6henhcznf/lIq3OIk3mqwLAvWKjNOgSOhgKezkE2rokPkOo8+v7xVwABAZuqnpsTCyntjWfGUCTYUjVR95PeIZHzir08Eh2g/1Vh7pKv96Mgm9PvdBA42N/7fweLffyB0oCO+SIOf6oY+KjL2mAPlvuNthy46WDrjYO3JmupwemvqJgwA/wFagpdq+6hoCwAAAABJRU5ErkJggg=="
    ),
)

import mmap
import datetime
import mimetypes
import wx
import os
import io
import sys
import posixpath
import base64
import time
import urllib
import urllib2
import socket
import httplib
import urlparse
from threading import Thread, Event
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urllib import unquote, unquote_plus
from os.path import getmtime
from win32com.client import Dispatch
import json
import jinja2
import cStringIO
import re
import  wx.lib.scrolledpanel as scrolled
import cgi
import _winreg
       
pluginVersionPattern = re.compile("version = \"([^\"]+)\"")
pythonSubstitutionPattern = re.compile('\{[^\}]+\}')
fileNameFromDownloadPattern = re.compile("filename=\"([^\"]+)\"")
urlPattern = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
def DownloadFile(fileUrl, folder):
    if folder is None or folder == "":
        print "Please set your AutoRemote files folder in the plugin settings."
        return
    folder = eg.ParseString(folder)
    if fileUrl.startswith("http"):
        file_name = fileUrl.split('/')[-1]
        u = urllib2.urlopen(fileUrl)
        meta = u.info()
        contentDisposition = meta.getheaders('Content-Disposition')
        if len(contentDisposition) > 0:
            fileNameFromServer = GetFileNameFromServer(contentDisposition[0])
            if fileNameFromServer is not None:
                file_name = fileNameFromServer

        if not folder.endswith("\\"):
            folder = folder + "\\"

        file_name = folder + file_name
        print "Downloading file: " + file_name + " to folder " + folder
        try:
            f = open(file_name, 'wb')
        except IOError:
            print "Can't receive AutoRemote files. You need to be running in Administrator mode."
            return

        file_size = int(meta.getheaders("Content-Length")[0])

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

        f.close()
        return file_name
    else:
        return fileUrl

def GetLocalIp(plugin):

    if plugin.localIp == "":
        success = False

        try:
            if plugin.alernateLocalIp : 
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("gmail.com",80))
                localip = s.getsockname()[0]
                #print "Alternate " + localip
                success = True
        except:
            pass

        if not success:
            localip = socket.gethostbyname(socket.gethostname())
            if not localip.startswith("127"):
                pass 
                #print "Normal " + localip
        
        #print "Current local IP detected: " + localip
    else:
        localip = plugin.localIp
    return localip

def OnBrowseFile(event, ctrl, options=None):
    if options is None:
        options = wx.OPEN
    else:
        options = wx.OPEN | options
    dialog = wx.FileDialog(None, "Choose a file", "", "", "*.*", options)
    if dialog.ShowModal() == wx.ID_OK:
        ctrl.SetValue("|".join(dialog.GetPaths()) +"|")
    dialog.Destroy()

def parentDir(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def getEventGhostExePath():
    return parentDir(parentDir(parentDir(os.path.realpath(__file__)))) + "\EventGhost.exe"

def define_action_on(filetype, registry_title, command, title=None):

    try:
        #print "Creating " + title + " action in the Windows Context Menu (command: "+command+")"
        """
        define_action_on(filetype, registry_title, command, title=None)
            filetype: either an extension type (ex. ".txt") or one of the special values ("*" or "Directory"). Note that "*" is files only--if you'd like everything to have your action, it must be defined under "*" and "Directory"
            registry_title: the title of the subkey, not important, but probably ought to be relevant. If title=None, this is the text that will show up in the context menu.
        """
        #all these opens/creates might not be the most efficient way to do it, but it was the best I could do safely, without assuming any keys were defined.
        reg = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Classes", 0, _winreg.KEY_SET_VALUE)
        k1 = _winreg.CreateKey(reg, filetype) #handily, this won't delete a key if it's already there.
        k2 = _winreg.CreateKey(k1, "shell")
        k3 = _winreg.CreateKey(k2, registry_title)
        k4 = _winreg.CreateKey(k3, "command")
        if title != None:
            _winreg.SetValueEx(k3, None, 0, _winreg.REG_SZ, title)
        _winreg.SetValueEx(k4, None, 0, _winreg.REG_SZ, command)
        _winreg.CloseKey(k3)
        _winreg.CloseKey(k2)
        _winreg.CloseKey(k1)
        _winreg.CloseKey(reg)
    except  Exception, exc:
        print "Can't add windows context menu: " + unicode(exc)

def createSendToShortcut(device):

    sendToFolder = os.environ.get('USERPROFILE') + '\\AppData\\Roaming\\Microsoft\Windows\\SendTo\\'
    path = sendToFolder + device.name.encode('utf-8') + ".lnk"
    target = getEventGhostExePath()
    wDir = parentDir(getEventGhostExePath())
    icon = getEventGhostExePath()
    arguments = "-event SentFromExplorer.To \"" + device.name +"\""

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()
    print "Created SendTo shortcut " + path


def first(list):
    try:
        first = next(iter(list))
        return first
    except:
        pass

def deviceByKey(plugin, key):
    device = first([(device) for device in plugin.devices if device.key == key])
    return device

def GetFileNameFromServer(contentDisposition):
    if len(contentDisposition) > 0:
            fileNameFromServer = fileNameFromDownloadPattern.search(contentDisposition).groups(1)
            if fileNameFromServer is not None:
                return fileNameFromServer[0]
    return None

def GetSavableDevices(devices):
    return [(i.name, i.url, i.key, i.localIp, i.tryLocalIp, i.port) for i in devices]

def SaveConfig(plugin):
    trItem = plugin.info.treeItem
    args = list(trItem.GetArguments())

    savableDevices = GetSavableDevices(plugin.devices)
    args[3] = savableDevices

    while len(args) < 8:
        args.append("")        
    args[7] = plugin.googleDriveRefreshToken

    eg.actionThread.Func(trItem.SetArguments)(args)       
    eg.document.SetIsDirty()
    eg.document.Save()
    print "Saved AutoRemote Configuration"

class ScrollPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)

class FileLoader(jinja2.BaseLoader):
    """Loads templates from the file system."""

    def get_source(self, environment, filename):
        try:
            sourceFile = open(filename, "rb")
        except IOError:
            raise jinja2.TemplateNotFound(filename)
        try:
            contents = sourceFile.read().decode("utf-8")
        finally:
            sourceFile.close()

        mtime = getmtime(filename)
        def uptodate():
            try:
                return getmtime(filename) == mtime
            except OSError:
                return False
        return contents, filename, uptodate



class MyServer(ThreadingMixIn, HTTPServer):
    address_family = getattr(socket, 'AF_INET6', None)

    def __init__(self, requestHandler, port):
        self.httpdThread = None
        self.abort = False
        for res in socket.getaddrinfo(None, port, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            #print res
            self.address_family = res[0]
            self.socket_type = res[1]
            address = res[4]
            break

        HTTPServer.__init__(self, address, requestHandler)


    def server_bind(self):
        """Called by constructor to bind the socket."""
        if socket.has_ipv6 and sys.getwindowsversion()[0] > 5:
            # make it a dual-stack socket if OS is Vista/Win7
            IPPROTO_IPV6 = 41
            self.socket.setsockopt(IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        HTTPServer.server_bind(self)


    def Start(self):
        """Starts the HTTP server thread"""
        self.httpdThread = Thread(name="WebserverThread", target=self.Run)
        self.httpdThread.start()


    def Run(self):
        try:
            # Handle one request at a time until stopped
            while not self.abort:
                self.handle_request()
        finally:
            self.httpdThread = None


    def Stop(self):
        """Stops the HTTP server thread"""
        if self.httpdThread:
            self.abort = True
            # closing the socket will awake the underlying select.select() call
            # so the handle_request() loop will notice the abort flag
            # immediately
            self.socket.close()
            self.RequestHandlerClass.repeatTimer.Stop()

    #def handle_error(self, request, client_address):
    #    eg.PrintError("HTTP Error")


class AutoRemotePayload:
    def __init__(self, message, params, commands, files=[], sender="", plugin = None, messageObj = None):
        self.armessage = message 
        self.arpar = params
        self.arcomm = commands
        self.files = files
        self.sender = sender
        self.plugin = plugin
        self.messageObj = messageObj

    def __str__(self):
        if self.armessage is not None:
            return repr(self.armessage)
        else:
            return "Empty"

    def GetDescription(self):
        result = None
        doAllLogs = False
        if self.plugin is not None:
            doAllLogs = self.plugin.systemLogs
        if doAllLogs:
            result = ""
            if 'fallback' in self.messageObj.communication_base_params:
                result = result + "\nThis is a redirected message."
            result = result + "\neg.event.payload.armessage: " + repr(self.armessage)
            if self.arpar and len(self.arpar)>0:
                result = result + "\neg.event.payload.arpar: " + repr(self.arpar)
            if len(self.arcomm)  > 0:
                result = result + "\neg.event.payload.arcomm: " + repr(self.arcomm)
            if self.files is not None and len(self.files) > 0:
                 result = result + "\neg.event.payload.files: " + str(self.files)
            if self.sender is not None:
                 result = result + "\neg.event.payload.sender: " + str(self.sender)

        return result

    def __repr__(self):
        return self.__str__()

def getCommunicationFromContent(content, egClass):
    request = content
    if "request=" in content:
        request = content.split("request=")[1].split("&")[0]

    if "response=" in content:
        request = content.split("response=")[1].split("&")[0]


    #print request
    requestJsonString = request
    #requestJsonString = unquote_plus(request)
    requestJson = json.loads(requestJsonString)
    type = requestJson.get("communication_base_params").get("type")
    print "Got communication of type: " + type
    communication = eval(type+"(egClass)")
    communication.FromJson(requestJson)
    return communication

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map['.ico'] = 'image/x-icon'
    extensions_map['.manifest'] = 'text/cache-manifest'
    # these class attributes will be set by the plugin
    authString = None
    authRealm = None
    basepath = None
    repeatTimer = None
    environment = None
    plugin = None

    def version_string(self):
        """Return the server software version string."""
        return "EventGhost/" + eg.Version.string


    def Authenticate(self):
        # only authenticate, if set
        if self.authString is None:
            return True

        # do Basic HTTP-Authentication
        authHeader = self.headers.get('authorization')
        if authHeader is not None:
            authType, authString = authHeader.split(' ', 2)
            if authType.lower() == 'basic' and authString == self.authString:
                return True

        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="%s"' % self.authRealm)
        return False


    def SendContent(self, text = "OK"):       
        self.send_response(200)
        self.send_header("Content-type", 'text/plain')
        self.send_header("Content-Length", len(text))
        self.end_headers()
        self.wfile.write(text.encode("UTF-8"))
        self.wfile.close()

    def SendFile(self, filePath):       
        self.send_response(200)
        self.send_header("Content-type", 'application/octet-stream')
        self.send_header("Content-Length", len(text))
        self.end_headers()
        self.wfile.write(text.encode("UTF-8"))
        self.wfile.close()

    def do_PUT(self):
        if self.plugin.fileFolder == "" or self.plugin.fileFolder is None:
            print "Can't download received files. You have to choose a folder in the AutoRemote plugin settings first."
        else:
            fileNameFromServer = GetFileNameFromServer(self.headers.get("Content-Disposition"))
            if fileNameFromServer is not None:
                file_name = fileNameFromServer

            folder = self.plugin.fileFolder
            if not folder.endswith("\\"):
                folder = folder + "\\"
            finalFilePath = folder + fileNameFromServer
            print "Receiving file " + fileNameFromServer
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                        })
            
            data = form.file.read()
            open(finalFilePath, "wb").write(data)
            response = ResponseFileUpload(self, finalFilePath)
            responseJson = response.ToJson()
            self.SendContent(responseJson)

    def do_POST(self):
        """Serve a POST request."""
        # First do Basic HTTP-Authentication, if set
        #print "do post"
        #print self.headers
        contentLength = int(self.headers.get('content-length'))
        acceptEncoding = self.headers.get('accept-encoding')
        content = self.rfile.read(contentLength).decode("utf-8")
        #print "Received " + str(content)
        communication = getCommunicationFromContent(content,self)
        response = communication.executeRequest(self)
        if response is None:
            response = ResponseNoAction(self)

        response.key = communication.sender;

        responseJson = response.ToJson()
        self.SendContent(responseJson)


    def do_GET(self):

        try:           
            result = self.plugin.googledrive.HandleCallback(self.path)
            if result is not None:
                self.SendContent(result)
            else:
                import urlparse
                parsed = urlparse.urlparse(self.path)
                #print parsed.path
                try:
                    parsedQueryString = urlparse.parse_qs(parsed.query)
                    message = parsedQueryString['message'][0]
                    sender = None
                    if 'sender' in parsedQueryString:
                        sender = parsedQueryString['sender'][0]
                    message = Message(self, text=message)
                    message.sender = sender
                    message.executeRequest(self)
                    self.SendContent("OK")
                except:
                    self.SendContent("AutoRemote is working.")
        except:
            eg.PrintTraceback()



    def log_message(self, format, *args):
        # suppress all messages
        pass


    def copyfile(self, src, dst):
        dst.write(src.read())


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # stolen from SimpleHTTPServer.SimpleHTTPRequestHandler
        # but changed to handle files from a defined basepath instead
        # of os.getcwd()
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(unquote(path))
        words = [word for word in path.split('/') if word]
        path = self.basepath
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

class GoogleDrive(object):
    accessToken = None
    refreshToken = None
    plugin = None
    askForDrivePermissions = None

    def __init__(self, plugin, refreshToken, askForDrivePermissions):
        self.plugin = plugin
        self.refreshToken = refreshToken
        self.askForDrivePermissions = askForDrivePermissions

    def Authorize(self):
        if self.askForDrivePermissions:
            print "using google drive"
            if self.refreshToken is None or self.refreshToken == "":
                wx.LaunchDefaultBrowser("https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&redirect_uri=http://localhost:"+str(self.plugin.port)+"&client_id=147354672683-74a5f79fdl5rnnt85mcnb0ul9k9get89.apps.googleusercontent.com&from_login=1&as=639eff90c29eec4d&pli=1&authuser=0")        
        else:
            print "not using google drive"

    def HandleCallback(self, path):
        path, dummy, remaining = path.partition("?")
        if remaining:
            if "code=" in remaining:
                    code = remaining.split("code=")[1]
                    url = "https://accounts.google.com/o/oauth2/token"
                    params = {"code" : code, "client_id": "147354672683-74a5f79fdl5rnnt85mcnb0ul9k9get89.apps.googleusercontent.com", "client_secret" : "Td25ul2qYJQv7WgmKYdshLOh", "redirect_uri" : "http://localhost:" + str(self.plugin.port), "grant_type": "authorization_code"}
                    data = urllib.urlencode(params)
                    request = urllib2.Request(url, data, {"Content-Type" : "application/x-www-form-urlencoded"})
                    f = urllib2.urlopen(request)

                    response = f.read()
                    responseJson = json.loads(response)

                    self.accessToken = responseJson.get("access_token")
                    self.SetRefreshToken(responseJson.get("refresh_token"))

                    return "Thank you. You can close this browser window now."

    def GetAccessToken(self):
        if self.accessToken is None or self.IsAccessTokenExpired():
            url = "https://accounts.google.com/o/oauth2/token"
            params = {"refresh_token" : self.refreshToken, "client_id": "147354672683-74a5f79fdl5rnnt85mcnb0ul9k9get89.apps.googleusercontent.com", "client_secret" : "Td25ul2qYJQv7WgmKYdshLOh", "grant_type": "refresh_token"}
            data = urllib.urlencode(params)
            request = urllib2.Request(url, data, {"Content-Type" : "application/x-www-form-urlencoded"})
            try:
                f = urllib2.urlopen(request)
            except IOError, e:
                self.ResetAccessToken()
                print "Couldn't get Google Drive Access Token. Asking for authorization..."
                self.Authorize()
                raise
            response = f.read()
            responseJson = json.loads(response)
            self.accessToken = responseJson.get("access_token")
            expiresIn = responseJson.get("expires_in")
            self.expirationDate = datetime.datetime.now() + datetime.timedelta(seconds = int(expiresIn))
       
        return self.accessToken

    def ResetAccessToken(self):
        print "Resetting Google Drive access token..."
        self.refreshToken = None
        self.accessToken = None

    def IsAccessTokenExpired(self):
        if self.expirationDate is None:
            return True
        else:
            return self.expirationDate < datetime.datetime.now()

    def GetAutoRemoteFolderId(self):
        url = "https://www.googleapis.com/drive/v2/files?q=mimeType%3D'application%2Fvnd.google-apps.folder'+and+trashed%3Dfalse+and+title%3D'AutoRemote'"
        request = urllib2.Request(url, headers= {"Authorization" : "Bearer " + self.GetAccessToken()})
        f = urllib2.urlopen(request)
        response = f.read()
        responseJson = json.loads(response)
        items = responseJson["items"]
        if len(items) > 0:
            return items[0]["id"]
        else:
            return self.UploadFolder("AutoRemote", "AutoRemote Folder")

    def SetRefreshToken(self, refreshToken):
        self.refreshToken = refreshToken
        self.plugin.SetGoogleDriveRefreshToken(refreshToken)

    def MakePublic(self, fileId):
        self.InsertPermission(fileId, "", "anyone", "reader")

    def InsertPermission(self, fileId, value, type, role):
        url = "https://www.googleapis.com/drive/v2/files/"+fileId+"/permissions"
        params = {"role" : role, "type": type, "value" : value}
        data = json.dumps(params)
        request = urllib2.Request(url, data, headers= {"Authorization" : "Bearer " + self.GetAccessToken(), "Content-Type": "application/json"})
        f = urllib2.urlopen(request)
        response = f.read()
    
    def UploadFileToAutoRemoteFolder(self, title, description = None, mimeType = None, filePath = None, fileContent = None):
        return self.UploadFile(title,description,mimeType, filePath, fileContent, self.GetAutoRemoteFolderId())

    def UploadFolder(self, title, description = None):
        print "Creating Folder " + title
        url = "https://www.googleapis.com/drive/v2/files"
        params = {"title": title, "description": description, "mimeType": "application/vnd.google-apps.folder" }
        contentType = "application/json"
        data = json.dumps(params)
        request = urllib2.Request(url, data, headers= {"Authorization" : "Bearer " + self.GetAccessToken(), "Content-Type": contentType})
        f = urllib2.urlopen(request)
        response = f.read()
        responseJson = json.loads(response)
        return responseJson["id"]
    
    def UploadFile(self, title, description = None, mimeType = None, filePath = None, fileContent = None, parentFolder = None):
        title = title.encode("utf-8")
        filePath = filePath.encode("utf-8")
        print "Uploading file " + str(title)
        boundary = "joaomgcd"
        contentType = None

        if mimeType is None:
            (mimeType, encoding) = mimetypes.guess_type(filePath)
            if mimeType is None:
                mimeType = ""

        if description is None:
            description = title

        url = "https://www.googleapis.com/drive/v2/files"


        params = {"title": title, "description": description, "mimeType": mimeType }
        if parentFolder is not None:
            params["parents"] = [{"id": parentFolder}]

        if filePath is not None:
            url = "https://www.googleapis.com/upload/drive/v2/files?uploadType=multipart"

            if fileContent is None:
                content_file = io.FileIO(filePath, 'r')
                fileContent = content_file.read()
                #fileContent = "blaaa"
                content_file.close()

            params = json.dumps(params)
            contentType = 'multipart/related; boundary="'+boundary+'"'
            data = "--" + boundary + "\nContent-Type: application/json; charset=UTF-8\n\n" + params + "\n\n" + "--" + boundary + "\nContent-Type: "+mimeType+"\n\n" + fileContent + "\n\n--" + boundary + "--"
          
        else:
            contentType = "application/json"
            data = json.dumps(params)

        request = urllib2.Request(url, data, headers= {"Authorization" : "Bearer " + self.GetAccessToken(), "Content-Type": contentType, "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"})
        try:
            f = urllib2.urlopen(request)
            response = f.read()
        except IOError, e:
            self.ResetAccessToken()
            raise
        responseJson = json.loads(response)
        id = responseJson["id"]
        self.MakePublic(id)
        link = responseJson["webContentLink"]
        try:
            self.plugin.TriggerEvent("FileSent", filePath)
        except:
            pass
        print "Uploaded file to Google Drive: " + link
        return link

def replacePythonCodeAndEncode(text):
    try:
        text = eg.ParseString(text)
        text = text.decode('utf-8')
    except TypeError, e:
        print "Error: {" + item + '} does not evaluate to a String. Not replacing: ' + repr(e)
    except NameError, e:
        print "Error: {" + item + '} does not evaluate to a String. Not replacing: ' + repr(e)
    return text


class Communication(object):    

    key = None
    sender = None
    communication_base_params = None

    def __init__(self, egClass, key=""):
        self.sender = egClass.plugin.dname
        self.communication_base_params = {"sender":egClass.plugin.dname, "type" : self.GetCommunicationType()}
        self.key = key

    def __str__(self):
        params = self.GetParams()
        result = ""
        for key, value in params.items():
            if value is not None and value != "":
                result = result + "\n" + key + ": " + str(value)
        return result

    def __repr__(self):
        return self.__str__()

    def GetParams(self):
        return json.dumps(self.__dict__)

    def GetParamsGCM(self):
        return {"request":self.GetParams(), "key":self.key, "sender":self.sender}
    
    
    def SendFiles(self, egClass, files, url, isLocalRequest):
        import urllib2
        filesRemotePaths = []
        try:
            for file in files:
                if file is not None and file != "":
                    if file.startswith("http"):
                        filesRemotePaths.append(file)
                    else:
                        print "Sending file: " + str(file)
                        sent = False
                        file = file.decode('utf-8')
                        with io.FileIO(file, 'r') as content_file:
                            fileContent = content_file.read()
                            originalFileName = os.path.basename(file)
                            print "original file name: " + originalFileName
                            if isLocalRequest:
                                try:
                                    opener = urllib2.build_opener(urllib2.HTTPHandler)
                                    request = urllib2.Request(url, data=fileContent)
                                    request.add_header("Content-Disposition", "attachment; filename=\"" + originalFileName + "\"")
                                    request.get_method = lambda: 'PUT'
                                    f = opener.open(request)
                                    response = f.read()
                                    communication = getCommunicationFromContent(response, egClass)
                                    communication.handleResponse(egClass)
                                    if communication.responseError == None or communication.responseError == "":
                                        print "File " + originalFileName + " sent"
                                        try:
                                            egClass.plugin.TriggerEvent("FileSent", str(file))
                                        except:
                                            pass
                                        filesRemotePaths.append(communication.path)
                                    else:
                                        egClass.plugin.TriggerEvent("FileError", str(file))
                                        print "Error sending file " + originalFileName + ": " + communication.responseError
                                except IOError, err:
                                    try:
                                        egClass.plugin.TriggerEvent("FileError", str(file))
                                    except:
                                        pass
                                    print "Couldn't send files to the device's local IP."
                            else:
                                print "Sending file via the web"
                                link = egClass.plugin.googledrive.UploadFileToAutoRemoteFolder(originalFileName, filePath= file, fileContent=fileContent)
                                filesRemotePaths.append(link)

        except IOError, err:
            print "Error sending files " + str(files) + ": " + str(err)

        if filesRemotePaths is not None and len(filesRemotePaths) > 0:
            egClass.plugin.TriggerEvent("FilesSent", filesRemotePaths)
        
        return ",".join(filesRemotePaths)
    
    def Send(self, egClass):
        Thread(target = self.SendSync, args=(egClass,)).start()

    def SendSync(self, egClass):
        device = deviceByKey(egClass.plugin, self.key)
        if device is not None:
            myLocalIp =GetLocalIp(egClass.plugin)
            isLocalRequest = device.tryLocalIp and device.localIp is not None and device.localIp != "" and myLocalIp is not None and myLocalIp != "" and device.localIp[:device.localIp.rfind(".")] == myLocalIp[:myLocalIp.rfind(".")]
            f = None
            if isLocalRequest:
                try:
                    port = device.port
                    if port is None:
                        port = "1817"
                    url = "http://" + device.localIp + ":" + port + "/"
                    result = self.DoBeforeSend(egClass, url, True)
                    if result:
                        print "Calling url " + url
                        params = self.GetParams()
                        dataToSend = str(params)
                        request = urllib2.Request(url)
                        request.add_header('Content-Type', 'application/json')
                        f = urllib2.urlopen(request,dataToSend)
                    else:
                        isLocalRequest = False
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print str(exc_tb.tb_lineno) + ": Couldn't make request via local network: " + str(e)  
                    isLocalRequest = False
            
            if not isLocalRequest:
                #url = 'http://localhost:8888/' + self.GetHttpEndpoint()
                url = 'https://autoremotejoaomgcd.appspot.com/' + self.GetHttpEndpoint()
                result = self.DoBeforeSend(egClass, url, False)
                if result:
                    print "Calling url " + url
                    params = self.GetParamsGCM()
                    str_params_data = {}
                    for k, v in params.iteritems():
                        str_params_data[k] = unicode(v).encode('utf-8')
                    params = urllib.urlencode(str_params_data)
                    try:
                        #print params
                        f = urllib2.urlopen(url,str(params))
                    except Exception as e:
                        print "Couldn't make request via the internet: " + str(e)  

            #print params
            if f is not None:
                response = f.read()
                if isLocalRequest:
                    communication = getCommunicationFromContent(response, egClass)
                    communication.handleResponse(egClass)
                    if communication.responseError == None or communication.responseError == "":
                        print "Request sent successfully"
                    else:
                        print "Error sending request: " + communication.responseError
                else:
                    print "Result from sending request: " + response
            else:
                print "Couldn't send Request"
        else:
            print "Can't send request: device doesn't exist anymore."


    def DoBeforeSend(self, egClass, url, isLocalRequest):
        pass

    def GetCommunicationType(self):
        return self.__class__.__name__

    def FromJson(self, json):
        self.__dict__ = json

    def FromDict(self, dict):
        self.__dict__.update(dict)

    def FromJsonString(self, jsonString):
        self.FromJson(json.loads(jsonString))

    def ToJson(self):
        return json.dumps(self.__dict__)


class Request(Communication):

    ttl = 0
    collapseKey = None

    def GetHttpEndpoint(self):
        return 'sendrequest'

    def DoBeforeSend(self, egClass, url, isLocalRequest):
        super(Request, self).DoBeforeSend(egClass,url, isLocalRequest)
        if self.ttl == "":
            self.ttl = "0"
        try:
            self.ttl = int(self.ttl)
        except:
            self.ttl = 0

        return True

class Response(Communication):
    responseError = None

    def GetHttpEndpoint(self):
        return 'sendresponse'

    def handleResponse(self, egClass):
        pass 

class ResponseNoAction(Response):

    def __init__(self, egClass, key=""):
        super(ResponseNoAction, self).__init__(egClass, key)




class Message(Request):
    message = None
    password = None
    target = None
    files=[]
    version = None

    def __init__(self, egClass, key="", text="", ttl="", password="", target="", files=""):
        super(Message, self).__init__(egClass, key)
        self.message = replacePythonCodeAndEncode(text)
        self.ttl = replacePythonCodeAndEncode(ttl)
        self.password = replacePythonCodeAndEncode(password)
        self.target = replacePythonCodeAndEncode(target)
        self.version = egClass.plugin.info.version
        self.files = replacePythonCodeAndEncode(files)
        if("|" in self.files):
            self.files = self.files.split("|")
        else:
            self.files = self.files.split(",")
        if len(self.files) == 1 and self.files[0] == "":
            self.files = []


    def DoBeforeSend(self, egClass, url, isLocalRequest):
        super(Message, self).DoBeforeSend(egClass,url, isLocalRequest)
        if self.files is not None and len(self.files) > 0:
            print "Sending files in message: " + str(self.files)
            files = self.SendFiles(egClass, self.files, url, isLocalRequest)
            if len(files) > 0:
                self.files = files
                return True
            else:
                return False
        else:
            self.files = ""
            return True        

    def downloadFile(self, fileUrl, folder):
        return DownloadFile(fileUrl, folder)


    def executeRequest(self, egClass):
        #print self.message
        plugin = egClass.plugin
        if plugin.fileFolder == "":
            print "Can't download received files. You have to choose a folder in the AutoRemote plugin settings first."
        else:
            if self.files is not None and len(self.files) > 0:
                print "Files: " + str(self.files)
                self.files = self.files.split(',')
                self.files = [self.downloadFile(file, plugin.fileFolder) for file in self.files]
                
        event = "Message"
        if self.message is not None:
            if not isinstance(self.message, unicode): 
                self.message = self.message.decode(eg.systemEncoding)
            #print "receiving message: " + repr(self.message)
            params, seperator, commands = self.message.partition("=:=")
            if not isinstance(commands, unicode): 
                commands = commands.decode(eg.systemEncoding)
            if not isinstance(params, unicode): 
                params = params.decode(eg.systemEncoding)
            params = params.split(" ")
            if "=:=" in commands:
                commands = commands.split("=:=")
            event = event + "." + params[0]
        else:
            params = []
            commands = []
            print "received empty message"
        payload = AutoRemotePayload(self.message, params, commands,self.files, deviceByKey(plugin,self.sender), plugin, self)
        desc = payload.GetDescription()
        if desc is not None:
            print desc
        event = plugin.TriggerEvent(event, payload)
        if self.message is not None and plugin.autoOpenUrls:
            if not plugin.dontOpenUrlsWithCommand or not "=:=" in self.message:
                urlMatch = urlPattern.search(self.message)
                if urlMatch is not None:
                    urlMatch = str(urlMatch.groups(0)[0])
                    if urlMatch:
                        print "Message has an URL. Opening: " + urlMatch
                        from os import startfile;startfile(urlMatch)
        while not event.isEnded:
            time.sleep(0.05)


class SendMessage(eg.ActionBase):
    name = "Send Message"
    description = "Send a message to your Android device"
    def __call__(self,  name="", url="", key="", text="", ttl="", password="", target="", channel="", files="", manualName =""):
        
        manualName =  replacePythonCodeAndEncode(manualName)
        if manualName != "":
            for device in self.plugin.devices:
                if device.name == manualName:
                    key = device.key
                    print "Found device with manual name: " + manualName +". Using this one instead."

        message = Message(self, key,text,ttl,password,target,files)
        message.Send(self)
        


    def GetLabel(self,  name="", url="", key="",  message="", ttl="", password="", target="", channel="", files="", manualName =""):
        return "Sending " + message + " to " + name

        
    def Configure(self,  name="", url="", key="",  message="", ttl="", password="", target="", channel="", files="", manualName =""):
        panel = eg.ConfigPanel(self)
        
        self.devicesCtrl = panel.Choice(0, [])
        panel.AddLine("Device:", self.devicesCtrl)

        for device in self.plugin.devices:
            self.devicesCtrl.Append(device.name)
    
        if name != "":
            self.devicesCtrl.SetStringSelection(name)
        else:
            self.devicesCtrl.SetSelection(0);
        
        self.deviceNameCtrl = panel.TextCtrl(manualName)
        panel.AddLine("Device Name (will override the above selected device):", self.deviceNameCtrl)

        messageCtrl = panel.TextCtrl(message)
        panel.AddLine("Message:", messageCtrl)
        
        ttlCtrl = panel.TextCtrl(ttl)
        panel.AddLine("Time To Live:", ttlCtrl)
        
        targetCtrl = panel.TextCtrl(target)
        panel.AddLine("Target:", targetCtrl)
        
        passwordCtrl = panel.TextCtrl(password)
        panel.AddLine("Password:", passwordCtrl)
        
        self.filesCtrl = panel.TextCtrl(files)
        panel.AddLine("Files (separate by comma or vertical bar (, or |)):", self.filesCtrl)

        filesButtonCtrl = panel.Button("Browse")
        panel.AddLine("Browse Files:", filesButtonCtrl)
        filesButtonCtrl.Bind(wx.EVT_BUTTON, self.OnBrowseFiles)

        
        while panel.Affirmed():
            selectedDevice = self.GetSelectedDevice()
        

            panel.SetResult(
                selectedDevice.name,
                selectedDevice.url,
                selectedDevice.key,
                messageCtrl.GetValue(),
                ttlCtrl.GetValue(),
                passwordCtrl.GetValue(),
                targetCtrl.GetValue(),
                "",
                self.filesCtrl.GetValue(),
                self.deviceNameCtrl.GetValue()               
            )
    
    
    def GetSelectedDevice(self):
        for device in self.plugin.devices:
            if device.name == self.devicesCtrl.GetStringSelection():
                return device
        return AutoRemoteDevice("","","")

    def OnBrowseFiles(self, event):
        OnBrowseFile(event, self.filesCtrl, wx.FD_MULTIPLE)

def registerDevice(plugin, deviceToRegister):
    try:
        device = deviceByKey(plugin, deviceToRegister.id)
        device.localIp = deviceToRegister.localip
        device.port = deviceToRegister.port            
        print "Device already registered. Updating properties: " + str(device)
    except:
        device = AutoRemoteDevice(deviceToRegister.name, "", deviceToRegister.id, deviceToRegister.localip, True, deviceToRegister.port)
        print "Registering new Device: " + str(device)
        plugin.devices.append(device)

class RequestSendRegistrationBase(Request):

    def registerDevice(self, plugin, deviceToRegister):
       registerDevice(plugin, deviceToRegister)

class DeviceAdditionalProperties(object):
    iconUrl = None
    type = None

    def __init__(self, iconUrl, type):
        self.iconUrl = iconUrl
        self.type = type


class RequestSendRegistration(RequestSendRegistrationBase):
    id = None
    name = None
    type = None
    localip = None
    publicip = None
    port = None
    haswifi = None
    additional = None

    def __init__(self, egClass, key="", localip="", publicip="", port="", ttl=""):
        super(RequestSendRegistration, self).__init__(egClass, key)
        self.id = egClass.plugin.dname
        self.name = egClass.plugin.dname
        self.type = "eventghost"
        self.port = port
        self.localip = localip
        self.publicip = publicip
        self.haswifi = True
        self.ttl = ttl
       # self.type = "plugin"
        #self.additional = DeviceAdditionalProperties("http://www.digitalfusionmag.com/articleimages/eventghost-logo.png", "eventghost").__dict__

    def executeRequest(self, egClass):
        plugin = egClass.plugin
        print "Received Registration from " + self.name

        self.registerDevice(plugin, self)

        SaveConfig(plugin)
        response = RequestGetRegistration(egClass).executeRequest(egClass)
        return response
        #print next(iter([(device) for device in plugin.devices if device.key == self.id]))
       

class RequestSendRegistrations(RequestSendRegistrationBase):
    devices = []

    def __init__(self, egClass, key=""):
        super(RequestSendRegistrations, self).__init__(egClass, key)

    def executeRequest(self, egClass):
        plugin = egClass.plugin
        print "Received Multiple Registrations: " + str([device['name'] for device in self.devices])
        for receivedDevice in self.devices:
            device = RequestSendRegistration(egClass) 
            device.FromDict(receivedDevice)           
            self.registerDevice(plugin, device)

        SaveConfig(plugin)


class RequestGetRegistration(Request):

    def __init__(self, egClass, key = ""):
        super(RequestGetRegistration, self).__init__(egClass, key)

    def executeRequest(self, egClass):
        plugin = egClass.plugin        
        localip = GetLocalIp(egClass.plugin)    

        port = str(plugin.port)
        publicIp = GetPublicIp(plugin)
        return ResponseGetRegistration(egClass, localip, publicIp, port)

class ResponseGetRegistration(Response):    
    
    id = None
    type = None
    name = None
    localip = None
    publicip = None
    port = None
    haswifi = True

    def __init__(self, egClass, localip="", publicip="", port=""):
        super(ResponseGetRegistration, self).__init__(egClass, egClass.plugin.dname)
        self.id = egClass.plugin.dname
        self.name = egClass.plugin.dname
        self.type = "eventghost"
        self.port = port
        self.localip = localip
        self.publicip = publicip
        self.haswifi = True

    def handleResponse(self, egClass):   
       plugin = egClass.plugin     
       registerDevice(plugin, self)

class ResponseBasic(Response):    
    
    result= None

    def __init__(self, egClass, result = ""):
        super(ResponseBasic, self).__init__(egClass, egClass.plugin.dname)
        self.result = result


class ResponseFileUpload(Response):    
    
    path = None

    def __init__(self, egClass, path=""):
        super(ResponseFileUpload, self).__init__(egClass, egClass.plugin.dname)
        self.path = path          

class RequestVersion(Request):

    def __init__(self, egClass, key = ""):
        super(RequestVersion, self).__init__(egClass, key)

    def executeRequest(self, egClass):
        plugin = egClass.plugin

        responseVersion = ResponseVersion(egClass)
        print "Replying with version " + responseVersion.version
        return responseVersion

class ResponseVersion(Response):    
    
    version = None

    def __init__(self, egClass):
        super(ResponseVersion, self).__init__(egClass, egClass.plugin.dname)
        self.version = egClass.plugin.info.version


class RequestUpdatePlugin(Message):


    def __init__(self, egClass, key = ""):
        super(RequestUpdatePlugin, self).__init__(egClass, key)

    def executeRequest(self, egClass):
        plugin = egClass.plugin
        
        print "Upgrading to version " + self.version
        self.files = self.files.split(',')
        fromFile = self.files[0]
        UpdatePlugin(fromFile)


class RequestGetLaterURLs(Request):


    def __init__(self, egClass, key = ""):
        super(RequestGetLaterURLs, self).__init__(egClass, key)

    def executeRequest(self, egClass):
        pass

class RequestReturnLaterURLs(Request):    
    
    urls=[]

    def __init__(self, egClass):
        super(RequestReturnLaterURLs, self).__init__(egClass, egClass.plugin.dname)
       
    def executeRequest(self, egClass):
        for url in self.urls:
            print "Opening " + url  + "..."
            from os import startfile;startfile(url)
            time.sleep(0.5)


def UpdatePlugin(fromFile):
    toFile = os.path.realpath(__file__).replace(".pyc", ".py")
    import shutil
    shutil.copy2(fromFile, toFile)
    print "Plugin updated. Please restart EventGhost to apply update."

def GetPublicIp(plugin):
    publicIp = plugin.publicIp
    if publicIp is None or publicIp == "":
        from urllib2 import urlopen
        try:
            publicIp = json.load(urlopen('http://httpbin.org/ip'))['origin']
            if("," in publicIp):
                publicIp = publicIp[0:publicIp.find(',')]
            print "Got public IP: " + publicIp
        except:
            pass
    return publicIp


class RegisterEventGhost(eg.ActionBase):
    name = "Register EventGhost"  
    description = "Register or refresh EventGhost info on your Android device. Recommended use is at user login and on EventGhost startup."

    def __call__(self,  name="", url="",key="", ttl=""):
        
        localip = GetLocalIp(self.plugin)
        port = str(self.plugin.port)
        publicIp = GetPublicIp(self.plugin)

        registration = RequestSendRegistration(self, key, localip, publicIp, port, ttl)
        registration.Send(self)
    

    def GetLabel(self,  name="", url="",key="", ttl=""):
        return "Registering on " + name
        
    def Configure(self,  name="", url="", key="", ttl=""):
        panel = eg.ConfigPanel(self)
        
        self.devicesCtrl = panel.Choice(0, [])
        panel.sizer.Add(panel.StaticText("Device:"), 1, wx.EXPAND)
        panel.sizer.Add(self.devicesCtrl, 1, wx.EXPAND)
        for device in self.plugin.devices:
            self.devicesCtrl.Append(device.name)
            
        self.devicesCtrl.SetStringSelection(name)
        

        ttlCtrl = panel.TextCtrl(ttl)
        panel.AddLine("Time To Live:", ttlCtrl)
        
        
        while panel.Affirmed():
            selectedDevice = self.GetSelectedDevice()
            panel.SetResult(
                selectedDevice.name,
                selectedDevice.url,
                selectedDevice.key,
                ttlCtrl.GetValue()
            )

    
    def GetSelectedDevice(self):
        for device in self.plugin.devices:
            if device.name == self.devicesCtrl.GetStringSelection():
                return device

class GetLaterUrls(eg.ActionBase):
    name = "Get Later URLs"  
    description = "Get the URLs that were stored as Send For Later on your Android device."

    def __call__(self,  name="", key=""):
        
        
        request = RequestGetLaterURLs(self, key)
        request.Send(self)
    

    def GetLabel(self,  name="", url="",key=""):
        return "Get Later URLs on " + name
        
    def Configure(self,  name="", url="", key=""):
        panel = eg.ConfigPanel(self)
        
        self.devicesCtrl = panel.Choice(0, [])
        panel.sizer.Add(panel.StaticText("Device:"), 1, wx.EXPAND)
        panel.sizer.Add(self.devicesCtrl, 1, wx.EXPAND)
        for device in self.plugin.devices:
            self.devicesCtrl.Append(device.name)
            
        self.devicesCtrl.SetStringSelection(name)        
        
        
        while panel.Affirmed():
            selectedDevice = self.GetSelectedDevice()
            panel.SetResult(
                selectedDevice.name,
                selectedDevice.key
            )

    
    def GetSelectedDevice(self):
        for device in self.plugin.devices:
            if device.name == self.devicesCtrl.GetStringSelection():
                return device

class ShowInputDialog(eg.ActionBase):
    name = "Show Input Dialog"  
    description = "Show an input dialog that allows you to create an EventGhost event that you can then use to trigger AutoRemote messages or notifications"

    def __call__(self,  dialogTitle="", dialogText="", textBoxText="", eventName="", useTextForEvent=False):
        
        
        class MyDialog():
            def __init__(self):
                dlg = wx.TextEntryDialog(None, eg.ParseString(dialogText),eg.ParseString(dialogTitle), textBoxText)
                if dlg.ShowModal() == wx.ID_OK:
                    response = dlg.GetValue()
                    trigger = "Input.OK." + eventName
                    if useTextForEvent:
                        trigger = trigger + response
                    eg.TriggerEvent(trigger, response)
                else:
                    eg.TriggerEvent("Input.CANCEL")
                dlg.Destroy()
        wx.CallAfter(MyDialog)
    

    def GetLabel(self,  dialogTitle="", dialogText="", textBoxText="", eventName="", useTextForEvent=False):
        return "Show input dialog: " + dialogTitle
        
    def Configure(self,  dialogTitle="Input some text", dialogText="Your text", textBoxText="", eventName="TextInput", useTextForEvent=False):
        panel = eg.ConfigPanel(self)
        
        dialogTitleCtrl = panel.TextCtrl(dialogTitle)
        panel.AddLine("Dialog Title:", dialogTitleCtrl)  
        
        dialogTextCtrl = panel.TextCtrl(dialogText)
        panel.AddLine("Dialog Text:", dialogTextCtrl) 
        
        textBoxTextCtrl = panel.TextCtrl(textBoxText)
        panel.AddLine("Text Box Text:", textBoxTextCtrl)  
        
        eventNameCtrl = panel.TextCtrl(eventName)
        panel.AddLine("Event Name:", eventNameCtrl)  
        
        useTextForEventCtrl = panel.CheckBox(useTextForEvent)
        panel.AddLine("Use Input Text In Event Name:", useTextForEventCtrl)  
        
        
        while panel.Affirmed():
            panel.SetResult(
                dialogTitleCtrl.GetValue(),
                dialogTextCtrl.GetValue(),
                textBoxTextCtrl.GetValue(),
                eventNameCtrl.GetValue(),
                useTextForEventCtrl.GetValue()
            )

    
    def GetSelectedDevice(self):
        for device in self.plugin.devices:
            if device.name == self.devicesCtrl.GetStringSelection():
                return device

class Notification(Request):
    title = None
    text = None
    url = None
    channel = None
    message = None
    id = None
    action = None
    icon = None
    led = None
    ledOn = None
    ledOff = None
    picture = None
    share = None
    action1 = None
    action1name = None
    action2 = None
    action2name = None
    action3 = None
    action3name = None
    sound = None
    vibration = None
    persistent = None
    statusbaricon = None
    action1icon = None
    action2icon = None
    action3icon = None
    ticker = None
    dismissontouch = None
    priority = None
    number = None
    contentInfo = None
    subtext = None
    maxprogress = None
    progress = None
    indeterminateprogress = None
    actionondismiss = None
    cancel = None

    def __init__(self, egClass, key=""):
        super(Notification, self).__init__(egClass, key)

    def __init__(self, egClass, key="", title = "",text = "",url = "",channel = "",message = "",id = "",action = "",icon = "",led = "",ledOn = "",ledOff = "",picture = "",share = "",action1 = "",action1name = "",action2 = "",action2name = "",action3 = "",action3name = "",sound = ""):
        super(Notification, self).__init__(egClass, key)
        self.title = replacePythonCodeAndEncode(title)
        self.text = replacePythonCodeAndEncode(text)
        self.url = replacePythonCodeAndEncode(url)
        self.channel = replacePythonCodeAndEncode(channel)
        self.message = replacePythonCodeAndEncode(message)
        self.id = replacePythonCodeAndEncode(id)
        self.action = replacePythonCodeAndEncode(action)
        self.icon = replacePythonCodeAndEncode(icon).replace("|","")
        self.led = replacePythonCodeAndEncode(led)
        self.ledOn = replacePythonCodeAndEncode(ledOn)
        self.ledOff = replacePythonCodeAndEncode(ledOff)
        self.picture = replacePythonCodeAndEncode(picture).replace("|","")
        self.share = replacePythonCodeAndEncode(share)
        self.action1 = replacePythonCodeAndEncode(action1)
        self.action1name = replacePythonCodeAndEncode(action1name)
        self.action2 = replacePythonCodeAndEncode(action2)
        self.action2name = replacePythonCodeAndEncode(action2name)
        self.action3 = replacePythonCodeAndEncode(action3)
        self.action3name = replacePythonCodeAndEncode(action3name)
        self.sound = replacePythonCodeAndEncode(sound)
    
    def executeRequest(self, egClass):
        message = Message(egClass)
        message.message = self.message
        message.sender = self.sender
        message.executeRequest(egClass)
    

    def DoBeforeSend(self, egClass, url, isLocalRequest):
        super(Notification, self).DoBeforeSend(egClass,url, isLocalRequest)
        result = True
        if len(self.icon) > 0:
            icon = self.SendFiles(egClass,  [self.icon], url, isLocalRequest)
            if len(icon) > 0:
                self.icon = icon
            else:
                result = False

        if len(self.picture) > 0:
            picture = self.SendFiles(egClass,  [self.picture], url, isLocalRequest)
            if len(picture) > 0:
                self.picture = picture
            else:   
                result = False
            
        return result

    def SetTitle(self, value):
        self.title = replacePythonCodeAndEncode(value)
        return self

    def SetText(self, value):
        self.text = replacePythonCodeAndEncode(value)
        return self

    def SetUrl(self, value):
        self.url = replacePythonCodeAndEncode(value)
        return self

    def SetChannel(self, value):
        self.channel = replacePythonCodeAndEncode(value)
        return self

    def SetMessage(self, value):
        self.message = replacePythonCodeAndEncode(value)
        return self

    def SetId(self, value):
        self.id = replacePythonCodeAndEncode(value)
        return self

    def SetAction(self, value):
        self.action = replacePythonCodeAndEncode(value)
        return self

    def SetIcon(self, value):
        self.icon = replacePythonCodeAndEncode(value).replace("|","")
        return self

    def SetLed_color(self, value):
        self.led = replacePythonCodeAndEncode(value)
        return self

    def SetLed_on(self, value):
        self.ledOn = replacePythonCodeAndEncode(value)
        return self

    def SetLed_off(self, value):
        self.ledOff = replacePythonCodeAndEncode(value)
        return self

    def SetPicture(self, value):
        self.picture = replacePythonCodeAndEncode(value).replace("|","")
        return self

    def SetAction_share(self, value):
        self.share = True if value != "" else False
        return self

    def SetAction_button1(self, value):
        self.action1 = replacePythonCodeAndEncode(value)
        return self

    def SetAction_label1(self, value):
        self.action1name = replacePythonCodeAndEncode(value)
        return self

    def SetAction_button2(self, value):
        self.action2 = replacePythonCodeAndEncode(value)
        return self

    def SetAction_label2(self, value):
        self.action2name = replacePythonCodeAndEncode(value)
        return self

    def SetAction_button3(self, value):
        self.action3 = replacePythonCodeAndEncode(value)
        return self

    def SetAction_label3(self, value):
        self.action3name = replacePythonCodeAndEncode(value)
        return self

    def SetSound(self, value):
        self.sound = replacePythonCodeAndEncode(value)
        return self

    def SetStatusbaricon(self, value):
        self.statusbaricon = replacePythonCodeAndEncode(value)
        return self
        
    def SetAction1icon(self, value):
        self.action1icon = replacePythonCodeAndEncode(value)
        return self
        
    def SetAction2icon(self, value):
        self.action2icon = replacePythonCodeAndEncode(value)
        return self
        
    def SetAction3icon(self, value):
        self.action3icon = replacePythonCodeAndEncode(value)
        return self
        
    def SetTicker(self, value):
        self.ticker = replacePythonCodeAndEncode(value)
        return self
        
    def SetDismissontouch(self, value):
        self.dismissontouch = replacePythonCodeAndEncode(value)
        return self
        
    def SetPriority(self, value):
        self.priority = replacePythonCodeAndEncode(value)
        return self
        
    def SetNumber(self, value):
        self.number = replacePythonCodeAndEncode(value)
        return self
        
    def SetContentInfo(self, value):
        self.contentInfo = replacePythonCodeAndEncode(value)
        return self
        
    def SetSubtext(self, value):
        self.subtext = replacePythonCodeAndEncode(value)
        return self
        
    def SetMaxprogress(self, value):
        self.maxprogress = replacePythonCodeAndEncode(value)
        return self
        
    def SetProgress(self, value):
        self.progress = replacePythonCodeAndEncode(value)
        return self
        
    def SetIndeterminateprogress(self, value):
        self.indeterminateprogress = replacePythonCodeAndEncode(value)
        return self
        
    def SetActionondismiss(self, value):
        self.actionondismiss = replacePythonCodeAndEncode(value)
        return self
        
    def SetCancel(self, value):
        self.cancel = replacePythonCodeAndEncode(value)
        return self
        
    def SetPersistent(self, value):
        self.persistent = replacePythonCodeAndEncode(value)
        return self
        

class SendNotification(eg.ActionBase):
    name = "Send Notification"  
    description = "Send a notification"

    def __call__(self, key="",  name="", title="", text="", url="", channel="", message="", id="", action="", icon="", led="", ledOn="", ledOff="", picture="", share="", action1="", action1name="", action2="", action2name="", action3="", action3name="", sound="", statusbaricon = "", action1icon = "", action2icon = "", action3icon = "", ticker = "", dismissontouch = "", priority = "", number = "", contentInfo = "", subtext = "", maxprogress = "", progress = "", indeterminateprogress = "", actionondismiss = "", cancel = "", ttl = "", persistent = "", manualName = ""):
        
        if manualName != "":
            for device in self.plugin.devices:
                if device.name == manualName:
                    key = device.key

        notification = Notification(self, key)
        notification.SetTitle(title).SetText(text).SetUrl(url).SetChannel(channel)
        notification.SetMessage(message).SetId(id).SetAction(action).SetIcon(icon).SetLed_color(led).SetLed_on(ledOn).SetLed_off(ledOff)
        notification.SetPicture(picture).SetAction_share(share).SetAction_button1(action1).SetAction_label1(action1name).SetAction_button2(action2)
        notification.SetAction_label2(action2name).SetAction_button3(action3).SetAction_label3(action3name).SetSound(sound)
        notification.SetStatusbaricon(statusbaricon).SetAction1icon(action1icon).SetAction2icon(action2icon).SetAction3icon(action3icon)
        notification.SetTicker(ticker).SetDismissontouch(dismissontouch).SetPriority(priority).SetNumber(number).SetContentInfo(contentInfo).SetSubtext(subtext)
        notification.SetMaxprogress(maxprogress).SetProgress(progress).SetIndeterminateprogress(indeterminateprogress).SetActionondismiss(actionondismiss).SetCancel(cancel).SetPersistent(persistent)
        notification.Send(self)
        #notification = Notification(self, key,  name, title, text, url, channel, message, id, action, icon, led, ledOn, ledOff, picture, share, action1, action1name, action2, action2name, action3, action3name, sound)
        #notification.Send()


    def GetLabel(self, key="",  name="",title="", text="",  url="", channel="", message="", id="", action="", icon="", led="", ledOn="", ledOff="", picture="", share="", action1="", action1name="", action2="", action2name="", action3="", action3name="", sound="", statusbaricon = "", action1icon = "", action2icon = "", action3icon = "", ticker = "", dismissontouch = "", priority = "", number = "", contentInfo = "", subtext = "", maxprogress = "", progress = "", indeterminateprogress = "", actionondismiss = "", cancel = "", ttl = "", persistent = "", manualName = ""):
        return "Sending Notification"
    
    def addLine(self, label, control):
        if(label is not None):
            self.sizer.Add(wx.StaticText(self.spanel,-1,label+":"),0,wx.TOP,3)
        self.sizer.Add(control, 0, wx.EXPAND)
        return control


    def Configure(self, key="",  name="",title="", text="",  url="",  channel="", message="", id="", action="", icon="", led="", ledOn="", ledOff="", picture="", share="", action1="", action1name="", action2="", action2name="", action3="", action3name="", sound="", statusbaricon = "", action1icon = "", action2icon = "", action3icon = "", ticker = "", dismissontouch = "", priority = "", number = "", contentInfo = "", subtext = "", maxprogress = "", progress = "", indeterminateprogress = "", actionondismiss = "", cancel = "", ttl = "", persistent = "", manualName = ""):
        panel = eg.ConfigPanel(self)

        self.spanel = ScrollPanel(panel)
        self.spanel.SetupScrolling()
        panel.sizer.Add(self.spanel, 1, wx.ALL|wx.EXPAND)
        self.sizer = wx.FlexGridSizer(cols = 2, vgap = 5, hgap = 10)
        self.sizer.AddGrowableCol(1)
        self.spanel.SetSizer(self.sizer)

        self.devicesCtrl = self.addLine("Device", wx.Choice(self.spanel, -1))
        for device in self.plugin.devices:
            self.devicesCtrl.Append(device.name)
        if name != "":            
            self.devicesCtrl.SetStringSelection(name)
        elif len(self.plugin.devices) > 0:
            self.devicesCtrl.SetSelection(0)

        self.deviceNameCtrl = self.addLine("Device Name (will override the above selected device):",wx.TextCtrl(self.spanel, -1, manualName))

        titleCtrl = self.addLine("Title",wx.TextCtrl(self.spanel, -1, title))
        textCtrl = self.addLine("Text", wx.TextCtrl(self.spanel, -1, text))
        messageCtrl = self.addLine("Automatic Action", wx.TextCtrl(self.spanel, -1, message))
        channelCtrl = self.addLine("Channel", wx.TextCtrl(self.spanel, -1, channel))
        urlCtrl = self.addLine("Url on Touch", wx.TextCtrl(self.spanel, -1, url))
        idCtrl = self.addLine("Id (same id will overlap)", wx.TextCtrl(self.spanel, -1, id))
        soundCtrl = self.addLine("Sound (1 to 10)", wx.TextCtrl(self.spanel, -1, sound))
        actionCtrl = self.addLine("Action on Touch", wx.TextCtrl(self.spanel, -1, action))
        self.iconCtrl = self.addLine("Icon Url or local path", wx.TextCtrl(self.spanel, -1, icon))
        iconFileButtonCtrl = self.addLine("Browse Icon File", wx.Button(self.spanel, -1, "Browse"))
        iconFileButtonCtrl.Bind(wx.EVT_BUTTON, self.OnBrowseFileIcon)
        ledCtrl = self.addLine("Led Color", wx.Choice(self.spanel, -1, (-1, -1), (-1, -1),  ['red', 'blue', 'green', 'black', 'white', 'gray', 'cyan', 'magenta', 'yellow', 'lightgray', 'darkgray']))
        ledOnCtrl = self.addLine("Led On Time", wx.TextCtrl(self.spanel, -1, ledOn))
        ledOffCtrl = self.addLine("Led Off Time", wx.TextCtrl(self.spanel, -1, ledOff))
        self.pictureCtrl = self.addLine("Picture Url or local path", wx.TextCtrl(self.spanel, -1, picture))
        pictureFileButtonCtrl = self.addLine("Browse Picture File", wx.Button(self.spanel, -1, "Browse"))
        pictureFileButtonCtrl.Bind(wx.EVT_BUTTON, self.OnBrowseFilePicture)
        shareCtrl = self.addLine("Show Share", wx.TextCtrl(self.spanel, -1, share))
        action1Ctrl = self.addLine("Action 1", wx.TextCtrl(self.spanel, -1, action1))
        action1nameCtrl = self.addLine("Action 1 Label", wx.TextCtrl(self.spanel, -1, action1name))
        action2Ctrl = self.addLine("Action 2", wx.TextCtrl(self.spanel, -1, action2))
        action2nameCtrl = self.addLine("Action 2 Label", wx.TextCtrl(self.spanel, -1, action2name))
        action3Ctrl = self.addLine("Action 3", wx.TextCtrl(self.spanel, -1, action3))
        action3nameCtrl = self.addLine("Action 3 Label", wx.TextCtrl(self.spanel, -1, action3name))
        statusbariconCtrl = self.addLine("Status Bar Icon", wx.TextCtrl(self.spanel, -1, statusbaricon))
        action1iconCtrl = self.addLine("Action 1 Icon", wx.TextCtrl(self.spanel, -1, action1icon))
        action2iconCtrl = self.addLine("Action 2 Icon", wx.TextCtrl(self.spanel, -1, action2icon))
        action3iconCtrl = self.addLine("Action 3 Icon", wx.TextCtrl(self.spanel, -1, action3icon))
        tickerCtrl = self.addLine("Ticker", wx.TextCtrl(self.spanel, -1, ticker))
        dismissontouchCtrl = self.addLine("Dismiss On Touch", wx.TextCtrl(self.spanel, -1, dismissontouch))
        priorityCtrl = self.addLine("Priority", wx.TextCtrl(self.spanel, -1, priority))
        numberCtrl = self.addLine("Number", wx.TextCtrl(self.spanel, -1, number))
        contentInfoCtrl = self.addLine("Content Info", wx.TextCtrl(self.spanel, -1, contentInfo))
        subtextCtrl = self.addLine("Sub Text", wx.TextCtrl(self.spanel, -1, subtext))
        maxprogressCtrl = self.addLine("Max Progress", wx.TextCtrl(self.spanel, -1, maxprogress))
        progressCtrl = self.addLine("Progress", wx.TextCtrl(self.spanel, -1, progress))
        indeterminateprogressCtrl = self.addLine("Indeterminate Progress", wx.TextCtrl(self.spanel, -1, indeterminateprogress))
        actionondismissCtrl = self.addLine("Action on Dismiss", wx.TextCtrl(self.spanel, -1, actionondismiss))
        cancelCtrl = self.addLine("Cancel", wx.TextCtrl(self.spanel, -1, cancel))
        persistentCtrl = self.addLine("Persistent", wx.TextCtrl(self.spanel, -1, persistent))
        ttlCtrl = self.addLine("Time To Live", wx.TextCtrl(self.spanel, -1, ttl))

        
        while panel.Affirmed():
            selectedDevice = self.GetSelectedDevice()
            panel.SetResult(
                selectedDevice.key,
                selectedDevice.name,
                titleCtrl.GetValue(),
                textCtrl.GetValue(),
                urlCtrl.GetValue(),
                channelCtrl.GetValue(),
                messageCtrl.GetValue(),
                idCtrl.GetValue(),
                actionCtrl.GetValue(),
                self.iconCtrl.GetValue(),
                ledCtrl.GetStringSelection(),
                ledOnCtrl.GetValue(),
                ledOffCtrl.GetValue(),
                self.pictureCtrl.GetValue(),
                shareCtrl.GetValue(),
                action1Ctrl.GetValue(),
                action1nameCtrl.GetValue(),
                action2Ctrl.GetValue(),
                action2nameCtrl.GetValue(),
                action3Ctrl.GetValue(),
                action3nameCtrl.GetValue(), 
                soundCtrl.GetValue(),
                statusbariconCtrl.GetValue(),
                action1iconCtrl.GetValue(),
                action2iconCtrl.GetValue(),
                action3iconCtrl.GetValue(),
                tickerCtrl.GetValue(),
                dismissontouchCtrl.GetValue(),
                priorityCtrl.GetValue(),
                numberCtrl.GetValue(),
                contentInfoCtrl.GetValue(),
                subtextCtrl.GetValue(),
                maxprogressCtrl.GetValue(),
                progressCtrl.GetValue(),
                indeterminateprogressCtrl.GetValue(),
                actionondismissCtrl.GetValue(),
                cancelCtrl.GetValue(),
                ttlCtrl.GetValue(),
                persistentCtrl.GetValue(),
                self.deviceNameCtrl.GetValue()
            )

        
    def GetSelectedDevice(self):
        for device in self.plugin.devices:
            if device.name == self.devicesCtrl.GetStringSelection():
                return device
        return AutoRemoteDevice("","","")

    def OnBrowseFileIcon(self, event):
        OnBrowseFile(event, self.iconCtrl)

    def OnBrowseFilePicture(self, event):
        OnBrowseFile(event, self.pictureCtrl)


class AutoRemote(eg.PluginBase):

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        authBox = "Basic Authentication"
        authRealm = "Realm:"
        authUsername = "Username:"
        authPassword = "Password:"


    def __init__(self):
        self.AddEvents()
        self.AddAction(SendMessage)
        self.AddAction(RegisterEventGhost)
        self.AddAction(SendNotification)
        self.AddAction(GetLaterUrls)
        self.AddAction(ShowInputDialog)       
        self.running = False


    def __start__(
        self,
        prefix=None,
        port=1818,
        dname="EventGhost",
        devices=[],
        publicIp="",
        fileFolder="",
        autoOpenUrls=True,
        googleDriveRefreshToken="",
        alernateLocalIp=False,
        systemLogs=True,
        windowContextMenuText="Send to EventGhost",
        dontOpenUrlsWithCommand=True,
        localIp="",
        askForDrivePermissions = True,
        authUsername="",
        authPassword=""
    ):
        self.info.eventPrefix = prefix
        if authUsername or authPassword:
            authString = base64.b64encode(authUsername + ':' + authPassword)
        else:
            authString = None
        class RequestHandler(MyHTTPRequestHandler):
            plugin = self
            environment = jinja2.Environment(loader=FileLoader())
            environment.globals = eg.globals.__dict__
            repeatTimer = eg.ResettableTimer(self.EndLastEvent)
        RequestHandler.basepath = None
        RequestHandler.authRealm = ""
        RequestHandler.authString = authString

        if len(devices) > 0:
            if(isinstance(devices[0], AutoRemoteDevice)):          
                self.devices = devices
                wx.CallAfter(self.SaveConfig, devices)
            else:
                self.devices = [AutoRemoteDevice(*i) for i in devices]
        else:
            self.devices = []

        self.port = port
        self.publicIp = publicIp
        self.localIp = localIp
        self.dname = dname
        self.fileFolder = fileFolder
        self.autoOpenUrls = autoOpenUrls
        self.dontOpenUrlsWithCommand = dontOpenUrlsWithCommand
        self.alernateLocalIp = alernateLocalIp
        self.systemLogs = systemLogs
        self.server = MyServer(RequestHandler, port)
        self.server.Start()
        self.googleDriveRefreshToken = googleDriveRefreshToken
        #for device in self.devices:
            #createSendToShortcut(device)
        define_action_on("*", "SendToEventGhost", getEventGhostExePath() + " -event SentFromExplorer.File \"%1\"", title=windowContextMenuText)
        self.googledrive = GoogleDrive(self, googleDriveRefreshToken,askForDrivePermissions)
        self.RemoteUpdgradePluginAsync()
        #print "id: " + str(self.googledrive.GetAutoRemoteFolderId())

        #link = self.googledrive.UploadFileToAutoRemoteFolder("test", filePath = u"C:\\Users\\João\\Pictures\\Enxara com as primas\\IMG_8623.JPG")
       
        self.googledrive.Authorize()
    def RemoteUpdgradePluginAsync(self, event = None):
        Thread(target = self.RemoteUpdgradePlugin).start()
        
    def RemoteUpdgradePlugin(self):
        try:
            versionFromWeb = urllib2.urlopen("https://www.dropbox.com/s/wjl64p05ykr9ic1/egversion?dl=1").read()
            remoteVersion = pluginVersionPattern.search(versionFromWeb).groups(1)[0]
            if float(remoteVersion) > float(self.info.version):
                print "AutoRemote plugin Remote version " + remoteVersion + " > Local Version " + self.info.version  + ". Upgrading..."
                filePath = DownloadFile("https://www.dropbox.com/s/3o0f18xzwgk0ywb/__init__.py?dl=1", self.fileFolder)
                if filePath is not None:                    
                    eg.TriggerEvent("AutoRemote.Updated");
                    print "Downloaded remote version to " + filePath
                    UpdatePlugin(filePath)
                else:
                    print "Can't update plugin from the web."
            else:
                print "AutoRemote plugin is up to date"
        except:
            print "Error checking for AutoRemote plugin updates"

    def SetGoogleDriveRefreshToken(self, refreshToken):
        self.googleDriveRefreshToken = refreshToken
        SaveConfig(self);

    def SaveConfig(self, devices):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        args[3] = [(i.name, i.url, i.key) for i in self.devices]
        eg.actionThread.Func(trItem.SetArguments)(args)       
        eg.document.SetIsDirty()
        eg.document.Save()
        print "Sucessfully converted to non-bugged-save version"

    def __stop__(self):
        self.server.Stop()

    def addLine(self, label, control, width=400):
        if(label is not None):
            self.boxsizer.Add(wx.StaticText(self.panel,-1,label+":"),0,wx.TOP,3)
        try:
            control.Size.SetWidth(width)
        except AttributeError:
            print "no Width: " + str(label)
        self.boxsizer.Add(control, 0)
        return control

    def addGroup(self, label):
        sb = wx.StaticBox(self.spanel, label=label)
        self.boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.panel.sizer.Add(self.boxsizer)

    #def GetLabel(self,
    #    prefix="HTTP",
    #    port=1818,
    #    name="",
    #    devices="[]",
    #    publicIp="",
    #    authUsername="",
    #    authPassword=""):
    #    return name

    def Configure(
        self,
        prefix="HTTP",
        port=1818,
        name="EventGhost",
        devices=[],
        publicIp="",
        fileFolder="",
        autoOpenUrls=True,
        googleDriveRefreshToken="",
        alernateLocalIp=False,
        systemLogs=True,
        windowContextMenuText="Send to EventGhost",
        dontOpenUrlsWithCommand = True,
        localIp="",
        askForDrivePermissions = True,
        authUsername="",
        authPassword=""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        
        self.panel = panel
        self.spanel = ScrollPanel(panel)
        self.spanel.SetupScrolling()
        panel.sizer.Add(self.spanel, 1, wx.ALL|wx.EXPAND)

        self.addGroup("EventGhost Properties")

        self.updateCtrl = self.addLine(None,panel.Button("Check for updates (current version: " + eg.plugins.AutoRemote.plugin.info.version + ")"))
        self.updateCtrl.Bind(wx.EVT_BUTTON, self.RemoteUpdgradePluginAsync)

        portCtrl = self.addLine("TCP/IP port", panel.SpinIntCtrl(port, min=1, max=65535))
        nameCtrl = self.addLine("Name to appear on your device",  panel.TextCtrl(name))
        publicIpCtrl = self.addLine("Your Public IP or Host Name (like a dyndns host name). Leave blank to get it automatically", panel.TextCtrl(publicIp))
        localIpCtrl = self.addLine("Your Local IP or Host Name. Leave blank to get it automatically", panel.TextCtrl(localIp))
        self.folderNameCtrl = self.addLine("Folder to store files in", panel.TextCtrl(fileFolder))
        folderButtonCtrl = self.addLine(None, panel.Button("Browse"))
        folderButtonCtrl.Bind(wx.EVT_BUTTON, self.OnBrowseFolder)
        self.autoOpenUrlsCtrl = self.addLine(None, panel.CheckBox(autoOpenUrls,label="Automatically Open Web Pages"))
        self.dontOpenUrlsWithCommandCtrl = self.addLine(None, panel.CheckBox(dontOpenUrlsWithCommand,label="Don't open URLs if there is a command (=:=) present"))
        self.alternateLocalIpCtrl = self.addLine(None, panel.CheckBox(alernateLocalIp,label="Use alternative method of getting local IP. (use only if your local IP isn't correct or if you have a large delay when sending messages)"))
        self.systemLogsCtrl = self.addLine(None, panel.CheckBox(systemLogs,label="Show all logs (disable if you want less AutoRemote logs to show up; important ones will still show.)"))
        self.windowsContextMenuCtrl = self.addLine("Windows Context Menu Text", panel.TextCtrl(windowContextMenuText))
        self.autoAskForDrivePermissionsCtrl = self.addLine(None, panel.CheckBox(askForDrivePermissions,label="Use Google Drive so you can easily transfer files to your Android Device"))
        

        self.addGroup("Add Device")

        self.deviceCtrl = self.addLine("Device Name", panel.TextCtrl())
        self.deviceCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnNameChanged)  

        self.urlCtrl = self.addLine("Device Personal URL (e.g. goo.gl/XxXxX)", panel.TextCtrl())
        self.urlCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnUrlChanged) 
            
        self.keyCtrl = self.addLine("Device Key (Try to fill your personal URL first and this field should be automatically detected)", panel.TextCtrl())
        #self.keyCtrl.Disable()

        self.addDeviceCtrl = self.addLine(None,panel.Button("Add"))
        self.addDeviceCtrl.Bind(wx.EVT_BUTTON, self.OnAddDevice)
        self.addDeviceCtrl.Disable()
        
        if len(devices) > 0:
                if(isinstance(devices[0], AutoRemoteDevice)):            
                    self.cdevices = devices
                else:
                    self.cdevices = [AutoRemoteDevice(*i) for i in devices]
        else:
            self.cdevices = []

        self.addGroup("Existing Devices")
        self.devicesCtrl = self.addLine(None, panel.Choice(0, []))
        for device in self.cdevices:
            self.devicesCtrl.Append(device.name)
        self.devicesCtrl.Bind(wx.EVT_CHOICE, self.OnSelectedDeviceChanged)

        self.removeDeviceCtrl = self.addLine(None, panel.Button("Remove"))
        self.removeDeviceCtrl.Bind(wx.EVT_BUTTON, self.OnRemoveDevice)
        self.removeDeviceCtrl.Disable()

        self.deviceLocalIp = self.addLine("Local IP", panel.TextCtrl())
        self.deviceLocalIp.Bind(wx.EVT_TEXT, self.OnDeviceLocalIpChanged)
        self.deviceLocalIp.Disable()

        self.tryLocalIp = self.addLine(None, panel.CheckBox(label="Try to contact via local IP if available"))
        self.tryLocalIp.Disable()
        self.tryLocalIp.Bind(wx.EVT_CHECKBOX, self.OnTryLocalIpChecked)

        while panel.Affirmed():
            panel.SetResult(
                "AutoRemote",
                portCtrl.GetValue(),
                nameCtrl.GetValue(),
                GetSavableDevices(self.cdevices),
                publicIpCtrl.GetValue(),
                self.folderNameCtrl.GetValue(),
                self.autoOpenUrlsCtrl.GetValue(),
                googleDriveRefreshToken,
                self.alternateLocalIpCtrl.GetValue(),
                self.systemLogsCtrl.GetValue(),
                self.windowsContextMenuCtrl.GetValue(),
                self.dontOpenUrlsWithCommandCtrl.GetValue(),
                localIpCtrl.GetValue(),
                self.autoAskForDrivePermissionsCtrl.GetValue()
            )
            
    def OnAddDevice(self, event):
        self.GetDeviceFromInput()
        self.cdevices.append(self.deviceToAdd)
        self.devicesCtrl.Append ( self.deviceToAdd.name )
        if self.devicesCtrl.GetValue() == -1:
            self.devicesCtrl.SetSelection ( 0 )
        self.addDeviceCtrl.Disable()

    def OnBrowseFolder(self, event):        
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.folderNameCtrl.SetValue(dialog.GetPath())
        dialog.Destroy()

    def OnRemoveDevice(self, event):
        index = self.devicesCtrl.GetValue()
        if index != -1:
            del self.cdevices[index]
            self.devicesCtrl.Delete(index)
            self.removeDeviceCtrl.Disable()
            self.tryLocalIp.Disable()
            self.tryLocalIp.SetValue(False)
            self.deviceLocalIp.Disable()
            self.deviceLocalIp.SetValue("")
        
    def OnUrlChanged(self, event):
        self.UpdateButton()
        
    def OnNameChanged(self, event):
        self.UpdateButton()
            
    def UpdateButton(self):
        self.GetDeviceFromInput()
        self.keyCtrl.SetValue(self.deviceToAdd.key)
        found = False        
        if self.deviceToAdd.key != "Invalid URL":
            for device in self.cdevices:
                if device.name == self.deviceCtrl.GetValue():
                    found = True
                    break
        
        if found:
            self.addDeviceCtrl.Disable()
            self.addDeviceCtrl.SetLabel("Name already exists")
        else:
            self.addDeviceCtrl.SetLabel("Add")
            self.addDeviceCtrl.Enable()
        
    def GetDeviceFromInput(self):
        addedDeviceName = self.deviceCtrl.GetValue()
        if self.keyCtrl.GetValue() == "" or self.keyCtrl.GetValue() == "Invalid URL":
            self.deviceToAdd =  AutoRemoteDevice(addedDeviceName, self.urlCtrl.GetValue())
        else:
            self.deviceToAdd = AutoRemoteDevice(addedDeviceName, self.urlCtrl.GetValue(), self.keyCtrl.GetValue())
        
    def OnSelectedDeviceChanged(self, event):
        #print self.devicesCtrl.GetValue()
        self.removeDeviceCtrl.Enable()
        self.tryLocalIp.Enable()
        self.deviceLocalIp.Enable()
        device = self.GetDeviceBeingManaged()

        if device is not None:
            #print "OnSelectedDeviceChanged: " + str(device)
            self.tryLocalIp.SetValue(device.tryLocalIp)
            if device.localIp is not None:
                self.deviceLocalIp.SetValue(device.localIp)
            else:
                self.deviceLocalIp.SetValue("")

    def OnTryLocalIpChecked(self, event):
        device = self.GetDeviceBeingManaged()
        if device is not None:
            device.tryLocalIp = event.IsChecked()
        #print "OnTryLocalIpChecked: " + str(device)

    def OnDeviceLocalIpChanged(self, event):
        localIp = self.deviceLocalIp.GetValue()
        device = self.GetDeviceBeingManaged()
        if device is not None:
            device.localIp = localIp

    def GetDeviceBeingManaged(self):
        index = self.devicesCtrl.GetValue()
        try:
            return self.cdevices[index]
        except:
            return None

        
class AutoRemoteDevice:
    
    name = None
    url = None
    key = None
    localIp = None
    port = None
    tryLocalIp = False

    def __init__(self, name, url, key = None, localIp = None, tryLocalIp = False, port = None):
        self.name = name
        self.url = url
        self.key = self.GetKey(self.url) if key is None else key
        self.localIp = localIp
        self.tryLocalIp = tryLocalIp
        self.port = port
    
    def __str__(self): 
        result = "\n\tkey: " + repr(self.key)
        result += "\n\tname: " + repr(self.name)
        result += "\n\turl: " + repr(self.url)
        result += "\n\tlocalIp: " + repr(self.localIp)
        result += "\n\tport: " + repr(self.port)
        result += "\n\ttryLocalIp: " + repr(self.tryLocalIp)

        return result

    def __repr__(self):
        return self.__str__()

    def GetKey(self, shortUrl):
        if not shortUrl == '':
            try:
                if not "http" in shortUrl:
                    shortUrl = "https://" + shortUrl
                result = urllib.urlopen('https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCW9fcDGiUhrqG8HKfNQJ9GuA8bxAZvUIQ&shortUrl={0}'.format(shortUrl)).read()
                resultObj = json.loads(result)
                url = resultObj["longUrl"]
                parsed = urlparse.urlparse(url)
                key = urlparse.parse_qs(parsed.query)['key'][0]
                print key
                return key
            except KeyError:
                return "Invalid URL"
        else:
            return "Invalid URL"

