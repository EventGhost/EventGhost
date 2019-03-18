# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg


eg.RegisterPlugin(
    name=u'Google Drive',
    author=u'K',
    version=u'0.2.2b',
    description=u'Automate Google Drive tasks',
    kind=u'other',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid=u'{C4B7D971-BD1A-4038-8F71-A1DD20CAF71C}',
)


import wx # NOQA
import os # NOQA
import base64 # NOQA
import port_forward # NOQA
import sys # NOQA
import threading # NOQA
import subprocess # NOQA
import tempfile # NOQA

lib_path = os.path.join(os.path.split(__file__)[0], 'libs')

if lib_path not in sys.path:
    sys.path.append(lib_path)


class AuthenticationError(Exception):
    pass


from oauth2client.client import AccessTokenRefreshError # NOQA


class Config(eg.PersistentData):
    credentials = None


class Text:

    class TrashFile:
        name = u'Trash File'
        description = 'Trash File'

    class DeleteFile:
        name = u'Delete File'
        description = 'Delete File'

    class UploadFile:
        name = u'Upload File'
        description = 'Upload File'

    class DownloadFile:
        name = u'Download File'
        description = 'Download File'

    class OpenFile:
        name = u'Open File'
        description = 'Open File'

    class ListFiles:
        name = u'List Files'
        description = 'List Files'


