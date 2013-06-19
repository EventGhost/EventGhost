import stat     
import os
from urlparse import urlparse
from os.path import join
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import paramiko


def FixRemotePath(remotePath):
    if not remotePath.endswith("/"):
        remotePath += "/"
    return remotePath
    
    
class Directory(object):
    
    def __init__(self):
        self.dirs = {}
        self.files = {}
        


class LocalDirectory(Directory):
    
    def __init__(self, path):
        Directory.__init__(self)
        for name in os.listdir(path):
            fullPath = os.path.join(path, name)
            if os.path.isdir(fullPath):
                self.dirs[name] = LocalDirectory(fullPath)
            else:
                self.files[name] = os.stat(fullPath)
        
        
        
class RemoteDirectory(Directory):
    
    def __init__(self, client, path):
        Directory.__init__(self)
        for entry in client.listdir_attr(path):
            name = entry.filename
            if stat.S_ISDIR(entry.st_mode):
                self.dirs[name] = RemoteDirectory(client, path + "/" + name)
            else:
                self.files[name] = entry
        
    

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
        
        
    def SyncDirs(self, localPath, remotePath):
        print "getting local directory tree:", localPath
        localDir = LocalDirectory(localPath)
        print "getting remote directory tree:", remotePath
        remoteDir = RemoteDirectory(self.sftpClient, remotePath)
        self.CreateDirs(localDir, remoteDir, remotePath)
        self.CreateFiles(localDir, remoteDir, localPath, remotePath)
        self.RemoveFiles(localDir, remoteDir, remotePath)
        self.RemoveDirs(localDir, remoteDir, remotePath)


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
            print "uploading:", join(localPath, fileName), "-->", remoteFilePath
            self.sftpClient.put(join(localPath, fileName), remoteFilePath)
            self.sftpClient.utime(remoteFilePath, (localStat.st_atime, localStat.st_mtime))
        for dirName in localDir.dirs:
            self.CreateFiles(
                localDir.dirs[dirName], 
                remoteDir.dirs[dirName], 
                join(localPath, dirName),
                remotePath + dirName + "/"
            )
            
            
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
                
                
        
    def Sync(self, localPath, additionalFiles=None):
        for name in os.listdir(localPath):
            localDir = join(localPath, name)
            if os.path.isdir(localDir):
                self.SyncDirs(localDir, self.remotePath + name + "/")
        
        if additionalFiles:
            for local, remote in additionalFiles:
                print local, self.remotePath + remote
                self.sftpClient.put(local, self.remotePath + remote)
        
        
    def ClearDirectory(self, remotePath, excludes=()):
        remotePath = FixRemotePath(remotePath)
        print "clearing all files in %s" % remotePath
        remoteDir = RemoteDirectory(self.sftpClient, remotePath)
        for fileName in remoteDir.files:
            if fileName not in excludes:
                self.sftpClient.remove(remotePath + fileName)
            else:
                print "    skipping file %s because of excludes parameter" % fileName
    
    
    def Close(self):
        self.sftpClient.close()
        self.sshClient.close()


