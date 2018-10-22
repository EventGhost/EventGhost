# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import os
import stat
import warnings
from os.path import join
from urlparse import urlparse

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import paramiko

class SftpSync(object):
    def __init__(self, url):
        self.url = url
        host = urlparse(url)
        self.remotePath = host.path
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "connecting:", host.hostname
        self.sshClient.connect(
            host.hostname,
            host.port,
            host.username,
            host.password
        )
        self.sftpClient = self.sshClient.open_sftp()

    def ClearDirectory(self, remotePath, excludes=()):
        remotePath = FixRemotePath(remotePath)
        print "clearing all files in %s" % remotePath
        remoteDir = RemoteDirectory(self.sftpClient, remotePath)
        for fileName in remoteDir.files:
            if fileName not in excludes:
                self.sftpClient.remove(remotePath + fileName)
            else:
                print (
                    "    skipping file %s because of excludes parameter" %
                    fileName
                )

    def Close(self):
        self.sftpClient.close()
        self.sshClient.close()

    def CreateDirs(self, localDir, remoteDir, remotePath):
        for dirName in localDir.dirs:
            if dirName not in remoteDir.dirs:
                print "creating directory:", remotePath + dirName
                self.sftpClient.mkdir(remotePath + dirName)
                remoteDir.dirs[dirName] = Directory()
            self.CreateDirs(
                localDir.dirs[dirName],
                remoteDir.dirs[dirName],
                remotePath + dirName + "/"
            )

    def CreateFiles(self, localDir, remoteDir, localPath, remotePath):
        for fileName in localDir.files:
            localStat = localDir.files[fileName]
            if fileName in remoteDir.files:
                remoteStat = remoteDir.files[fileName]
                if remoteStat.st_size == localStat.st_size:
                    if remoteStat.st_mtime == int(localStat.st_mtime):
                        continue
            remoteFilePath = remotePath + fileName
            print "uploading: %s --> %s" % (
                join(localPath, fileName),
                remoteFilePath
            )
            self.sftpClient.put(join(localPath, fileName), remoteFilePath)
            self.sftpClient.utime(
                remoteFilePath,
                (localStat.st_atime, localStat.st_mtime)
            )
        for dirName in localDir.dirs:
            self.CreateFiles(
                localDir.dirs[dirName],
                remoteDir.dirs[dirName],
                join(localPath, dirName),
                remotePath + dirName + "/"
            )

    def RemoveDirs(self, localDir, remoteDir, remotePath):
        for dirName in remoteDir.dirs:
            if dirName not in localDir.dirs:
                localSubDir = Directory()
            else:
                localSubDir = localDir.dirs[dirName]
            self.RemoveDirs(
                localSubDir,
                remoteDir.dirs[dirName],
                remotePath + dirName + "/"
            )
            if dirName not in localDir.dirs:
                print "removing directory:", remotePath + dirName + "/"
                self.sftpClient.rmdir(remotePath + dirName)

    def RemoveFiles(self, localDir, remoteDir, remotePath):
        for fileName in remoteDir.files:
            if fileName not in localDir.files:
                print "deleting:", remotePath + fileName
                self.sftpClient.remove(remotePath + fileName)
        for dirName in remoteDir.dirs:
            if dirName not in localDir.dirs:
                localSubDir = Directory()
            else:
                localSubDir = localDir.dirs[dirName]
            self.RemoveFiles(
                localSubDir,
                remoteDir.dirs[dirName],
                remotePath + dirName + "/"
            )

    def Sync(self, localPath, additionalFiles=None):
        print("Syncing: %s" % localPath)
        for name in list((os.walk(localPath)))[0][1]:
            localDir = join(localPath, name)
            print('checking localDir: %s' % localDir)
            self.SyncDirs(localDir, self.remotePath + name + "/")

        if additionalFiles:
            for local, remote in additionalFiles:
                print local, self.remotePath + remote
                self.sftpClient.put(local, self.remotePath + remote)

    def SyncDirs(self, localPath, remotePath):
        print "getting local directory tree:", localPath
        localDir = LocalDirectory(localPath)
        print "getting remote directory tree:", remotePath
        remoteDir = RemoteDirectory(self.sftpClient, remotePath)
        self.CreateDirs(localDir, remoteDir, remotePath)
        self.CreateFiles(localDir, remoteDir, localPath, remotePath)
        self.RemoveFiles(localDir, remoteDir, remotePath)
        self.RemoveDirs(localDir, remoteDir, remotePath)


class Directory(object):
    def __init__(self):
        self.dirs = {}
        self.files = {}


class LocalDirectory(Directory):
    def __init__(self, path):
        Directory.__init__(self)
        _, dirs, files = list(os.walk(path))[0]
        for name in dirs:
            self.dirs[name] = LocalDirectory(os.path.join(path, name))
        for name in files:
            self.files[name] = os.stat(os.path.join(path, name))


class RemoteDirectory(Directory):
    def __init__(self, client, path):
        Directory.__init__(self)
        for entry in client.listdir_attr(path):
            name = entry.filename
            if stat.S_ISDIR(entry.st_mode):
                self.dirs[name] = RemoteDirectory(client, path + "/" + name)
            else:
                self.files[name] = entry


def FixRemotePath(remotePath):
    if not remotePath.endswith("/"):
        remotePath += "/"
    return remotePath