class GoogleDrive(eg.PluginBase):
    text = Text

    def __init__(self):
        self._gauth = None
        self.temp_files = []
        if 'REQUESTS_CA_BUNDLE' not in os.environ:
            pth = sys.executable
            pth = os.path.split(pth)[0]
            pth = os.path.join(pth, 'lib27', 'site-packages')
            sys.path += [pth]
            os.environ['REQUESTS_CA_BUNDLE'] = (
                os.path.join(pth, 'requests', 'cacert.pem')
            )

        self.google_drive_path = tempfile.gettempdir()

        self.client_file = os.path.join(
            self.google_drive_path,
            'settings.yaml',
        )

        self.client_credentials = os.path.join(
            self.google_drive_path,
            'credentials.json'
        )

        self._drive = None
        self.AddAction(TrashFile)
        self.AddAction(DeleteFile)
        self.AddAction(UploadFile)
        self.AddAction(DownloadFile)
        self.AddAction(OpenFile)
        self.AddAction(ListFiles)

    def __authenticate(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()
            os.chdir(self.google_drive_path)

        from pydrive.auth import (
            GoogleAuth,
            ClientRedirectServer,
            ClientRedirectHandler,
            webbrowser,
            CheckAuth,
            AuthenticationError,
            RefreshError
        )
        from pydrive.drive import GoogleDrive as _GoogleDrive


        class GAuth(GoogleAuth):

            @CheckAuth
            def LocalWebserverAuth(
                self,
                callback_host='localhost',
                callback_port=None
            ):

                if port_forward.add_port_mapping(callback_port) is False:
                    eg.PrintNotice(
                        'GoogleDrive: Unable to set port forwarding on '
                        'router.\n'
                        'Please forward port 56874 to the IP address of '
                        'this computer.\n'
                        'If you have done this then you can ignore this '
                        'message.'
                    )
                httpd = ClientRedirectServer(
                    (callback_host, callback_port),
                    ClientRedirectHandler
                )
                oauth_callback = 'http://%s:%s/' % (
                callback_host, callback_port)
                gauth.flow.redirect_uri = oauth_callback
                authorize_url = gauth.GetAuthUrl()
                webbrowser.open(authorize_url, new=1, autoraise=True)
                httpd.handle_request()
                if 'error' in httpd.query_params:
                    print('Authentication request was rejected')
                if 'code' not in httpd.query_params:
                    print(
                        'Failed to find "code" in the query '
                        'parameters of the redirect.'
                    )
                    return False

                return httpd.query_params['code']


        with open(self.client_file, 'w') as f:
            f.write(base64.decodestring(CLIENT))

        self._gauth = gauth = GAuth()

        def restart():
            Config.credentials = None
            eg.config.Save()
            self._drive = None
            self._gauth = None
            try:
                os.remove(self.client_credentials)
            except WindowsError:
                pass
            try:
                os.remove(self.client_file)
            except WindowsError:
                pass
            self.__authenticate(cwd)

        if Config.credentials is None:
            try:
                gauth.LocalWebserverAuth(callback_port=56874)
            except RefreshError:
                for f in os.listdir(self.google_drive_path):
                    if f.startswith('client_secret') and f.endswith('json'):
                        try:
                            os.remove(os.path.join(self.google_drive_path, f))
                        except WindowsError:
                            pass
                    restart()
                    return

            gauth.GetFlow()
        else:
            with open(self.client_credentials, 'w') as f:
                f.write(base64.decodestring(Config.credentials))

            gauth.LoadCredentialsFile(self.client_credentials)
        try:
            gauth.Authorize()
        except AuthenticationError:
            try:
                gauth.Refresh()
            except RefreshError:
                restart()
                return

            else:
                gauth.Authorize()

        self.__save_credentials()

        self._drive = _GoogleDrive(gauth)
        os.chdir(cwd)
        _ = self.files

    def __start__(self):
        t = threading.Thread(target=self.__authenticate)
        t.daemon = True
        t.start()

    def __save_credentials(self):
        self._gauth.SaveCredentialsFile(self.client_credentials)

        with open(self.client_credentials, 'r') as f:
            Config.credentials = base64.encodestring(f.read())

        eg.config.Save()

    @property
    def drive(self):
        if self._drive is None:
            self.__authenticate()

        if self._drive is None:
            raise AuthenticationError
        return self._drive

    @property
    def files(self):
        try:
            return self.drive.ListFile(
                {'q': "'root' in parents and trashed=false"}
            ).GetList()
        except AccessTokenRefreshError:
            try:
                if self._gauth.access_token_expired:
                    self._gauth.Refresh()
            except AccessTokenRefreshError:
                self.__stop__()
                Config.credentials = None
                eg.config.Save()
                self.__authenticate()

            return self.drive.ListFile(
                {'q': "'root' in parents and trashed=false"}
            ).GetList()

    def __stop__(self):
        cwd = os.getcwd()
        os.chdir(self.google_drive_path)
        self.__save_credentials()
        os.chdir(cwd)

        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except WindowsError:
                pass

        del self.temp_files[:]

        self._drive = None
        self._gauth = None
        os.remove(self.client_credentials)
        os.remove(self.client_file)


class TrashFile(eg.ActionBase):

    def __call__(self, file_name):
        for f in self.plugin.files:
            if file_name == f['title']:
                f.Trash()

    def Configure(self, file_name=''):
        panel = eg.ConfigPanel()
        choices = sorted(f['title'] for f in self.plugin.files)

        file_st = panel.StaticText('File:')
        file_ctrl = wx.ComboBox(panel, -1, choices=choices)

        if file_name in choices:
            file_ctrl.SetStringSelection(file_name)
        else:
            file_ctrl.SetSelection(0)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)

        file_sizer.Add(file_st, 0, wx.ALL, 5)
        file_sizer.Add(file_ctrl, 0, wx.ALL, 5)
        panel.sizer.Add(file_sizer)

        while panel.Affirmed():
            panel.SetResult(file_ctrl.GetStringSelection())


class DeleteFile(eg.ActionBase):

    def __call__(self, file_name):
        for f in self.plugin.files:
            if file_name == f['title']:
                f.Delete()

    def Configure(self, file_name=''):
        panel = eg.ConfigPanel()
        choices = sorted(f['title'] for f in self.plugin.files)

        file_st = panel.StaticText('File:')
        file_ctrl = wx.ComboBox(panel, -1, choices=choices)

        if file_name in choices:
            file_ctrl.SetStringSelection(file_name)
        else:
            file_ctrl.SetSelection(0)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)

        file_sizer.Add(file_st, 0, wx.ALL, 5)
        file_sizer.Add(file_ctrl, 0, wx.ALL, 5)
        panel.sizer.Add(file_sizer)

        while panel.Affirmed():
            panel.SetResult(file_ctrl.GetStringSelection())


