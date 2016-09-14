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

import locale
import os
import urllib
import urllib2
import urlparse
import wx
from os.path import basename, dirname
from threading import Thread
from time import clock

class TransferDialog(wx.Dialog):
    """
    The progress dialog that is shown while the file is transfered.
    """
    def __init__(self, parent, transfers, stopEvent=None):
        self.stopEvent = stopEvent
        self.abort = False
        self.transfers = transfers
        self.speed = 0
        wx.Dialog.__init__(self, parent, title="Transfer Progress")
        self.messageCtrl = wx.StaticText(
            self,
            label="",
            style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        )
        style = wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE

        def SText(label, *args, **kwargs):
            """
            Simpler creation of a wx.StaticText
            """
            return wx.StaticText(self, -1, label, *args, **kwargs)

        x = 70
        self.remainingCtrl = SText("-", size=(x, -1), style=style)
        self.elapsedCtrl = SText("-", size=(x, -1), style=style)
        self.remainingSizeCtrl = SText("-", size=(x, -1), style=style)
        self.speedCtrl = SText("-", size=(x, -1), style=style)
        self.totalSizeCtrl = SText("-", style=style, size=(x, -1))

        currentStaticBox = wx.StaticBox(self, label="Current File")
        self.currentFileCtrl = SText("", style=wx.ST_NO_AUTORESIZE)
        self.currentProgressCtrl = SText("      %", style=style)
        self.gauge = wx.Gauge(
            self,
            range=1000,
            style=wx.GA_HORIZONTAL | wx.GA_SMOOTH,
            size=(-1, 15)
        )
        overallStaticBox = wx.StaticBox(self, label="Overall")
        self.overallFileCtrl = SText("", style=wx.ST_NO_AUTORESIZE)
        self.overallProgressCtrl = SText("      %", style=style)
        self.allGauge = wx.Gauge(
            self,
            range=1000,
            style=wx.GA_HORIZONTAL | wx.GA_SMOOTH,
            size=(-1, 15)
        )

        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.currentFileCtrl, 1, wx.EXPAND)
        sizer1.Add(self.currentProgressCtrl, 0, wx.ALIGN_RIGHT)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add((0, 0), 1, wx.EXPAND)
        sizer2.Add(SText("Transfer speed: "), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.speedCtrl, 0, wx.EXPAND | wx.ALIGN_RIGHT)

        sizer3 = wx.StaticBoxSizer(currentStaticBox, wx.VERTICAL)
        sizer3.Add(sizer1, 0, wx.EXPAND)
        sizer3.Add((0, 5))
        sizer3.Add(self.gauge, 0, wx.EXPAND)
        sizer3.Add((0, 5))
        sizer3.Add(sizer2, 0, wx.EXPAND)

        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(self.overallFileCtrl, 1, wx.EXPAND)
        sizer4.Add(self.overallProgressCtrl, 0, wx.ALIGN_RIGHT)

        sizer5 = wx.FlexGridSizer(4, 5, 5, 5)
        sizer5.Add(SText("Elapsed time:"), 0, wx.ALIGN_RIGHT)
        sizer5.Add(self.elapsedCtrl)
        sizer5.Add((10, 0), 1, wx.EXPAND)
        sizer5.Add(SText("Total size:"), 0, wx.ALIGN_RIGHT)
        sizer5.Add(self.totalSizeCtrl)
        sizer5.Add(SText("Remaining time:"), 0, wx.ALIGN_RIGHT)
        sizer5.Add(self.remainingCtrl)
        sizer5.Add((10, 0), 1, wx.EXPAND)
        sizer5.Add(SText("Remaining size:"), 0, wx.ALIGN_RIGHT)
        sizer5.Add(self.remainingSizeCtrl)
        sizer5.AddGrowableCol(2, 1)

        sizer6 = wx.StaticBoxSizer(overallStaticBox, wx.VERTICAL)
        sizer6.Add(sizer4, 0, wx.EXPAND)
        sizer6.Add((0, 5))
        sizer6.Add(self.allGauge, 0, wx.EXPAND)
        sizer6.Add((0, 5))
        sizer6.Add(sizer5, 0, wx.EXPAND)

        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.messageCtrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer0.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        sizer0.Add(sizer6, 0, wx.EXPAND | wx.ALL, 5)
        sizer0.Add((10, 10))
        sizer0.Add(self.cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizerAndFit(sizer0)
        self.SetSize((400, -1))
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        self.startTime = clock()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        Thread(target=self.ThreadRun).start()
        self.Show()

    def CreateActions(self):
        self.overallSize = 0
        todo = []
        for src, dest in self.transfers:
            root = src.split(":", 1)[0].lower()
            if root in "abcdefghijklmnopqrstuvwxyz":
                # local file
                size = self.LocalGetSize(src)
                action = self.SftpUpload
            elif root == "http":
                urlparts = urlparse.urlsplit(src)
                urlparts = urlparts._replace(path=urllib.quote(urlparts.path))
                src = urlparse.urlunsplit(urlparts)
                size = self.HttpGetSize(src)
                action = self.HttpDownload
            todo.append(((action, src, dest, size, self.overallSize)))
            self.overallSize += size
        return todo

    def HttpDownload(self, src, dest, size):
        testFile = urllib2.urlopen(src)
        infile = ProgressFile(testFile, size, self.SetProgress, self.speed)
        try:
            os.makedirs(dirname(dest))
        except:
            pass
        outfile = open(dest, "wb")
        while True:
            data = infile.read(32768)
            if len(data) == 0:
                break
            outfile.write(data)
        infile.close()
        outfile.close()

    def HttpGetSize(self, path):
        testFile = urllib2.urlopen(path)
        return int(testFile.info()["Content-Length"])

    def LocalGetSize(self, path):
        return os.stat(path).st_size

    def OnCancel(self, dummyEvent):
        """
        Handles a click on the cancel button.
        """
        self.abort = True
        self.cancelButton.Enable(False)
        self.messageCtrl.SetLabel("Closing connection. Please wait...")

    def OnTimer(self, dummyEvent):
        """
        Called every second to update the progress dialog.
        """
        elapsedTime = clock() - self.startTime
        self.elapsedCtrl.SetLabel(GetTimeStr(elapsedTime))

    def SetProgress(self, *args, **kwargs):
        wx.CallAfter(self._SetProgress, *args, **kwargs)
        if self.abort:
            return False

    def SftpUpload(self, src, dest, size):
        log = self.messageCtrl.SetLabel
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            import paramiko

        testFile = open(src, "rb")
        infile = ProgressFile(testFile, size, self.SetProgress)

        urlParts = urlparse.urlparse(dest)
        log("Connecting to sftp://%statInfo..." % urlParts.hostname)
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            sshClient.connect(
                urlParts.hostname,
                urlParts.port,
                urlParts.username,
                urlParts.password,
            )
        except paramiko.SSHException:
            exit("Error: Couldn't connect to server")
        except paramiko.AuthenicationException:
            exit("Error: Authentication Exception")
        except paramiko.BadHostKeyException:
            exit("Error: Bad Host Key Exception")

        try:
            client = sshClient.open_sftp()
        except:
            exit("Error: Can't create SFTP client")
        destPath = urlParts.path  #IGNORE:E1101
        destDir = dirname(destPath)
#        log("Changing path to: %s" % destDir)
#        client.chdir(destDir)
        log("Getting directory listing...")
        fileList = client.listdir(destDir)
        log("Creating temp name.")
        for i in range(0, 999999):
            tempFileName = "tmp%06d" % i
            if tempFileName not in fileList:
                break
        if destDir[-1] != "/":
            destDir += "/"
        tmpPath = destDir + tempFileName
        log("Uploading " + basename(src))

        outfile = client.file(tmpPath, 'wb')
        outfile.set_pipelined(True)
        while True:
            data = infile.read(32768)
            if len(data) == 0:
                break
            outfile.write(data)
        infile.close()
        outfile.close()
        rSize = client.stat(tmpPath).st_size

        if self.abort:
            client.remove(tmpPath)
            log("Upload canceled by user.")
        else:
            if rSize != size:
                raise IOError('size mismatch in put! %d != %d' % (rSize, size))
            if basename(destPath) in fileList:
                client.remove(destPath)
            client.rename(tmpPath, destPath)
            localStat = os.stat(src)
            client.utime(destPath, (localStat.st_atime, localStat.st_mtime))
            log("Upload done!")
        client.close()

    def ThreadRun(self):
        """
        Transfers the files in a separate thread.
        """
        try:
            self.overallSize = 0
            self.transferedSize = 0
            todo = self.CreateActions()
            for i, (action, src, dest, size, transferedSize) in enumerate(todo):
                self.transferedSize = transferedSize
                self.currentFileCtrl.SetLabel(basename(dest))
                self.overallFileCtrl.SetLabel("File %d of %d" % (i + 1, len(todo)))
                action(src, dest, size)
        finally:
            if self.stopEvent:
                self.stopEvent.set()
            wx.CallAfter(self.Destroy)

    def _SetProgress(self, speed, pos, size):
        self.speed = speed
        overallPos = self.transferedSize + pos
        if speed:
            remainingTime = (self.overallSize - overallPos) / speed
        else:
            remainingTime = 1000
        percent = int((pos * 100.0) / size)
        allPercent = int(overallPos * 100.0 / self.overallSize)
        self.gauge.SetValue(percent * 10)
        self.allGauge.SetValue(allPercent * 10)
        self.SetTitle("%d%% Transfer Progress" % allPercent)
        self.currentProgressCtrl.SetLabel("%d%%" % percent)
        self.overallProgressCtrl.SetLabel("%d%%" % allPercent)
        self.speedCtrl.SetLabel("%0.2f KiB/s" % (speed / 1024))
        self.remainingCtrl.SetLabel(GetTimeStr(remainingTime + 1))
        self.remainingSizeCtrl.SetLabel(FormatBytes(self.overallSize - overallPos))
        self.totalSizeCtrl.SetLabel(FormatBytes(self.overallSize))


class ProgressFile(object):
    """
    A proxy to a file, that also holds progress information.
    """
    def __init__(self, fileObject, size, progressCallback=None, initialSpeed=0):
        self.progressCallback = progressCallback
        self.period = 15
        self.start = 0
        self.lastSecond = 0
        self.lastBytes = 0
        self.Reset()
        self.rate = initialSpeed

        self.size = size
        self.fileObject = fileObject
        self.pos = 0
        self.startTime = clock()

    def Add(self, numBytes):
        now = clock()
        if numBytes == 0 and (now - self.lastSecond) < 0.1:
            return

        if self.rate == 0:
            self.Reset()

        div = self.period * 1.0
        if self.start > now:
            self.start = now
        if now < self.lastSecond:
            self.lastSecond = now

        timePassedSinceStart = now - self.start
        timePassed = now - self.lastSecond
        if timePassedSinceStart < div:
            div = timePassedSinceStart
        if div < 1:
            div = 1.0

        self.rate *= 1 - timePassed / div
        self.rate += numBytes / div

        self.lastSecond = now
        if numBytes > 0:
            self.lastBytes = now
        if self.rate < 0:
            self.rate = 0

    def close(self):  #IGNORE:C0103 Invalid name "read"
        """
        Implements a file-like close()
        """
        self.fileObject.close()
        elapsed = (clock() - self.startTime)  # NOQA

    def read(self, size):  #IGNORE:C0103 Invalid name "read"
        """
        Implements a file-like read() but also updates the progress variables.
        """
        data = self.fileObject.read(size)
        numBytes = len(data)
        self.pos += numBytes
        self.Add(numBytes)
        if self.progressCallback:
            if self.progressCallback(self.rate, self.pos, self.size) is False:
                return ""
        return data

    def Reset(self):
        now = clock()
        self.start = now
        self.lastSecond = now
        self.rate = 0
        self.lastBytes = 0


def FormatBytes(numBytes):
    """
    Returns a formatted string of a byte count value.
    """
    return locale.format("%d", numBytes, grouping=True)

def GetTimeStr(seconds):
    """
    Returns a nicely formatted time string.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%0.2d:%0.2d" % (hours, minutes, seconds)