class UploadFile(eg.ActionBase):

    def __call__(self, file_path, file_name):

        for f in self.plugin.files:
            if file_name == f['title']:
                break
        else:
            f = self.plugin.drive.CreateFile(
                dict(
                    title=file_name,
                    uploadType='media',
                    originalFilename=file_name
                )
            )

        def do(f_name):
            f.SetContentFile(f_name)
            f.Upload()
            eg.Print(
                'Google Drive: Finished uploading file %s' %
                f_name
            )

        t = threading.Thread(
            target=do,
            args=(os.path.join(file_path, file_name),)
        )
        t.daemon = True

        eg.Print(
            'Google Drive: Uploading file %s' %
            os.path.join(file_path, file_name)
        )
        t.start()

    def Configure(self, file_path='', file_name=''):
        if not file_path:
            file_path = "."

        panel = eg.ConfigPanel()
        file_ctrl = eg.FileBrowseButton(panel, startDirectory=file_path)

        if file_name:
            file_ctrl.SetValue(os.path.join(file_path, file_name))

        panel.sizer.Add(file_ctrl, 0, wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult(*os.path.split(file_ctrl.GetValue()))


class DownloadFile(eg.ActionBase):

    def __call__(self, dest_file, src_file):
        for f in self.plugin.files:
            if f['title'] == src_file:
                def do(f_name):
                    f.GetContentFile(
                        f_name,
                        f['mimeType']
                    )
                    eg.Print(
                        'Google Drive: Finished downloading file %s' % f_name
                    )

                t = threading.Thread(
                    target=do,
                    args=(os.path.join(dest_file, src_file),)
                )
                t.daemon = True

                eg.Print(
                    'Google Drive: Downloading file %s to %s' %
                    (src_file, dest_file)
                )
                t.start()

    def Configure(self, dest_path='', src_file=''):
        if not dest_path:
            dest_path = os.path.join(
                os.path.expandvars('%USERPROFILE%'),
                'Documents'
            )

        panel = eg.ConfigPanel()
        choices = sorted(f['title'] for f in self.plugin.files)

        src_st = panel.StaticText('File to download:')
        src_ctrl = wx.ComboBox(panel, -1, choices=choices)

        dest_st = panel.StaticText('Save to:')

        dest_ctrl = eg.DirBrowseButton(panel, startDirectory=dest_path)
        dest_ctrl.SetValue(dest_path)

        if src_file in choices:
            src_ctrl.SetStringSelection(src_file)
        else:
            src_ctrl.SetSelection(0)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)

        file_sizer.Add(src_st, 0, wx.ALL, 5)
        file_sizer.Add(src_ctrl, 0, wx.ALL, 5)

        dest_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dest_sizer.Add(dest_st, 0, wx.ALL, 5)
        dest_sizer.Add(dest_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        eg.EqualizeWidths((src_st, dest_st))

        panel.sizer.Add(file_sizer)
        panel.sizer.Add(dest_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dest_ctrl.GetValue(),
                src_ctrl.GetStringSelection()
            )


class OpenFile(eg.ActionBase):

    def __call__(self, file_name):
        files = self.plugin.drive.ListFile(
            {'q': "'root' in parents and trashed=false"}
        ).GetList()

        for f in files:
            if f['title'] == file_name:
                def do(f_name):
                    temp_dir = tempfile.gettempdir()
                    temp_file = os.path.join(temp_dir, f_name)
                    f.GetContentFile(temp_file, f['mimeType'])
                    self.plugin.temp_files += [temp_file]
                    subprocess.Popen(
                        '"%s"' % temp_file,
                        shell=True
                    )

                t = threading.Thread(target=do, args=(file_name,))
                t.daemon = True
                eg.Print('Google Drive: Opening file %s' % file_name)
                t.start()

    def Configure(self, file_name=''):
        panel = eg.ConfigPanel()
        choices = sorted(f['title'] for f in self.plugin.files)

        file_st = panel.StaticText('File:')
        file_ctrl = wx.ComboBox(panel, -1, choices=choices)

        if file_name in choices:
            file_ctrl.SetStringSelection(file_name)
        else:
            file_ctrl.SetSelection(0)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)

        file_sizer.Add(file_st, 0, wx.ALL, 5)
        file_sizer.Add(file_ctrl, 0, wx.ALL, 5)
        panel.sizer.Add(file_sizer)

        while panel.Affirmed():
            panel.SetResult(file_ctrl.GetStringSelection())


class ListFiles(eg.ActionBase):

    def __call__(self):
        return [f['title'] for f in self.plugin.files]


CLIENT = (
    'Y2xpZW50X2NvbmZpZ19iYWNrZW5kOiBzZXR0aW5ncwpjbGllbnRfY29uZmlnOgogIGNsaWVud'
    'F9pZDogODE1OTEwNTczMDE2LTFjaTYwMm82ZGdhdWVjcWZvZzg2ZnFyc3RxNGl0aDRsLmFwcH'
    'MuZ29vZ2xldXNlcmNvbnRlbnQuY29tCiAgY2xpZW50X3NlY3JldDogaUxTU1lNQkJPZ3ZUME9'
    'sZm50RkJqOVNTCiAgYXV0aF91cmk6IGh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29h'
    'dXRoMi9hdXRoCiAgdG9rZW5fdXJpOiBodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vY'
    'XV0aDIvdG9rZW4KICByZWRpcmVjdF91cmk6IGh0dHA6Ly9sb2NhbGhvc3Q6NTY4NzQvCgpzYX'
    'ZlX2NyZWRlbnRpYWxzOiBUcnVlCnNhdmVfY3JlZGVudGlhbHNfYmFja2VuZDogZmlsZQpzYXZ'
    'lX2NyZWRlbnRpYWxzX2ZpbGU6IGNyZWRlbnRpYWxzLmpzb24KCmdldF9yZWZyZXNoX3Rva2Vu'
    'OiBUcnVlCgpvYXV0aF9zY29wZToKICAtIGh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1d'
    'GgvZHJpdmUuZmlsZQogIC0gaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vYXV0aC9kcml2ZS'
    '5pbnN0YWxs'
)

FILE_PROPERTIES = [
    'alternateLink',
    'appDataContents',
    'canComment',
    'canReadRevisions',
    'copyable',
    'createdDate',
    'defaultOpenWithLink',
    'description',
    'downloadUrl',
    'editable',
    'embedLink',
    'etag',
    'explicitlyTrashed',
    'exportLinks',
    'fileExtension',
    'fileSize',
    'folderColorRgb',
    'fullFileExtension',
    'headRevisionId',
    'iconLink',
    'id',
    'imageMediaMetadata',
    'indexableText',
    'isAppAuthorized',
    'kind',
    'labels',
    'lastModifyingUser',
    'lastModifyingUserName',
    'lastViewedByMeDate',
    'markedViewedByMeDate',
    'md5Checksum',
    'mimeType',
    'modifiedByMeDate',
    'modifiedDate',
    'openWithLinks',
    'originalFilename',
    'ownedByMe',
    'ownerNames',
    'owners',
    'parents',
    'permissions',
    'properties',
    'quotaBytesUsed',
    'selfLink',
    'shareable',
    'shared',
    'sharedWithMeDate',
    'sharingUser',
    'spaces',
    'thumbnail'
    'thumbnailLink',
    'title',
    'userPermission',
    'version',
    'videoMediaMetadata',
    'webContentLink',
    'webViewLink',
    'writersCanShare'
]


