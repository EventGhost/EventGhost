# Plugins/MediaMonkey/__init__.py
#
# Copyright (C)  2009 Pako  <lubos.ruckl@quick.cz>
#
# This file is part of EventGhost.
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#Last change: 2010-02-10 12:24  GMT+1

import wx
from win32com.client import Dispatch
from eg.WinApi.Utils import CloseHwnd
import time
import datetime
import wx.lib.masked as masked
import codecs
from os.path import isfile
from os.path import split as path_split
from os import remove as remove_file
from functools import partial
from random import randint


eg.RegisterPlugin(
    name = "MediaMonkey",
    author = "Pako",
    version = "0.2.12",
    kind = "program",
    guid = "{50602341-ABC3-47AD-B859-FCB8C03ED4EF}",
    createMacrosOnAdd = True,
    description = ur'''<rst>
Adds support functions to control MediaMonkey_.

**Note:**
 To trigger events from MediaMonkey_, you must install
 "EventGhost.vbs" file to *MediaMonkey/Scripts/Auto* folder.

.. _MediaMonkey: http://www.MediaMonkey.com/ ''',
    url = "http://www.eventghost.org/forum/viewtopic.php?t=563",
    icon = (
        "R0lGODlhEAAQAPcAADQyNLyaTHRmRJSWlPzGNFxOPGxqbFROVKSGRJyWfOzSlOTCdGRmZ"
        "HReRERCPIRyTNy2dIyCbPzSZMSylExOTFxaXOTe5HxyVOS2ROzCTFxWPIx+ZKSajDw6PP"
        "zinExGTPTSfHR2dFRWVKSOVLyibGxiTExKRISKjNy+lIx6VPzOVKyaZLSqnFRSRJyGTNT"
        "GrOzKfERCRJR6RNS2fPzWdGRiXIx2VMyqXGxWPEQ+RDw2PMSiRIRuVJyenPzKRHRydFRS"
        "VLSedNS6hHx2ZGRaTIR2TKSSdPzWbMS6pFxeXPzy1IRyVPzKTGRWPKSSXLymhEQ+PPzqt"
        "PzahHx+fFxWVLymfHRiTJyShMzCpPzSXFxSRKSKTOzWtExGRNy2fMSqZH4HhAAAAAAAAM"
        "AAAAAIEgAACgAAEwAAAP8JhP8AAP8AAP8AAP8yAP8HAP+RAP98AACreAAGAACRTQB8AAA"
        "wBADqAAASAAAAAADQ4gA8BBUlAABbAGAIYOlAnhI4gAAAfNJ4IOYARYEAH3wAAMhNAMUA"
        "ABwAAAAAAErwB+PqAIESAHwAAKBGAHfQAFAmAABbAMgIAMVAQAE4HwAAAGsFAAAAAAAAA"
        "AAAAJxuAOi9ABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4AnpAAgHwAfH"
        "AA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pKgW3AJGSAHx8AEogKvRFAIAfAHwAAAA0WAB"
        "k8RWDEgB8AAD//wD//wD//wD//8gAAMUAABwAAAAAAABcpAHq6wASEgAAAAA09gBkOACD"
        "TAB8AFcIhPT864ASEnwAAIgYd+ruEBKQTwB8AMgAuMW36xySEgB8AKD/NAD/ZAD/gwD/f"
        "B8gWgBF7AAfEgAAABE01ABk/wCD/wB8fwSgMADr7AASEgAAAAPnIABkRQCDHwB8AACINA"
        "BkZACDgwB8fAABIAAARQAAHwAAAAQxbgAAvQAwAAAAAAMBAAAAAAAAAAAAAAAajQAA4gA"
        "ARwAAACH5BAEAABYALAAAAAAQABAABwjtAC0IFNjDgMEfPQYqtDCAAY8gECCQ4FFjwMIQ"
        "ViBIOcLxiAcUVgwMPGFlAY0jErJIkBBFCRcrJwQyIIEyywoDI2AoUfLiiQgLIT58OZIlA"
        "BAKQK5wqFABSJcpXSLQkKACQYyrMRzEeJDCRJcYQ1Ay2dFFqwMtGFReceAASokiBWIAuN"
        "olg48sRy7o6NJCRwetFBx0IEKACd4UHX7YUIAFCYUOOhwU8KFCgpQlIk2gUMLir2AZlY9"
        "AiCGzxAQAHbZsASBAwhEYApIMNFHCyIwbAHSMkAKhBJSFSRwsqYKjQJUHUH4ulAmgOQAG"
        "CwMCADs="
    ),
)
#====================================================================
MyWindowMatcher = eg.WindowMatcher(
    None,
    u'{*}MediaMonkey{*}',
    u'TFMainWindow{*}',
    None,
    None,
    1,
    True,
    0,
    0
)

SONG_TABLE_FIELDS=(
    ("Album","T","AlbumName"),
    ("AlbumArtist","T","AlbumArtistName"),
    ("Artist","T","ArtistName"),
    ("AudioCDTrack","I",""),
    ("Author","T","Author"),
    ("Band","T","Band"),
    ("Bitrate","I","Bitrate"),
    ("BPM","I","BPM"),
    ("Broadcast","I",""),
    ("CacheName","T","CachedPath"),
    ("CacheStatus","I","Cached"),
    ("Comment","T","Comment"),
    ("Conductor","T","Conductor"),
    ("Copyright","T","Copyright"),
    ("Copyrighted","I",""),
    ("Custom1","T","Custom1"),
    ("Custom2","T","Custom2"),
    ("Custom3","T","Custom3"),
    ("Custom4","T","Custom4"),
    ("Custom5","T","Custom5"),
    ("DateAdded","D","DateAdded"),
    ("DiscNumber","T","DiscNumberStr"),
    ("EncodedBy","T",""),
    ("Encoder","T","Encoder"),
    ("FileLength","I","FileLength"),
    ("FileModified","D","FileModified"),
    ("GaplessBytes","I","GaplessBytes"),
    ("Genre","T","Genre"),
    ("GroupDesc","T","Grouping"),
    ("ID","I","ID"),
    ("IDAlbum","I",""),
    ("IDFolder","I",""),
    ("IDMedia","I","Media"),
    ("InitialKey","T",""),
    ("InvolvedPeople","T","InvolvedPeople"),
    ("ISRC","T","ISRC"),
    ("Language","T",""),
    ("LastTimePlayed","D","LastPlayed"),
    ("Lyricist","T","Lyricist"),
    ("Lyrics","T","Lyrics"),
    ("MaxSample","R",""),
    ("MediaType","T",""),
    ("Mood","T","Mood"),
    ("NormalizeAlbum","R","LevelingAlbum"),
    ("NormalizeTrack","R","Leveling"),
    ("Occasion","T","Occasion"),
    ("OrigArtist","T","OriginalArtist"),
    ("OrigFileLength","I",""),
    ("Original","I",""),
    ("OrigLyricist","T","OriginalLyricist"),
    ("OrigTitle","T","OriginalTitle"),
    ("OrigYear","I","OriginalYear"),
    ("PlaybackPos","I","Bookmark"),
    ("PlayCounter","I","PlayCounter"),
    ("PostGap","I","PostGap"),
    ("PreGap","I","PreGap"),
    ("PreviewLength","I",""),
    ("PreviewName","T","PreviewPath"),
    ("PreviewStartTime","I",""),
    ("PreviewState","I",""),
    ("Publisher","T","Publisher"),
    ("Quality","T","Quality"),
    ("Rating","I","Rating"),
    ("RatingString","T",""),
    ("Remixer","T",""),
    ("SamplingFrequency","I","SampleRate"),
    ("Seekable","I","isBookmarkable"),
    ("SignPart1","I",""),
    ("SignPart2","I",""),
    ("SignPart3","I",""),
    ("SignPart4","I",""),
    ("SignType","I",""),
    ("SongLength","I","SongLength"),
    ("SongPath","T","Path"),
    ("SongTitle","T","Title"),
    ("Stereo","I","Channels"),
    ("SubTitle","T",""),
    ("Tempo","T","Tempo"),
    ("TotalSamples","I","TotalSamples"),
    ("TrackModified","D",""),
    ("TrackNumber","T","TrackOrderStr"),
    ("VBR","I","VBR"),
    ("WebArtist","T",""),
    ("WebCommercial","T",""),
    ("WebCopyright","T",""),
    ("WebFilepage","T",""),
    ("WebPayment","T",""),
    ("WebPublisher","T",""),
    ("WebRadio","T",""),
    ("WebSource","T",""),
    ("WebUser","T",""),
    ("Year","I","Year"),
)
#===============================================================================

#class MyFileBrowseButton(eg.FileBrowseButton):
#    def GetTextCtrl(self):          #  now I can make build-in textCtrl
#        return self.textControl     #  non-editable !!!
#====================================================================

class MediaMonkeyWorkerThread(eg.ThreadWorker):
    """
    Handles the COM interface in a thread of its own.
    """
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.MM = Dispatch("SongsDB.SDBApplication")
        self.MM.ShutdownAfterDisconnect = False
            
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        del self.MM
        self.plugin.workerThread = None
        
    def isRunning(self):
        flag = True
        counter = 0
        try:
            if self.MM.IsRunning:
                return True
        except:
            pass
        del self.MM
        self.MM = Dispatch("SongsDB.SDBApplication")
        self.MM.ShutdownAfterDisconnect = False
        while not self.MM.IsRunning:
            counter += 1
            if counter >= 1000:
                flag = False
                break
        return flag            
        
    def DoCommand(self, command):
        if self.isRunning():
            getattr(self.MM.Player, command)()

    def SetValue(self, command, value):
        if self.isRunning():
            setattr(self.MM.Player,command, value)
        
    def GetValue(self,command):
        if self.isRunning():
            return getattr(self.MM.Player, command)
        
    def Previous(self):
        if self.isRunning():
            if self.MM.Player.CurrentSongIndex !=0:
                self.MM.Player.Previous()
            elif self.MM.Player.isRepeat:
                self.MM.Player.CurrentSongIndex = self.MM.Player.PlaylistCount-1
       
    def GetSongData(self,index):
        if self.isRunning():
            repeat = self.MM.Player.isRepeat
            SongDataDict = dict([(item[2],None) for item in SONG_TABLE_FIELDS if item[2] != ""])
            curIndx = self.MM.Player.CurrentSongIndex
            count = self.MM.Player.PlaylistCount
            if not repeat:
                if (index == 1 and curIndx == count-1) or (index == -1 and curIndx == 0):
                    return None,None
            else:
                if index == 1 and curIndx == count-1:
                    curIndx = -1
                elif index == -1 and curIndx == 0:
                    curIndx = count    
            index += curIndx
            tmpObject = self.MM.Player.PlaylistItems(index)
            
            for item in SongDataDict.iterkeys():
                itm = getattr(tmpObject,item)
                if type(itm) == unicode:
                    SongDataDict[item] = itm
                else:
                    SongDataDict[item] = str(itm)
            return SongDataDict, index+1

    def WriteToMMdatabase(self, command, value, flag):
        if self.isRunning():
            setattr(self.MM.Player.CurrentSong,command,value)
            self.MM.Player.CurrentSong.UpdateDB()
            if flag:
                self.MM.Player.CurrentSong.WriteTags()
       
    def LoadPlaylistByTitle(self, plString,repeat,shuffle,crossfade,clear):
        if self.isRunning():
            plItems = self.MM.PlaylistByTitle(plString).Tracks
            Total = plItems.Count
            if Total > 0:
                if repeat < 2:
                    self.MM.Player.isRepeat = bool(repeat)
                if crossfade < 2:
                    self.MM.Player.isCrossfade = bool(crossfade)
                if shuffle < 2:
                    self.MM.Player.isShuffle = bool(shuffle)
                if clear:
                    self.MM.Player.PlaylistClear()
                    self.MM.Player.PlaylistAddTracks(plItems)
                    self.MM.Player.Stop()
                else:
                    self.MM.Player.PlaylistAddTracks(plItems)
                if self.MM.Player.isPaused or not self.MM.Player.isPlaying:
                    self.MM.Player.Play()
            if self.plugin.trigger:
                self.plugin.TriggerEvent(Text.playlistEvt, (plString, str(Total)))
                    
    def GetNotAccessibleTracks(self, filePath):
        if self.isRunning():
            count = 0
            try:
                MyTracks = self.MM.Database.QuerySongs("")
                file = codecs.open(filePath,encoding='utf-8', mode='w',errors='replace')
                while not MyTracks.EOF:
                    path = MyTracks.Item.Path
                    if not isfile(path):
                        count += 1
                        file.write('\t'.join((
                            str(MyTracks.Item.ID),
                            MyTracks.Item.Title,
                            path,
                        )))
                        file.write('\n')
                    MyTracks.Next()
                file.close()
            except:
                pass
            self.plugin.TriggerEvent("unaccessible",str(count))

    def DeleteSongFromLibrary(self,ID):
        if self.isRunning():
            sql = ' FROM Songs WHERE ID="%s"' % ID
            self.MM.Database.ExecSQL('DELETE'+sql)
            return self.MM.Database.OpenSQL('SELECT COUNT(*)'+sql).ValueByIndex(0)
            
    def AddSongToPlaylist(self, plString, skip):
        if self.isRunning():
            idSong=self.MM.Player.CurrentSong.ID
            IDPlaylist=self.MM.PlaylistByTitle(plString).ID
            if IDPlaylist <> 0:
                sql="SELECT COUNT(*) FROM PlaylistSongs WHERE PlaylistSongs.IDSong="+\
                    str(idSong)+" AND PlaylistSongs.IDPlaylist="+str(IDPlaylist)
                if self.MM.Database.OpenSQL(sql).ValueByIndex(0) == "0":
                    self.MM.PlaylistByTitle(plString).AddTrackById(idSong)
                    res = 0
                else:
                    res = 1
            else:
                res = 2
            if skip:
                self.MM.Player.Next()
            if self.plugin.trigger:
                self.plugin.TriggerEvent(self.plugin.text.resAdded[3],self.plugin.text.resAdded[res] % plString)

    def RemoveSongFromPlaylist(self, plString, skip, now_pl):
        if self.isRunning():
            Player = self.MM.Player
            idSong=Player.CurrentSong.ID
            IDPlaylist=self.MM.PlaylistByTitle(plString).ID
            if IDPlaylist <> 0:
                sql=" FROM PlaylistSongs WHERE IDPlaylist="+str(IDPlaylist)+" AND IDSong="+str(idSong)
                if self.MM.Database.OpenSQL("SELECT COUNT(*)"+sql).ValueByIndex(0) == "1":
                    self.MM.Database.ExecSQL("DELETE"+sql)
                    self.MM.MainTracksWindow.Refresh()
                    indx=Player.CurrentSongIndex
                    if indx > -1:
                        if idSong==Player.PlaylistItems(indx).ID:
                            if now_pl:
                                Player.PlaylistDelete(indx)
                        res = 0
                else:
                    res = 1
            else:
                res = 2
            if skip:
                Player.Next()
            if self.plugin.trigger:
                self.plugin.TriggerEvent(self.plugin.text.resRemoved[3],self.plugin.text.resRemoved[res] % plString)

    def RemoveSongFromNowPlaying(self, skip):
        if self.isRunning():
            Player = self.MM.Player
            res = 1
            idSong=Player.CurrentSong.ID
            indx=Player.CurrentSongIndex
            if indx > -1:
                if idSong==Player.PlaylistItems(indx).ID:
                    Player.PlaylistDelete(indx)
                    res = 0
                if skip:
                    Player.Next()
            if self.plugin.trigger:
                self.plugin.TriggerEvent(self.plugin.text.resNowPlay[2],self.plugin.text.resNowPlay[res])
            
    def LoadPlaylist(self,sql,repeat,crossfade,shuffle,clear,Total,plName):
        MyTracks = self.MM.Database.QuerySongs(sql)
        tmpSongList = self.MM.NewSongList
        n=0
        while not MyTracks.EOF:
            tmpSongList.Add(MyTracks.Item)
            n+=1
            if n==10:
                if clear:
                    self.MM.Player.PlaylistClear()
                    self.MM.Player.Stop()
                self.MM.Player.PlaylistAddTracks(tmpSongList)
                if repeat<2:
                    self.MM.Player.isRepeat = bool(repeat)
                if crossfade<2:
                    self.MM.Player.isCrossfade = bool(crossfade)
                if shuffle<2:
                    self.MM.Player.isShuffle = bool(shuffle)
                if self.MM.Player.isPaused or not self.MM.Player.isPlaying:
                    self.MM.Player.Play()
                del tmpSongList
                tmpSongList = self.MM.NewSongList
            MyTracks.Next()
        if n > 0 and n < 10:
            if clear:
                self.MM.Player.PlaylistClear()
                self.MM.Player.Stop()
                if repeat<2:
                    self.MM.Player.isRepeat = bool(repeat)
                if crossfade<2:
                    self.MM.Player.isCrossfade = bool(crossfade)
                if shuffle<2:
                    self.MM.Player.isShuffle = bool(shuffle)
            if self.MM.Player.isPaused or not self.MM.Player.isPlaying:
                self.MM.Player.PlaylistAddTracks(tmpSongList)
                self.MM.Player.Play()
        else:
            self.MM.Player.PlaylistAddTracks(tmpSongList)            
        if self.plugin.trigger:
            self.plugin.TriggerEvent(Text.playlistEvt, (plName, str(Total)))


    def LoadFilterPlaylist(
        self,
        plName,
        mode,
        listRules,
        order,
        trend,
        crit,
        limit,
        random,
        num,
        repeat,
        shuffle,
        crossfade,
        clear,
        unitList,
        trendList
    ):
        if self.isRunning():
            propertiesList = SONG_TABLE_FIELDS
            sql=""
            op=' AND ' if mode == 0 else ' OR '
            for rule in listRules:
                rule_2 = eg.ParseString(rule[2])
                i=listRules.index(rule)
                substValues1=(op,propertiesList[rule[0]][0],rule_2)
                substValues2=(op,rule_2,propertiesList[rule[0]][0])
                substValues3=(op,propertiesList[rule[0]][0])
                dateType=propertiesList[rule[0]][1]
                emptVal = '""'  if dateType == "T" else '"-1"'
                tuplOper=("=","<>",">",">=","<","<=")

                if dateType=="D":
                    if rule[1]<6:
                        for ix in range(0,6):
                            if rule[1]==ix:
                                substValues=(op,propertiesList[rule[0]][0],tuplOper[ix],rule_2)
                                sql+="%sstrftime('%%Y-%%m-%%d %%H:%%M:%%S',%s+2415018.5)%s'%s'" % substValues
                                break
                    else:
                        substValues=(op,propertiesList[rule[0]][0],rule_2[:-1],unitList[int(rule_2[-1])])
                        if rule[1]==6:
                            sql+="%s(%s+2415018.5)>julianday('now','-%s %s','localtime')" % substValues
                        if rule[1]==7:
                            sql+="%s(%s+2415018.5)<julianday('now','-%s %s','localtime')" % substValues
                else: # (No "DateType")
                    for ix in range(0,6):
                        if rule[1]==ix:
                            substValues=(op,propertiesList[rule[0]][0],tuplOper[ix],rule_2)
                            sql+='%s%s%s"%s"' % substValues
                            break
                    if rule[1]==6:
                        sql+='%slike("%s%%",%s)' % substValues2
                    if rule[1]==7:
                        sql+='%sNOT like("%s%%",%s)' % substValues2
                    elif rule[1]==8:
                        sql+='%slike("%%%s",%s)' % substValues2
                    elif rule[1]==9:
                        sql+='%sNOT like("%%%s",%s)' % substValues2
                    elif rule[1]==10:
                        sql+='%sinstr(%s,"%s")' %  substValues1
                    elif rule[1]==11:
                        sql+='%sNOT (instr(%s,"%s"))' %  substValues1
                    elif rule[1]==12:
                        sql+='%s%s=' % substValues3 + emptVal
                    elif rule[1]==13:
                        sql+='%s%s<>' % substValues3 + emptVal
            sql=(sql[5:] if mode==0 else sql[4:])
            if random:
                sql += " ORDER BY RANDOM()"        
            elif order:
                sql+=" order by "+propertiesList[crit][0]+" "+trendList[trend]
            if limit:
                sql+=" limit "+str(num)

            #print sql #Debuging
            Total=self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
            if int(Total) > 0:
                self.LoadPlaylist(sql,repeat,crossfade,shuffle,clear,Total,plName)

    def LoadSqlPlaylist(
        self,
        plName,
        sql,
        repeat,
        shuffle,
        crossfade,
        clear,
    ):
        if self.isRunning():
            #print sql #Debuging
            sql = eg.ParseString(sql)
            Total=self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
            n=0
            if int(Total) > 0:
                self.LoadPlaylist(sql,repeat,crossfade,shuffle,clear,Total,plName)        
        
    def GetStatistics(self):
        if self.isRunning():
            tracks = self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Songs").ValueByIndex(0)
            albums = self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Albums").ValueByIndex(0)
            #artists = self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Artists").ValueByIndex(0)
            #playlists = self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Playlists").ValueByIndex(0)
            return tracks,albums #,artists,playlists
        
    def Jubox(self,ID,clear,repeat,shuffle,crossfade,stop):
        if self.isRunning():
            sql = 'IDAlbum="%s"' % ID
            Total=self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
            tmpSongList = self.MM.NewSongList
            if int(Total) > 0:
                if clear:
                    self.MM.Player.PlaylistClear()
                    count = 0
                else:
                    count = self.MM.Player.PlaylistCount
                MyTracks = self.MM.Database.QuerySongs(sql)
                res = (MyTracks.Item.AlbumName,MyTracks.Item.ArtistName)
                while not MyTracks.EOF:
                    tmpSongList.Add(MyTracks.Item)
                    MyTracks.Next()
                if repeat<2:
                    self.MM.Player.isRepeat = bool(repeat)
                if crossfade<2:
                    self.MM.Player.isCrossfade = bool(crossfade)
                if shuffle<2:
                    shuffle = bool(shuffle)
                    self.MM.Player.isShuffle = shuffle
                else:
                    shuffle = self.MM.Player.isShuffle
                self.MM.Player.PlaylistAddTracks(tmpSongList)
                if stop:
                    if not shuffle:
                        self.MM.Player.CurrentSongIndex = count
                    else:
                        self.MM.Player.CurrentSongIndex = randint(count,count+int(Total)-1)
                if self.MM.Player.isPaused or not self.MM.Player.isPlaying:
                    self.MM.Player.Play()
                if self.plugin.trigger:
                    self.plugin.TriggerEvent(Text.albumEvt, res)

    def SongJubox(self,ID,clear,stop):
        if self.isRunning():
            sql = 'ID="%s"' % ID
            res = None
            Total=self.MM.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
            if int(Total) > 0:
                if clear:
                    self.MM.Player.PlaylistClear()
                MyTrack = self.MM.Database.QuerySongs(sql)
                res = (MyTrack.Item.Title,MyTrack.Item.AlbumName,MyTrack.Item.ArtistName)
                count = self.MM.Player.PlaylistCount
                self.MM.Player.PlaylistAddTrack(MyTrack.Item)
                if stop:
                    self.MM.Player.CurrentSongIndex = count
                if self.MM.Player.isPaused or not self.MM.Player.isPlaying:
                    self.MM.Player.Play()
                if self.plugin.trigger:
                    self.plugin.TriggerEvent(Text.songEvt, res)

    def ExportAlbumList(self,filePath):
        if self.isRunning():
            count = 0
            try:
                albums=self.MM.Database.OpenSQL("SELECT ID,Artist,Album FROM Albums")   
                file = codecs.open(filePath,encoding='utf-8', mode='w',errors='replace')
                while not albums.EOF: #Structure = ID, Artist, Album
                    count += 1
                    artist = albums.ValueByIndex(1)
                    artist = artist if artist else Text.unknArtist
                    album = albums.ValueByIndex(2)
                    album = album if album else Text.unknAlbum
                    file.write('\t'.join((
                        str(albums.ValueByIndex(0)),
                        album,
                        artist
                    )))
                    file.write('\n')
                    albums.Next()
                file.close()
            except:
                pass
            self.plugin.TriggerEvent("jukebox", str(count))
                
    def ExportSongList(self,filePath):
        if self.isRunning():
            count = 0
            try:
                songs=self.MM.Database.QuerySongs("")   
                file = codecs.open(filePath,encoding='utf-8', mode='w',errors='replace')
                while not songs.EOF:
                    count += 1
                    artist = songs.Item.ArtistName
                    artist = artist if artist else Text.unknArtist
                    file.write('\t'.join((
                        str(songs.Item.ID),
                        songs.Item.Title,
                        artist
                    )))
                    file.write('\n')
                    songs.Next()
                file.close()
            except:
                pass
            self.plugin.TriggerEvent("jukebox", str(count))
#====================================================================

class Text:
    unknAlbum = "<unknown album>"
    unknArtist = "<unknown artist>"
    errorNoWindow = "Couldn't find MediaMonkey window"
    errorConnect = "MediaMonkey is not running or not connected"
    mainGrpName = "Main control of MediaMonkey"
    mainGrpDescr = "Actions for main control of MediaMonkey."
    levelGrpName = "Another control of MediaMonkey"
    levelGrpDescr = (
        "More actions for control of MediaMonkey"
        " (volume, balance, seek, ...)."
    )
    extrGrpName = "Writing to MM database"
    extrGrpDescr = (
        "Actions for writing various parameters to MediaMonkey's database."
    )
    infoGrpName = "Information retrieval"
    infoGrpDescr = (
        "Retrieve information about the MM player settings and"
        " information about songs in the MM playlist."
    )
    labelsA = (
        'ID     ',
        'Album',
        'Artist',
    )
    labelsS = (
        'ID     ',
        'Song title',
        'Artist',
    )    
    labelsU = (
        'ID     ',
        'Song title',
        'File path',
    )
    
    toolTipFolder = "Press button and browse to select file ..."
    browseTitle = "Selected file:"
  
    please = "Please be patient"
    close = "Close"
    popup = "Add now"
    popup2 = "Delete from library"
    refresh = "Refresh"
    sepLabel = 'Character or string to use as delimiter:'
    filepath = "File path"
    filename = "File name"
    triggerEvents = "Trigger events"
    triggerEventsToolTip = '''If you select this option, some actions (such as %s
or %s) will trigger an event upon completion,
a payload is used to indicate the results of the action. 

The event triggered will be constructed as follows:
Prefix: MediaMonkey
Suffix: a string indicating the particular command (e.g. playlist, or track_added)
Payload: this will depend on the results of the action

For example, if you try to add a track to a playlist 'test' the payload will be either:
u"Track already exists in playlist test" or u"Track added to playlist test"

Another example: executing 'Load Playlist by Filter', where you choose name
the filter 'Beatles' the result may be: MediaMonkey.playlist (u'Beatles','220')
220 indicates that there are 220 tracks in the library that match your query.'''

    playlistEvt = 'playlist'
    albumEvt = 'album_added'
    songEvt = 'song_added'
    
    resAdded = (
        "Track added to playlist %s",
        "Track already exists in playlist %s",
        "Playlist %s does not exist",
        "track_added"
    )
    
    resRemoved = (
        "Track removed from playlist %s",
        "Track does not exist in playlist %s",
        "Playlist %s does not exist",
        "track_removed"
    )
    
    resNowPlay = (
        "Track removed from Now Playing playlist",
        "Track not removed from Now Playing playlist",
        "removed_from_now_playing"
    )
    
    sepToolTip = '''Optionally, enter the character
or string to be used as a delimiter (separator), between items.
Default is to use the character "\\n" (new line).'''

    repeat = "Continous playback"
    shuffle = "Shuffle tracks"
    crossfade = "Crossfade"
    clearPlaylist = "Clear the Now Playing playlist before adding new tracks"
    stopPlaying = "Stop playing just sounding songs"
    random = "Order by random"
    randomToolTip = '''(True Shuffle)  Shuffles the playlist (like cards) before starting playback.
This allows us to see what song will play next, and what played previously.
Whereas selecting the "%s" checkbox will cause the player to jump randomly through a playlist.'''

    SongTableFields = (
        "Album",
        "Album Artist",
        "Artist",
        "Audio CD Track",
        "Author",
        "Band",
        "Bitrate",
        "BPM",
        "Broadcast",
        "Cache Name",
        "Cache Status",
        "Comment",
        "Conductor",
        "Copyright",
        "Copyrighted",
        "Custom1",
        "Custom2",
        "Custom3",
        "Custom4",
        "Custom5",
        "Date Added",
        "Disc Number",
        "Encoded By",
        "Encoder",
        "File Length",
        "File Modified",
        "Gapless Bytes",
        "Genre",
        "Group Desc",
        "Song ID",
        "ID Album",
        "ID Folder",
        "ID Media",
        "Initial Key",
        "Involved People",
        "ISRC",
        "Language",
        "Last Time Played",
        "Lyricist",
        "Lyrics",
        "Max Sample",
        "Media Type",
        "Mood",
        "Normalize Album",
        "Normalize Track",
        "Occasion",
        "Original Artist",
        "Original FileLength",
        "Original",
        "Original Lyricist",
        "Original Title",
        "Original Year",
        "Playback Position",
        "Play Counter",
        "Post Gap",
        "Pre Gap",
        "Preview Length",
        "Preview Name",
        "Preview StartTime",
        "Preview State",
        "Publisher",
        "Quality",
        "Rating",
        "Rating String",
        "Remixer",
        "Sampling Frequency",
        "Seekable",
        "Sign Part1",
        "Sign Part2",
        "Sign Part3",
        "Sign Part4",
        "Sign Type",
        "Song Length",
        "Song Path",
        "Song Title",
        "Stereo",
        "SubTitle",
        "Tempo",
        "Total Samples",
        "Track Modified",
        "Track Number",
        "VBR",
        "Web Artist",
        "Web Commercial",
        "Web Copyright",
        "Web Filepage",
        "Web Payment",
        "Web Publisher",
        "Web Radio",
        "Web Source",
        "Web User",
        "Year",
    )
#====================================================================

class MediaMonkey(eg.PluginBase):
    workerThread = None
    workerThread2 = None
    text = Text

    def __init__(self):
        group = self.AddGroup(
            self.text.mainGrpName,
            self.text.mainGrpDescr
        )
        group.AddAction(Start)
        group.AddAction(Exit)
        group.AddAction(Play)
        group.AddAction(TogglePlay)
        group.AddAction(DiscretePause)
        group.AddAction(Stop)
        group.AddAction(Next)
        group.AddAction(Previous)
        group.AddAction(LoadPlaylist)
        group.AddAction(LoadPlaylistByFilter)
        group.AddAction(LoadPlaylistBySql)
        group.AddAction(AddCurrentSongToPlaylist)
        group.AddAction(RemoveCurrentSongFromPlaylist)
        group.AddAction(RemoveCurrentSongFromNowPlaying)
        group.AddAction(Jukebox)
        group.AddAction(SongJukebox)
        group.AddAction(SendKeys)

        group = self.AddGroup(
            self.text.levelGrpName,
            self.text.levelGrpDescr
        )
        group.AddAction(ToggleMute)
        group.AddAction(SetVolume)
        group.AddAction(VolumeUp)
        group.AddAction(VolumeDown)
        group.AddAction(SetBalance)
        group.AddAction(SetRepeat)
        group.AddAction(SetShuffle)
        group.AddAction(SetAutoDJ)
        group.AddAction(SetCrossfade)
        group.AddAction(BalanceRight)
        group.AddAction(BalanceLeft)
        group.AddAction(Seek)

        group = self.AddGroup(
            self.text.extrGrpName,
            self.text.extrGrpDescr
        )
        group.AddAction(WritingToMM)

        group = self.AddGroup(
            self.text.infoGrpName,
            self.text.infoGrpDescr
        )
        group.AddAction(GetBasicStatistics)
        group.AddAction(GetNotAccessibleTracks)
        group.AddActionsFromList(ACTIONS)
        group.AddAction(GetStatus)
        group.AddActionsFromList(ACTIONS2)
        group.AddAction(GetDetailSongInfo)
        group.AddAction(GetClassificationInfo)
        group.AddAction(GetTechnicalSongInfo)
        group.AddAction(GetUniversal)

    def __start__(self, trigger = True):
        self.volume=None
        self.muted=False
        self.trigger = trigger
        eg.Bind("Main.MM_finishing",self.StopThreads)

        
    def checkWorkerThread(self):
        if not self.workerThread:
            self.workerThread = MediaMonkeyWorkerThread(self)
            self.workerThread.Start(100.0)
        return True
        
    def Configure(self, trigger = True):
        panel = eg.ConfigPanel(self)
        triggerEventsCtrl = wx.CheckBox(panel, -1, '  '+Text.triggerEvents)
        triggerEventsCtrl.SetValue(trigger)
        #triggerEventsCtrl.SetToolTip(wx.ToolTip(self.text.triggerEventsToolTip % (LoadPlaylist.name,AddCurrentSongToPlaylist.name)))
        staticToolTip = wx.StaticText(panel,-1,self.text.triggerEventsToolTip % (LoadPlaylist.name,AddCurrentSongToPlaylist.name))
        #staticToolTip.Enable(False)
        panel.AddCtrl(triggerEventsCtrl)
        panel.AddCtrl(staticToolTip)

        while panel.Affirmed():
            panel.SetResult(triggerEventsCtrl.GetValue(),
            )
        
    def SendCommand(self, command):
        if self.checkWorkerThread():
            self.workerThread.CallWait(partial(self.workerThread.DoCommand, command),1000)

    def SetValue(self, command, value):
        if self.checkWorkerThread():
            self.workerThread.CallWait(partial(self.workerThread.SetValue, command, value),1000)
            
    def GetValue(self, command):
        if self.checkWorkerThread():
            return self.workerThread.CallWait(partial(self.workerThread.GetValue, command),1000)
        
    def GetSongData(self,index):    
        if self.checkWorkerThread():
            return self.workerThread.CallWait(partial(self.workerThread.GetSongData, index),1000)
        
    def Jubox(self, ID, clear=True,repeat=2,shuffle=2,crossfade=2,stop = True):
        if self.checkWorkerThread():
            self.workerThread.Call(partial(
                self.workerThread.Jubox,
                ID,
                clear,
                repeat,
                shuffle,
                crossfade,
                stop
            ))

    def SongJubox(self, ID,clear=False,stop = True):
        if self.checkWorkerThread():
            self.workerThread.Call(partial(
                self.workerThread.SongJubox,
                ID,
                clear,
                stop
            ))
#        return res,Total

    def DeleteSong(self, ID):
        if self.checkWorkerThread():
            res = self.workerThread.CallWait(partial(
                self.workerThread.DeleteSongFromLibrary,
                ID,
            ),1000)
            return res

    def __stop__(self):
        eg.Unbind("Main.MM_finishing",self.StopThreads)
        self.StopThreads()

    def StopThreads(self,event=None):
        if self.workerThread:
            self.workerThread.Stop()
            self.workerThread = None
        if self.workerThread2:
            self.workerThread2.Stop()
            self.workerThread2 = None
#===============================================================================

class Start(eg.ActionBase):
    name = "Start/Connect MediaMonkey"
    description = "Start or Connect MediaMonkey through COM-API."

    def __call__(self):
        dummy = self.plugin.GetValue('isRepeat')
#===============================================================================

class Exit(eg.ActionBase):
    name = "Exit/Disconnect MediaMonkey"
    description = "Disconnect MediaMonkey, with the option to close it."
    
    def __call__(self,choice=True):
        self.plugin.StopThreads()
        if choice:
            hwnds = MyWindowMatcher()
            if hwnds:
                CloseHwnd(hwnds[0])
            else:
                raise self.Exceptions.ProgramNotRunning

    def Configure(self, choice=True):
        panel = eg.ConfigPanel(self)
        choiceCtrl = wx.CheckBox(panel, -1, self.text.choice_label)
        choiceCtrl.SetValue(choice)
        panel.AddCtrl(choiceCtrl)

        while panel.Affirmed():
            panel.SetResult(choiceCtrl.GetValue())
            
    class text:
        choice_label = "Close MediaMonkey too"
#====================================================================

class Play(eg.ActionBase):
    name = "Play"
    description = "Play."

    def __call__(self):
        self.plugin.SendCommand('Play')
#====================================================================

class TogglePlay(eg.ActionBase):
    name = "Toggle Play"
    description = "Toggles between play and pause."

    def __call__(self):
        if  not self.plugin.GetValue('isPlaying'):
            # Play
            return self.plugin.SendCommand('Play')
        else:
            # Toggle Play/Pause
            return self.plugin.SendCommand('Pause')
#====================================================================

class DiscretePause(eg.ActionBase):
    name = "Discrete Pause"
    description = (
        "Pauses MediaMonkey if it is playing, but won't do anything if "
        "MediaMonkey is already paused."
    )

    def __call__(self):
        if self.plugin.GetValue('isPlaying'):
            if not self.plugin.GetValue('isPaused'):
                return self.plugin.SendCommand('Pause')
#====================================================================

class Stop(eg.ActionBase):
    name = "Stop"
    description = "Stop MediaMonkey Playback."

    def __call__(self):
        return self.plugin.SendCommand('Stop')
#====================================================================

class Next(eg.ActionBase):
    name = "Next"
    description = "Play next track."

    def __call__(self):
        self.plugin.SendCommand('Next')
#====================================================================

class Previous(eg.ActionBase):
    name = "Previous"
    description = "Play previous track."

    def __call__(self):
        if self.plugin.checkWorkerThread():
            self.plugin.workerThread.Call(partial(self.plugin.workerThread.Previous))
#====================================================================

class ToggleMute(eg.ActionBase):
    name = "Toggle Mute"
    description = "Toggle MediaMonkey mute on and off."

    def __call__(self):
        if not self.plugin.muted:
            self.plugin.volume=self.plugin.GetValue('Volume')
            self.plugin.SetValue('Volume',0)
            self.plugin.muted=True
        else:
            self.plugin.SetValue('Volume',self.plugin.volume)
            self.plugin.muted=False
#====================================================================

class SetVolume(eg.ActionBase):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%) from 0 to 100."
        
    def __call__(self, volume=50.00):
        self.plugin.SetValue('Volume',volume/100)
        if volume!=0:
            self.plugin.muted=False

    def GetLabel(self, volume):
        return self.text.label_tree+str(int(volume))+"%"

    def Configure(self, volume=50.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            volume,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

    class text:
        label_tree="Set volume "
        label_conf="Volume Level:"
#====================================================================

class VolumeUp(eg.ActionBase):
    name = "Volume up "
    description = "Increase volume by x%."

    def __call__(self, step=10.0):
        if step>0:
            self.plugin.muted=False
            volume=self.plugin.GetValue('Volume')
            if volume<1:
                if volume>(1-step/100):
                    volume=1
                else:
                    volume+=step/100
                self.plugin.SetValue('Volume',volume)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0,fractionWidth=1)
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

    class text:
        label_tree="Volume up "
        label_conf="Volume step:"
#====================================================================

class VolumeDown(eg.ActionBase):
    name = "Volume down "
    description = "Decrease volume by x%."

    def __call__(self, step=-10.0):
        volume=self.plugin.GetValue('Volume')
        if volume>0:
            if volume<abs(step)/100:
                volume=0
            else:
                volume+=step/100
            self.plugin.SetValue('Volume',volume)

    def GetLabel(self, step):
        return self.text.label_tree+str(abs(int(step)))+"%"

    def Configure(self, step=-10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=0.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

    class text:
        label_tree="Volume down "
        label_conf="Volume step:"
#====================================================================

class SetBalance(eg.ActionBase):
    name = "Set Balance"
    description = "Sets the balance."

    def __call__(self, balance=0.0):
        self.plugin.SetValue('Panning',balance/100)

    def GetLabel(self, balance):
        return self.text.label_tree+str(int(balance))+"%"

    def Configure(self, balance=0.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            balance,
            max=100.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

    class text:
        label_tree="Set balance "
        label_conf = "Balance (-100 ... 100):"
#====================================================================

class SetShuffle(eg.ActionBase):
    name = "Set shuffle tracks"
    description = "Set shuffle tracks mode to on or off."

    def __call__(self, switch=0):
        if switch==0: #
            self.plugin.SetValue('isShuffle',True)
        else: #
            self.plugin.SetValue('isShuffle',False)

    def GetLabel(self, switch):
        return "Set shuffle tracks "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.ShuffleON, self.text.ShuffleOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)

    class text:
        radiobox = "Set shuffle tracks to state ..."
        ShuffleON = "ON"
        ShuffleOFF = "OFF"
#====================================================================

class SetRepeat(eg.ActionBase):
    name = "Set continous playback"
    description = "Turn continuous mode on or off"

    def __call__(self, switch=0):
        if switch==0: #
            self.plugin.SetValue('isRepeat',True)
        else: #
            self.plugin.SetValue('isRepeat',False)

    def GetLabel(self, switch):
        return "Set continous playback "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.RepeatON, self.text.RepeatOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)

    class text:
        radiobox = "Set continous playback to state ..."
        RepeatON = "ON"
        RepeatOFF = "OFF"
#====================================================================

class SetAutoDJ(eg.ActionBase):
    name = "Set AutoDJ"
    description = "Turn the AutoDJ on or off."
    
    def __call__(self, switch=0):
        if switch==0: #
            self.plugin.SetValue('isAutoDJ', True)
        else: #
            self.plugin.SetValue('isAutoDJ', False)

    def GetLabel(self, switch):
        return "Set AutoDJ "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.AutoDJON, self.text.AutoDJOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)
            
    class text:
        radiobox = "Set AutoDJ to state ..."
        AutoDJON = "ON"
        AutoDJOFF = "OFF"
#====================================================================

class SetCrossfade(eg.ActionBase):
    name = "Set Crossfade"
    description = "Sets the crossfade to on or off."

    def __call__(self, switch=0):
        if switch==0: #
            self.plugin.SetValue('isCrossfade', True)
        else: #
            self.plugin.SetValue('isCrossfade', False)

    def GetLabel(self, switch):
        return "Set Crossfade "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.CrossfadeON, self.text.CrossfadeOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)

    class text:
        radiobox = "Set Crossfade to state ..."
        CrossfadeON = "ON"
        CrossfadeOFF = "OFF"
#====================================================================

class BalanceRight(eg.ActionBase):
    name = "Balance Right x%"
    description = "Shift balance to the right x%."

    def __call__(self, step=10.0):
        if step>0:
            balance=self.plugin.GetValue('Panning')
            if balance<1:
                if balance>(1-step/100):
                    balance=1
                else:
                    balance+=step/100
                self.plugin.SetValue('Panning',balance)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

    class text:
        label_tree="Balance right "
        label_conf = "Balance step:"
#====================================================================

class BalanceLeft(eg.ActionBase):
    name = "Balance Left x%"
    description = "Shift balance to the left x%."

    def __call__(self, step=10.0):
        if step>0:
            balance=self.plugin.GetValue('Panning')
            if balance>-1:
                if balance<(step/100-1):
                    balance=-1
                else:
                    balance+=-step/100
                self.plugin.SetValue('Panning',balance)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

    class text:
        label_tree="Balance left "
        label_conf = "Balance step:"
#====================================================================

class Seek(eg.ActionBase):
    name = "Seek Forward or Backward x%"
    description = "Seek Forward or Backward x%."

    def __call__(self, step=10.0, direction=0):
        length=self.plugin.GetValue('CurrentSongLength')
        pos=self.plugin.GetValue('PlaybackTime')
        if direction: #Backward
            if pos>length*step/100:
                self.plugin.SetValue('PlaybackTime',pos-length*step/100)
            else:
                self.plugin.SetValue('PlaybackTime',0)
        else:         #Forward
            if pos<length-length*step/100:
                self.plugin.SetValue('PlaybackTime',pos+length*step/100)
            else:
                self.plugin.SetValue('PlaybackTime',length-500)

    def GetLabel(self, step, direction):
        return self.text.tree_lab1\
            +(self.text.tree_lab2 if direction else self.text.tree_lab3)\
            +" "+str(int(step))+"%"

    def Configure(self, step=10.0, direction=0):
        text=Text
        panel = eg.ConfigPanel(self)
        seekCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0, fractionWidth=1)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.btnForward, self.text.btnBackward],
            style=wx.RA_SPECIFY_ROWS
        )
        panel.AddLabel(self.text.label)
        panel.AddCtrl(seekCtrl)
        radioBox.SetSelection(direction)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(seekCtrl.GetValue(),radioBox.GetSelection())

    class text:
        radiobox = "Seek direction"
        btnForward = "Forward"
        btnBackward = "Backward"
        label = "Seek step (%):"
        tree_lab1 = "Seek "
        tree_lab2 = "backward"
        tree_lab3 = "forward"
#====================================================================

class GetBasicStatistics(eg.ActionBase):
    name = "Get Basic Statistics"
    description = "Get Basic Statistics (number of tracks and albums in the database)."

    def __call__(self,sep=''):
        if self.plugin.checkWorkerThread():
            if sep == '':
                sep = '\n'
            tracks, albums = self.plugin.workerThread.CallWait(partial(self.plugin.workerThread.GetStatistics),60)
            return self.text.tracks % tracks+sep+self.text.albums % albums
        
    def GetLabel(self,sep=''):
        return self.name
        
    def Configure(self,sep=''):
        panel = eg.ConfigPanel(self)
        sepLbl = wx.StaticText(panel,-1,self.plugin.text.sepLabel)
        sepCtrl = wx.TextCtrl(panel,-1,sep)
        sepLbl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        sepCtrl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        mySizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.sizer.Add(mySizer,0,wx.TOP,30)
        mySizer.Add(sepLbl,0,wx.TOP,4)
        mySizer.Add((10,1))
        mySizer.Add(sepCtrl)
        while panel.Affirmed():
            panel.SetResult(sepCtrl.GetValue(),)

    class text():
        tracks = '%s tracks'
        albums ='%s albums'
#====================================================================

class GetNotAccessibleTracks(eg.ActionBase):
    name = "Show/Edit inaccessible tracks"
    description = u'''<rst>**Show/Edit tracks that MediaMonkey cannot access.**

ATTENTION !!! This operation may take several minutes !!!
List of found tracks is exported to selected file.
For each track is recorded song ID, song title and file path. 
You can this file import for example to MS Excel or OOo Calc'''

    frameIsOpen = False

    def __call__(self,path=""):
        if not path:
            path = eg.folderPath.Documents + '\\UnaccessibleTracks.txt'
        if not self.frameIsOpen:
            self.unaccessibleTracksFrame = UnaccessibleTracksFrame(parent = self)
            wx.CallAfter(
                self.unaccessibleTracksFrame.ShowUnaccessibleTracksFrame,
                path,
            )
            self.frameIsOpen = True
        
    def Configure(self, path=''):
        txt = self.text
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        if not path:
            path = eg.folderPath.Documents + '\\UnaccessibleTracks.txt'
        self.path = path
        startFolder = path_split(path)[1]
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.plugin.text.toolTipFolder,
            dialogTitle = self.plugin.text.browseTitle,
            buttonText = eg.text.General.browse,
            fileMask="CSV files (*.csv)|*.csv|"\
                "Text file (*.txt)|*.txt|"\
                "All files (*.*)|*.*",
        )
        filepathCtrl.SetValue(path)        
        openButton = wx.Button(panel, -1, txt.openButton)
        openButton.SetToolTip(wx.ToolTip(txt.baloonBttn % path))
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(filepathCtrl,0,wx.TOP,3)
        sizerAdd(openButton,0,wx.TOP,30)
        
        def onOpenBtnClick(event):
            if not self.frameIsOpen:
                self.unaccessibleTracksFrame = UnaccessibleTracksFrame(parent = self)
                wx.CallAfter(
                    self.unaccessibleTracksFrame.ShowUnaccessibleTracksFrame,
                    filepathCtrl.GetValue(),
                    False
                )
                self.frameIsOpen = True
            event.Skip()

        openButton.Bind(wx.EVT_BUTTON, onOpenBtnClick)
        
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue()
            )    

    class text():
        label1 = "Target file for export:"
        openButton = "Open/create track list file"
        baloonBttn ='''Open dialog to edit file %s.
If this file does not exist, it will first be created.'''
#====================================================================

class GetSomeInfo(eg.ActionBase):
    def __call__(self):
        return self.value[0]*self.plugin.GetValue(self.value[1])
#====================================================================

class GetStatus(eg.ActionBase):
    name = "Get Status"
    description = "Get Player Status (returns string: Playing, Paused or Stopped)."
    
    def __call__(self):
        playing=self.plugin.GetValue('isPlaying')
        paused=self.plugin.GetValue('isPaused')
        if not playing:
            return self.text.stopped
        elif playing and not paused:
            return self.text.playing
        elif playing and paused:
            return self.text.paused
            
    class text():
        playing = "Playing"
        paused = "Paused"
        stopped = "Stopped"
#====================================================================

class GetSongInfo(eg.ActionBase):

    def __call__(self,arrayInfo,sep=''):
        #self.value: 0 ... current track
        #           -1 ... previous track
        #            1 ... next track 
        shuffle = self.plugin.GetValue('isShuffle')
        if not shuffle or self.value == 0:
            SongData,ix = self.plugin.GetSongData(self.value)
            if (SongData,ix)==(None,None):
                return self.text.noData
            if sep == '':
                sep = '\n'
            path=SongData['Path']
            indx=path.rfind("\\")+1
            result=path[:indx]+sep if arrayInfo[0] else ""
            result+=path[indx:]+sep if arrayInfo[1] else ""
            listPropert=(
                "Title",
                "ArtistName",
                "Genre",
                "Rating",
                "AlbumName",
                "DiscNumberStr",
                "TrackOrderStr",
                "AlbumArtistName",
                "Year",
                "Grouping",
                "OriginalYear",
                "Author",
                "Conductor",
                "Comment"
            )
            for propert,cond in zip(listPropert,arrayInfo[2:]):
                result+=SongData[propert]+sep if cond else ""
            if arrayInfo[16]:
                result+=str(ix)+sep
            return result[:-len(sep)]
        else:
            return self.text.shuffleON
            

    def GetLabel(self, arrayInfo,sep=''):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*17,
        sep=''
    ):
        text=dict(zip([item[0] for item in SONG_TABLE_FIELDS],Text.SongTableFields))
        panel = eg.ConfigPanel(self)
        filepathCtrl = wx.CheckBox(panel, -1, self.plugin.text.filepath)
        filepathCtrl.SetValue(arrayInfo[0])
        filenameCtrl = wx.CheckBox(panel, -1, self.plugin.text.filename)
        filenameCtrl.SetValue(arrayInfo[1])
        tracktitleCtrl = wx.CheckBox(panel, -1, text['SongTitle'])
        tracktitleCtrl.SetValue(arrayInfo[2])
        artistCtrl = wx.CheckBox(panel, -1, text['Artist'])
        artistCtrl.SetValue(arrayInfo[3])
        genreCtrl = wx.CheckBox(panel, -1, text['Genre'])
        genreCtrl.SetValue(arrayInfo[4])
        ratingCtrl = wx.CheckBox(panel, -1, text['Rating'])
        ratingCtrl.SetValue(arrayInfo[5])
        albumCtrl = wx.CheckBox(panel, -1, text['Album'])
        albumCtrl.SetValue(arrayInfo[6])
        discCtrl = wx.CheckBox(panel, -1, text['DiscNumber'])
        discCtrl.SetValue(arrayInfo[7])
        trackCtrl = wx.CheckBox(panel, -1, text['TrackNumber'])
        trackCtrl.SetValue(arrayInfo[8])
        albumartistCtrl = wx.CheckBox(panel, -1, text['AlbumArtist'])
        albumartistCtrl.SetValue(arrayInfo[9])
        yearCtrl = wx.CheckBox(panel, -1, text['Year'])
        yearCtrl.SetValue(arrayInfo[10])
        groupingCtrl = wx.CheckBox(panel, -1, text['GroupDesc'])
        groupingCtrl.SetValue(arrayInfo[11])
        origDateCtrl = wx.CheckBox(panel, -1, text['OrigYear'])
        origDateCtrl.SetValue(arrayInfo[12])
        composerCtrl = wx.CheckBox(panel, -1, text['Author'])
        composerCtrl.SetValue(arrayInfo[13])
        conductorCtrl = wx.CheckBox(panel, -1, text['Conductor'])
        conductorCtrl.SetValue(arrayInfo[14])
        commentCtrl = wx.CheckBox(panel, -1, text['Comment'])
        commentCtrl.SetValue(arrayInfo[15])
        seqNumCtrl = wx.CheckBox(panel, -1, self.text.seqNum)
        seqNumCtrl.SetValue(arrayInfo[16])
        sepCtrl = wx.TextCtrl(panel,-1,sep)
        sepCtrl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        sepLabel = wx.StaticText(panel,-1,self.plugin.text.sepLabel)
        sepLabel.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        line = wx.StaticLine(panel, -1, size=(440,-1), style=wx.LI_HORIZONTAL)

        panelSizer = panel.sizer
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        
        bottomSizer.Add(sepLabel,0,wx.TOP,4)
        bottomSizer.Add((10,1))
        bottomSizer.Add(sepCtrl,0)

        leftSizer.Add(tracktitleCtrl,0)
        leftSizer.Add(artistCtrl,0,wx.TOP,10)
        leftSizer.Add(genreCtrl,0,wx.TOP,10)
        leftSizer.Add(albumCtrl,0,wx.TOP,10)
        leftSizer.Add(albumartistCtrl,0,wx.TOP,10)
        leftSizer.Add(groupingCtrl,0,wx.TOP,10)
        leftSizer.Add(composerCtrl,0,wx.TOP,10)
        leftSizer.Add(conductorCtrl,0,wx.TOP,10)
        leftSizer.Add(seqNumCtrl,0,wx.TOP,10)
        rightSizer.Add(filepathCtrl,0)
        rightSizer.Add(filenameCtrl,0,wx.TOP,10)
        rightSizer.Add(yearCtrl,0,wx.TOP,10)
        rightSizer.Add(origDateCtrl,0,wx.TOP,10)
        rightSizer.Add(discCtrl,0,wx.TOP,10)
        rightSizer.Add(trackCtrl,0,wx.TOP,10)
        rightSizer.Add(ratingCtrl,0,wx.TOP,10)
        rightSizer.Add(commentCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panelSizer.Add(mainSizer,0)
        panelSizer.Add(line,0,wx.TOP,10)
        panelSizer.Add(bottomSizer,0,wx.TOP,10)

        while panel.Affirmed():
            arrayInfo=[
                filepathCtrl.GetValue(),
                filenameCtrl.GetValue(),
                tracktitleCtrl.GetValue(),
                artistCtrl.GetValue(),
                genreCtrl.GetValue(),
                ratingCtrl.GetValue(),
                albumCtrl.GetValue(),
                discCtrl.GetValue(),
                trackCtrl.GetValue(),
                albumartistCtrl.GetValue(),
                yearCtrl.GetValue(),
                groupingCtrl.GetValue(),
                origDateCtrl.GetValue(),
                composerCtrl.GetValue(),
                conductorCtrl.GetValue(),
                commentCtrl.GetValue(),
                seqNumCtrl.GetValue()
            ]
            panel.SetResult(
                arrayInfo,
                sepCtrl.GetValue()
            )

    class text:
        seqNum = 'Sequence number in "Now playing" window'
        shuffleON = 'Shuffle is ON !'
        noData = 'No data !'
#====================================================================

class GetDetailSongInfo(eg.ActionBase):
    name = "Get detailed song info"
    description = "Get detailed information about the currently playing song."

    def __call__(self, arrayInfo, sep=''):
        SongData,ix = self.plugin.GetSongData(0)
        listPropert=(
        "Lyricist",
        "BPM",
        "InvolvedPeople",
        "OriginalArtist",
        "OriginalTitle",
        "OriginalLyricist",
        "ISRC",
        "Publisher",
        "Encoder",
        "Copyright"
        )
        if sep == '':
            sep = '\n'
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result += SongData[propert]+sep if cond else ""
        return result[:-len(sep)]

    def GetLabel(self, arrayInfo, sep=''):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*10,
        sep=''
    ):
        text=dict(zip([item[0] for item in SONG_TABLE_FIELDS],Text.SongTableFields))
        panel = eg.ConfigPanel(self)
        lyricistCtrl = wx.CheckBox(panel, -1, text['Lyricist'])
        lyricistCtrl.SetValue(arrayInfo[0])
        BPMCtrl = wx.CheckBox(panel, -1, text['BPM'])
        BPMCtrl.SetValue(arrayInfo[1])
        involvedpeopleCtrl = wx.CheckBox(panel, -1, text['InvolvedPeople'])
        involvedpeopleCtrl.SetValue(arrayInfo[2])
        originalartistCtrl = wx.CheckBox(panel, -1, text['OrigArtist'])
        originalartistCtrl.SetValue(arrayInfo[3])
        originaltitleCtrl = wx.CheckBox(panel, -1, text['OrigTitle'])
        originaltitleCtrl.SetValue(arrayInfo[4])
        originallyricistCtrl = wx.CheckBox(
            panel,
            -1,
            text['OrigLyricist']
        )
        originallyricistCtrl.SetValue(arrayInfo[5])
        ISRCCtrl = wx.CheckBox(panel, -1, text['ISRC'])
        ISRCCtrl.SetValue(arrayInfo[6])
        publisherCtrl = wx.CheckBox(panel, -1, text['Publisher'])
        publisherCtrl.SetValue(arrayInfo[7])
        encoderCtrl = wx.CheckBox(panel, -1, text['Encoder'])
        encoderCtrl.SetValue(arrayInfo[8])
        copyrightCtrl = wx.CheckBox(panel, -1, text['Copyright'])
        copyrightCtrl.SetValue(arrayInfo[9])
        sepCtrl = wx.TextCtrl(panel,-1,sep)
        sepCtrl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        sepLabel = wx.StaticText(panel,-1,self.plugin.text.sepLabel)
        sepLabel.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        line = wx.StaticLine(panel, -1, size=(440,-1), style=wx.LI_HORIZONTAL)

        panelSizer = panel.sizer
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        
        bottomSizer.Add(sepLabel,0,wx.TOP,4)
        bottomSizer.Add((10,1))
        bottomSizer.Add(sepCtrl,0)

        leftSizer.Add(lyricistCtrl,0)
        leftSizer.Add(involvedpeopleCtrl,0,wx.TOP,10)
        leftSizer.Add(originalartistCtrl,0,wx.TOP,10)
        leftSizer.Add(originaltitleCtrl,0,wx.TOP,10)
        leftSizer.Add(originallyricistCtrl,0,wx.TOP,10)
        rightSizer.Add(BPMCtrl,0)
        rightSizer.Add(ISRCCtrl,0,wx.TOP,10)
        rightSizer.Add(publisherCtrl,0,wx.TOP,10)
        rightSizer.Add(encoderCtrl,0,wx.TOP,10)
        rightSizer.Add(copyrightCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panelSizer.Add(mainSizer,0)
        panelSizer.Add(line,0,wx.TOP,10)
        panelSizer.Add(bottomSizer,0,wx.TOP,10)

        while panel.Affirmed():
            arrayInfo=[
                lyricistCtrl.GetValue(),
                BPMCtrl.GetValue(),
                involvedpeopleCtrl.GetValue(),
                originalartistCtrl.GetValue(),
                originaltitleCtrl.GetValue(),
                originallyricistCtrl.GetValue(),
                ISRCCtrl.GetValue(),
                publisherCtrl.GetValue(),
                encoderCtrl.GetValue(),
                copyrightCtrl.GetValue()
            ]
            panel.SetResult(
                arrayInfo,
                sepCtrl.GetValue()
            )
#====================================================================

class GetClassificationInfo(eg.ActionBase):
    name = "Get classification song info"
    description = "Get classification song information about the currently playing song."

    def __call__(self, arrayInfo, sep=''):
        SongData,ix = self.plugin.GetSongData(0)
        listPropert=(
            "Tempo",
            "Mood",
            "Occasion",
            "Quality",
            "Custom1",
            "Custom2",
            "Custom3",
            "Custom4",
            "Custom5"
        )
        if sep == '':
            sep = '\n'
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=SongData[propert]+sep if cond else ""
        return result[:-len(sep)]
        
    def GetLabel(self, arrayInfo, sep=''):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*9,
        sep=''
    ):
        text=dict(zip([item[0] for item in SONG_TABLE_FIELDS],Text.SongTableFields))
        panel = eg.ConfigPanel(self)
        tempoCtrl = wx.CheckBox(panel, -1, text['Tempo'])
        tempoCtrl.SetValue(arrayInfo[0])
        moodCtrl = wx.CheckBox(panel, -1, text['Mood'])
        moodCtrl.SetValue(arrayInfo[1])
        occasionCtrl = wx.CheckBox(panel, -1, text['Occasion'])
        occasionCtrl.SetValue(arrayInfo[2])
        qualityCtrl = wx.CheckBox(panel, -1, text['Quality'])
        qualityCtrl.SetValue(arrayInfo[3])
        custom1Ctrl = wx.CheckBox(panel, -1, text['Custom1'])
        custom1Ctrl.SetValue(arrayInfo[4])
        custom2Ctrl = wx.CheckBox(panel, -1, text['Custom2'])
        custom2Ctrl.SetValue(arrayInfo[5])
        custom3Ctrl = wx.CheckBox(panel, -1, text['Custom3'])
        custom3Ctrl.SetValue(arrayInfo[6])
        custom4Ctrl = wx.CheckBox(panel, -1, text['Custom4'])
        custom4Ctrl.SetValue(arrayInfo[7])
        custom5Ctrl = wx.CheckBox(panel, -1, text['Custom5'])
        custom5Ctrl.SetValue(arrayInfo[8])
        sepCtrl = wx.TextCtrl(panel,-1,sep)
        sepCtrl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        sepLabel = wx.StaticText(panel,-1,self.plugin.text.sepLabel)
        sepLabel.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        line = wx.StaticLine(panel, -1, size=(440,-1), style=wx.LI_HORIZONTAL)
        panelSizer = panel.sizer
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        
        bottomSizer.Add(sepLabel,0,wx.TOP,4)
        bottomSizer.Add((10,1))
        bottomSizer.Add(sepCtrl,0)

        leftSizer.Add(tempoCtrl,0)
        leftSizer.Add(moodCtrl,0,wx.TOP,10)
        leftSizer.Add(occasionCtrl,0,wx.TOP,10)
        leftSizer.Add(qualityCtrl,0,wx.TOP,10)
        rightSizer.Add(custom1Ctrl,0)
        rightSizer.Add(custom2Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom3Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom4Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom5Ctrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panelSizer.Add(mainSizer,0)
        panelSizer.Add(line,0,wx.TOP,10)
        panelSizer.Add(bottomSizer,0,wx.TOP,10)

        while panel.Affirmed():
            arrayInfo=[
                tempoCtrl.GetValue(),
                moodCtrl.GetValue(),
                occasionCtrl.GetValue(),
                qualityCtrl.GetValue(),
                custom1Ctrl.GetValue(),
                custom2Ctrl.GetValue(),
                custom3Ctrl.GetValue(),
                custom4Ctrl.GetValue(),
                custom5Ctrl.GetValue()
            ]
            panel.SetResult(
                arrayInfo,
                sepCtrl.GetValue()
            )
#====================================================================

class GetTechnicalSongInfo(eg.ActionBase):
    name = "Get technical song info"
    description = "Get technical information about the currently playing song. (song length, bitrate, etc.)"

    def __call__(self, arrayInfo, sep=''):
        SongData,ix = self.plugin.GetSongData(0)
        listPropert=(
            "SongLength",
            "FileLength",
            "Bitrate",
            "VBR",
            "SampleRate",
            "Channels",
            "PlayCounter",
            "Leveling",
            "LastPlayed"
        )
        if sep == '':
            sep = '\n'
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=SongData[propert]+sep if cond else ""
        return result[:-len(sep)]

    def GetLabel(self, arrayInfo, sep=''):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*9,
        sep=''
    ):
        text=dict(zip([item[0] for item in SONG_TABLE_FIELDS],Text.SongTableFields))
        panel = eg.ConfigPanel(self)
        lengthCtrl = wx.CheckBox(panel, -1, text['SongLength'])
        lengthCtrl.SetValue(arrayInfo[0])
        filesizeCtrl = wx.CheckBox(panel, -1, text['FileLength'])
        filesizeCtrl.SetValue(arrayInfo[1])
        bitrateCtrl = wx.CheckBox(panel, -1, text['Bitrate'])
        bitrateCtrl.SetValue(arrayInfo[2])
        VBRCtrl = wx.CheckBox(panel, -1, text['VBR'])
        VBRCtrl.SetValue(arrayInfo[3])
        frequencyCtrl = wx.CheckBox(panel, -1, text['SamplingFrequency'])
        frequencyCtrl.SetValue(arrayInfo[4])
        stereoCtrl = wx.CheckBox(panel, -1, text['Stereo'])
        stereoCtrl.SetValue(arrayInfo[5])
        counterCtrl = wx.CheckBox(panel, -1, text['PlayCounter'])
        counterCtrl.SetValue(arrayInfo[6])
        levelingCtrl = wx.CheckBox(panel, -1, text['NormalizeTrack'])
        levelingCtrl.SetValue(arrayInfo[7])
        lastplayedCtrl = wx.CheckBox(panel, -1, text['LastTimePlayed'])
        lastplayedCtrl.SetValue(arrayInfo[8])
        sepCtrl = wx.TextCtrl(panel,-1,sep)
        sepCtrl.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        sepLabel = wx.StaticText(panel,-1,self.plugin.text.sepLabel)
        sepLabel.SetToolTip(wx.ToolTip(self.plugin.text.sepToolTip))
        line = wx.StaticLine(panel, -1, size=(440,-1), style=wx.LI_HORIZONTAL)
#        seekableCtrl = wx.CheckBox(panel, -1, text.seekable)
#        seekableCtrl.SetValue(seekable)
#        copyrightedCtrl = wx.CheckBox(panel, -1, text.copyrighted)
#        copyrightedCtrl.SetValue(copyrighted)
#        originalCtrl = wx.CheckBox(panel, -1, text.original)
#        originalCtrl.SetValue(original)
        panelSizer = panel.sizer
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        bottomSizer.Add(sepLabel,0,wx.TOP,4)
        bottomSizer.Add((10,1))
        bottomSizer.Add(sepCtrl,0)
        leftSizer.Add(lengthCtrl,0)
        leftSizer.Add(bitrateCtrl,0,wx.TOP,10)
        leftSizer.Add(frequencyCtrl,0,wx.TOP,10)
        leftSizer.Add(counterCtrl,0,wx.TOP,10)
        leftSizer.Add(lastplayedCtrl,0,wx.TOP,10)
        rightSizer.Add(filesizeCtrl,0)
        rightSizer.Add(VBRCtrl,0,wx.TOP,10)
        rightSizer.Add(stereoCtrl,0,wx.TOP,10)
        rightSizer.Add(levelingCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panelSizer.Add(mainSizer,0)
        panelSizer.Add(line,0,wx.TOP,10)
        panelSizer.Add(bottomSizer,0,wx.TOP,10)
#        panel.AddCtrl(seekableCtrl)
#        panel.AddCtrl(copyrightedCtrl)
#        panel.AddCtrl(originalCtrl)

        while panel.Affirmed():
            arrayInfo=[
                lengthCtrl.GetValue(),
                filesizeCtrl.GetValue(),
                bitrateCtrl.GetValue(),
                VBRCtrl.GetValue(),
                frequencyCtrl.GetValue(),
                stereoCtrl.GetValue(),
                counterCtrl.GetValue(),
                levelingCtrl.GetValue(),
                lastplayedCtrl.GetValue(),
#                seekableCtrl.GetValue(),
#                copyrightedCtrl.GetValue(),
#                originalCtrl.GetValue(),
            ]
            panel.SetResult(
                arrayInfo,
                sepCtrl.GetValue()
            )

    class text:
        length = "Length"
        filesize = "File size"
        bitrate = "Bitrate"
        VBR = "VBR"
        frequency = "Frequency"
        stereo = "Stereo"
        counter = "Play counter"
        leveling = "Leveling"
        lastplayed = "Last played"
#        seekable = "Seekable"
#        copyrighted = "Copyrighted"
#        original = "Original"
#====================================================================

class GetUniversal(eg.ActionBase):
    name = "Get Universal"
    description = "Get any one piece of information about the currently playing song."

    def __call__(self, field):
        SongData,ix = self.plugin.GetSongData(0)
        tmpList = [tpl[2] for tpl in SONG_TABLE_FIELDS]
        return SongData[tmpList[field]]

    def GetLabel(self, field):
        return self.text.get % Text.SongTableFields[field]
    
    def Configure(self, field=-1):
        choices = filter(lambda i: i[0]!="",zip(
            [tpl[2] for tpl in SONG_TABLE_FIELDS],
            Text.SongTableFields
        ))
        choices = [item[1] for item in choices]
        choices.sort()
        panel=eg.ConfigPanel(self)
        panel.AddLabel(self.text.label)
        infoCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        if field > -1:
            infoCtrl.SetStringSelection(Text.SongTableFields[field])
        panel.AddCtrl(infoCtrl)
        
        while panel.Affirmed():
            panel.SetResult(Text.SongTableFields.index(infoCtrl.GetStringSelection()))

    class text:
        label="Select requested property:"
        get = "Get %s"
#====================================================================

class WritingToMM(eg.ActionBase):
    name = "Write to MM database"
    description = "Write specific tags (mood etc) to currently playing song."

    def __init__(self):
        text=self.text
        self.listCtrl=(
            "wx.TextCtrl(panel, -1, value)",
            (
                "eg.SpinNumCtrl(panel,-1,value,max=100.0,min=0.0,"
                "fractionWidth=1,increment=10,style=wx.TE_READONLY)"
            )
        )
        self.propertiesList=(
            ("Tempo",0,False),
            ("Mood",0,False),
            ("Occasion",0,False),
            ("Quality",0,False),
            ("Custom1",0,False),
            ("Custom2",0,False),
            ("Custom3",0,False),
            ("Custom4",0,False),
            ("Custom5",0,False),
            ("Comment",0,True),
            ("Genre",0,True),
            ("Rating",1,True),
        )
        
    def __call__(self, i, arrayValue0, arrayValue1):
        ndx = [itm[0] for itm in self.propertiesList].index([it[0] for it in SONG_TABLE_FIELDS][i])
        tmpList=[]
        attrib = [itm[2] for itm in SONG_TABLE_FIELDS][i]
        if self.plugin.checkWorkerThread():
            self.plugin.workerThread.CallWait(partial(
                self.plugin.workerThread.WriteToMMdatabase,
                attrib,
                arrayValue0[ndx],
                arrayValue1[ndx]
            ))

    def GetLabel(self, i, arrayValue0, arrayValue1):
        ndx = [itm[0] for itm in self.propertiesList].index([it[0] for it in SONG_TABLE_FIELDS][i])
        lbl = Text.SongTableFields[i]
        itm2 = arrayValue0[ndx] if (self.propertiesList[ndx][1] == 0) else str(int(arrayValue0[ndx]))
        result = self.text.set % (lbl, itm2)
        if arrayValue1[ndx]:
            result += " (+ID3)"
        return result

    def Configure(
        self,
        i=-1,
        arrayValue0=[
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            50,
        ],
        arrayValue1 = [False] * 12
    ):
        arrayVal0 = arrayValue0[:]
        arrayVal1 = arrayValue1[:]
        choices=[]
        for item in self.propertiesList:
            indx = [ix[0] for ix in SONG_TABLE_FIELDS].index(item[0])
            choices.append(Text.SongTableFields[indx])
        choices.sort()
        panel = eg.ConfigPanel(self)
        choiceLbl=wx.StaticText(panel, -1, self.text.label)
        choiceCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        choiceCtrl.SetStringSelection(Text.SongTableFields[i])
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        choiceSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        choiceSizer.Add(choiceLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(choiceCtrl, 0, wx.EXPAND)
        mainSizer.Add(choiceSizer, 0, wx.EXPAND|wx.ALL, 10)
        dynSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        mainSizer.Add(dynSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
        panel.sizer.Add(mainSizer)

        def onChoiceChange(event=None):
            dynSizer.Clear(True)
            dynLbl = wx.StaticText(
                panel,
                -1,
                choiceCtrl.GetStringSelection()+":"
            )
            ix = Text.SongTableFields.index(choiceCtrl.GetStringSelection())
            field = SONG_TABLE_FIELDS[ix][0]
            ndx = [item[0] for item in self.propertiesList].index(field)
            line = self.propertiesList[ndx][1]
            value = arrayVal0[ndx]
            dynCtrl = eval(self.listCtrl[line])
            dynSizer.Add(dynLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            dynSizer.Add(dynCtrl, 0, wx.EXPAND)
            if self.propertiesList[ndx][2]:
                chkBoxCtrl = wx.CheckBox(panel, label=self.text.checkboxlabel)
                chkBoxCtrl.SetValue(arrayVal1[ndx])
                dynSizer.Add((5,5))
                dynSizer.Add(chkBoxCtrl, 0, wx.EXPAND)
            mainSizer.Layout()
            if event:
                event.Skip()

        choiceCtrl.Bind(wx.EVT_CHOICE, onChoiceChange)
        if i> -1:
            ndx = [itm[0] for itm in self.propertiesList].index([it[0] for it in SONG_TABLE_FIELDS][i])
            onChoiceChange()

        while panel.Affirmed():
            ix = Text.SongTableFields.index(choiceCtrl.GetStringSelection())
            field = SONG_TABLE_FIELDS[ix][0]
            ndx = [item[0] for item in self.propertiesList].index(field)
            arrayVal0[ndx] = dynSizer.GetChildren()[1].GetWindow().GetValue()
            if self.propertiesList[ndx][2]:
                arrayVal1[ndx] = dynSizer.GetChildren()[3].GetWindow().GetValue()
                 
            panel.SetResult(ix, arrayVal0, arrayVal1 )

    class text:
        label="Select requested property:"
        set = "Set %s = %s"
        checkboxlabel = "Make entry to ID3 tag too"
#====================================================================

class LoadPlaylist(eg.ActionBase):
    name = "Load Playlist by Name"
    description = "Loads a MediaMonkey playlist defined by name."

    def __call__(self, plString, repeat, shuffle, crossfade, clear):
        if not self.plugin.workerThread2:
            self.plugin.workerThread2 = MediaMonkeyWorkerThread(self.plugin)
            self.plugin.workerThread2.Start(100.0)
        args = (
            self.plugin.workerThread2.LoadPlaylistByTitle,
            plString,
            repeat,
            shuffle,
            crossfade,
            clear
        )
        self.plugin.workerThread2.Call(partial(*args))

    def Configure(self, plString="",repeat=2,shuffle=2,crossfade=2, clear = True):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString)
        repeatChkBoxCtrl = wx.CheckBox(panel, label=Text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=Text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=Text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        clearPlaylistChkBoxCtrl = wx.CheckBox(panel, label=Text.clearPlaylist)
        clearPlaylistChkBoxCtrl.SetValue(clear)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        bottmSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottmSizer.Add(leftSizer,2,wx.EXPAND)
        SizerAdd(bottmSizer,0,wx.EXPAND)
        leftSizer.Add(repeatChkBoxCtrl,0,wx.TOP,15,)
        leftSizer.Add(shuffleChkBoxCtrl,0,wx.TOP,15)
        leftSizer.Add(crossfadeChkBoxCtrl,0,wx.TOP,15)
        leftSizer.Add(clearPlaylistChkBoxCtrl,0,wx.TOP,15)
        
        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue(),
                clearPlaylistChkBoxCtrl.GetValue(),
            )

    class text:
        playlistName = "Playlist name:"
        found = "found (%s songs)"
        noFound = "not found or empty"
#====================================================================

class AddCurrentSongToPlaylist(eg.ActionBase):
    name = "Add currently playing song to playlist"
    description = "Adds the currently playing song to a specific playlist."

    def __call__(self, plString, skip):
        if self.plugin.checkWorkerThread():
            args = (
                self.plugin.workerThread.AddSongToPlaylist,
                plString,
                skip
            )
            self.plugin.workerThread.Call(partial(*args))

    def Configure(self, plString="", skip=False):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                skipChkBoxCtrl.GetValue(),
            )

    class text:
        playlistName = "Playlist name:"
        skip = "Skip to next track"
#====================================================================

class RemoveCurrentSongFromPlaylist(eg.ActionBase):
    name = "Remove current playing song from Playlist"
    description = "Remove the currently playing song from a specific playlist."

    def __call__(self, plString, skip, now_pl):
        if self.plugin.checkWorkerThread():
            args = (
                self.plugin.workerThread.RemoveSongFromPlaylist,
                plString,
                skip,
                now_pl
            )
            self.plugin.workerThread.Call(partial(*args))

    def Configure(self, plString="", skip=False, now_pl=False):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)
        now_plChkBoxCtrl = wx.CheckBox(panel, label=self.text.now_pl)
        now_plChkBoxCtrl.SetValue(now_pl)
        SizerAdd(now_plChkBoxCtrl,0,wx.TOP,15,)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                skipChkBoxCtrl.GetValue(),
                now_plChkBoxCtrl.GetValue(),
            )

    class text:
        playlistName = "Playlist name:"
        skip = "Skip to next track"
        now_pl='Remove track from "Now playing" window too'
#====================================================================

class RemoveCurrentSongFromNowPlaying(eg.ActionBase):
    name = "Remove currently playing song from Now Playing playlist"
    description = "Remove the currently playing song from Now Playing playlist."

    def __call__(self, skip):
        if self.plugin.checkWorkerThread():
            self.plugin.workerThread.Call(partial(
                    self.plugin.workerThread.RemoveSongFromNowPlaying,
                    skip
                ))
            
    def Configure(self, skip=False):
        panel = eg.ConfigPanel(self)
        text = self.text
        SizerAdd = panel.sizer.Add
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)

        while panel.Affirmed():
            panel.SetResult(
                skipChkBoxCtrl.GetValue(),
            )

    class text:
        skip = "Skip to next track"
#====================================================================

class LoadPlaylistByFilter(eg.ActionBase):
    name = "Load Playlist by Filter"
    description = "Loads a MediaMonkey playlist defined by filter (SQL query)."

    def __init__(self):
        self.myDirty=None

        self.unitList=(
           # "seconds",
            "minutes",
            "hours",
            "days",
            "months",
            "years"
        )

        self.trendList=(
            "asc",
            "desc"
        )

        self.exprList1=(
            "equal",
            "notEqual",
            "greater",
            "greatOrEqual",
            "less",
            "lowerOrEqual",
            "beforeLess",
            "beforeMore",
        )

        self.exprList=[
            "equal",
            "notEqual",
            "greater",
            "greatOrEqual",
            "less",
            "lowerOrEqual",
            "startsWith",
            "notStartsWith",
            "endsWith",
            "notEndsWith",
            "includes",
            "notIncludes",
            "isEmpty",
            "isNotEmpty",
        ]

    def __call__(
        self,
        plName,
        mode,
        listRules,
        order,
        trend,
        crit,
        limit,
        random,
        num,
        repeat,
        shuffle,
        crossfade,
        clear,
    ):
        if not self.plugin.workerThread2:
            self.plugin.workerThread2 = MediaMonkeyWorkerThread(self.plugin)
            self.plugin.workerThread2.Start(100.0)
        args = (
            self.plugin.workerThread2.LoadFilterPlaylist,
            plName,
            mode,
            listRules,
            order,
            trend,
            crit,
            limit,
            random,
            num,
            repeat,
            shuffle,
            crossfade,
            clear,
            self.unitList,
            self.trendList
  )
        self.plugin.workerThread2.Call(partial(*args))

    def Configure(
        self,
        plName="",
        mode=0,
        listRules=[[-1,-1,u""]],
        order=False,
        trend=0,
        crit=0,
        limit=False,
        random=False,
        num="100",
        repeat=2,
        shuffle=2,
        crossfade=2,
        clear=True,
    ):
        text = self.text
        def validityCheck():
            if CheckEnable:
                flag=True
                for i in range(0,self.i):
                    choice0=listRules2[i][0]
                    choice1=listRules2[i][1]
                    if choice0<0 or choice1<0:
                        flag=False
                        break
                    else:
                        if SONG_TABLE_FIELDS[choice0][1] <> "D":
                            if choice1 < 12 and listRules2[i][2]==u"":
                                flag=False
                                break
                        else:
                            #if choice1>5 and wx.FindWindowById(i+150).GetValue()<1:
                            if choice1>5 and int(listRules2 [i][2][:-1])<1:
                                flag=False
                                break
                if not self.myDirty:
                    panel.SetIsDirty(True)
                    myDirty=True
                panel.EnableButtons(flag)

        choices = list(Text.SongTableFields)
        choicesS=choices[:]
        choicesS.sort()
        
        listRules2=[] #working copy (after Cancel flush it)
        for i in range(0,len(listRules)):
            listRules2.append(listRules[i][:])
        maxRules=10
        panel = eg.ConfigPanel(self)
        panel.sizer.SetMinSize((560, 110+29*maxRules))
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.radioboxMode,
            choices=[text.modeAnd, text.modeOr],
            style=wx.RA_SPECIFY_COLS
        )
        radioBoxMode.SetMinSize((556,43))
        radioBoxMode.SetSelection(mode)
        nameCtrl = wx.TextCtrl(panel, -1, plName,size=(100,22))
        orderChkBoxCtrl = wx.CheckBox(panel, label="")
        orderChkBoxCtrl.SetValue(order)
        dirTxt1=wx.StaticText(panel, -1, self.text.order1)
        trends=[eval("self.text."+tpl) for tpl in self.trendList]
        dirCtrl=wx.Choice(panel, -1, choices=trends,size=(-1, -1))
        dirCtrl.SetSelection(trend)
        dirTxt2=wx.StaticText(panel, -1, self.text.order2)
        critCtrl=wx.Choice(panel, -1, choices=choicesS,size=(-1, -1))
        critCtrl.SetStringSelection(choices[crit])
        limitChkBoxCtrl = wx.CheckBox(panel, label="")
        limitChkBoxCtrl.SetValue(limit)
        limitTxt1=wx.StaticText(panel, -1, self.text.limit1)
        numCtrl = masked.NumCtrl(
            panel, -1, num,
            min=1,integerWidth=6,
            allowNegative=False,groupDigits=False)
        limitTxt2=wx.StaticText(panel, -1, self.text.limit2+10*' ')
        randomChkBoxCtrl = wx.CheckBox(panel,  label=Text.random)
        randomChkBoxCtrl.SetToolTip(wx.ToolTip(Text.randomToolTip % Text.shuffle))
        randomChkBoxCtrl.SetValue(random)
        repeatChkBoxCtrl = wx.CheckBox(panel, label=Text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=Text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=Text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        clearPlaylistChkBoxCtrl = wx.CheckBox(panel, label=Text.clearPlaylist)
        clearPlaylistChkBoxCtrl.SetValue(clear)

        self.mySizer = wx.GridBagSizer(vgap=8,hgap=10)
        self.mySizer.SetMinSize((560, 6+29*maxRules))
        statBox_1 = wx.StaticBox(panel, -1, "")
        statBox_2 = wx.StaticBox(panel, -1, "")
        stBoxSizer = wx.StaticBoxSizer(statBox_1, wx.VERTICAL)
        stBoxSizer.SetMinSize((426,-1))
        rightSizer = wx.StaticBoxSizer(statBox_2, wx.VERTICAL)
        rightSizer.SetMinSize((120,69))
        orderSizer=wx.BoxSizer(wx.HORIZONTAL)
        limitSizer=wx.BoxSizer(wx.HORIZONTAL)        
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        lrSizer =wx.BoxSizer(wx.HORIZONTAL)
        bottmSizer = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=40)

        rightSizer.Add(wx.StaticText(panel, -1, text.filterName),0,wx.LEFT|wx.TOP,4)
        rightSizer.Add(nameCtrl, 0,wx.LEFT|wx.TOP,4)
        rightSizer.Add((1,12))
        orderSizer.Add(orderChkBoxCtrl,0,wx.TOP,4)
        orderSizer.Add(dirTxt1,0,wx.LEFT|wx.TOP,4)
        orderSizer.Add(dirCtrl,0,wx.LEFT,4)
        orderSizer.Add(dirTxt2,0,wx.LEFT|wx.TOP,4)
        orderSizer.Add(critCtrl,0,wx.LEFT,4)
        limitSizer.Add(limitChkBoxCtrl,0,wx.TOP,4)
        limitSizer.Add(limitTxt1,0,wx.LEFT|wx.TOP,4)
        limitSizer.Add(numCtrl, 0,wx.LEFT,4)
        limitSizer.Add(limitTxt2,0,wx.LEFT|wx.TOP,4)
        limitSizer.Add(randomChkBoxCtrl,0,wx.TOP,4)
        stBoxSizer.Add(limitSizer,0,wx.TOP,8)
        stBoxSizer.Add(orderSizer,0,wx.TOP,4)
        bottmSizer.Add(repeatChkBoxCtrl,0,wx.LEFT,5)
        bottmSizer.Add(shuffleChkBoxCtrl,0)
        bottmSizer.Add(crossfadeChkBoxCtrl,0,wx.LEFT,5)
        bottmSizer.Add(clearPlaylistChkBoxCtrl,0)
        leftSizer.Add(stBoxSizer,0)
        #leftSizer.Add(bottmSizer,0,wx.TOP,10)
        lrSizer.Add(leftSizer)
        lrSizer.Add(rightSizer,0,wx.LEFT,10)
        panel.sizer.Add(radioBoxMode, 0)
        panel.sizer.Add(self.mySizer, 0,wx.TOP,10)
        panel.sizer.Add(lrSizer)
        panel.sizer.Add(bottmSizer,0,wx.TOP,10)

        def CreateExprCtrl(row):
#Called from:	 AddRow,UpdateChoiceExpr
            if SONG_TABLE_FIELDS[listRules2[row][0]][1]=="D": # Date & Time
                choicExpr=[eval("self.text."+tpl) for tpl in self.exprList1]
            else:
                choicExpr=[eval("self.text."+tpl) for tpl in self.exprList]
            exprCtrl=wx.Choice(panel, row+100, choices=choicExpr,size=(182, 22))
            exprCtrl.SetSelection(listRules2[row][1])
            exprCtrl.Bind(wx.EVT_CHOICE, OnExprChoice)
            self.mySizer.Add(exprCtrl,(row,1))
            self.mySizer.Layout()

        def ConvToWxDt(dt):
#Called from: CreateStrCtrl, UpdateStr
            """Conversion of data record to wx.DateTime format."""
            wxDttm=wx.DateTime()
            wxDttm.Set(int(dt[8:10]),int(dt[5:7])-1,int(dt[:4]))
            return wxDttm

        def CreateStrCtrl(row):
#Called from: UpdateStr, AddRow
            tp=SONG_TABLE_FIELDS[listRules2[row][0]][1]
            if tp<>"D":
                strCtrl=wx.TextCtrl(panel, row+150, "",size=(168, 22))
                strCtrl.Bind(wx.EVT_TEXT, OnStrChange)
                strCtrl.SetValue(listRules2[row][2])
                if listRules2[row][1]>11:
                    strCtrl.Enable(False)
                infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                infoSizer.Add(strCtrl)
            else: # Date & Time Ctrl
                if listRules2[row][1]<6: #for absolute date/time type
                    clndrCtrl=wx.DatePickerCtrl(panel,row+150, size=(85,22),
                        style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    clndrCtrl.SetRange(ConvToWxDt('1900-01-01'),ConvToWxDt('2050-12-31'))
                    clndrCtrl.SetValue(ConvToWxDt(listRules2[row][2]))
                    clndrCtrl.Bind(wx.EVT_DATE_CHANGED, OnClndrChange)
                    infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                    infoSizer.Add(clndrCtrl)
                    spinBtn = wx.SpinButton(panel,row+250, wx.DefaultPosition, (-1,22), wx.SP_VERTICAL )
                    timeCtrl = masked.TimeCtrl(
                        panel, row+200, name="24hrCtrl", fmt24hr=True,
                        spinButton=spinBtn
                        )
                    timeCtrl.SetValue(listRules2[row][2][11:])
                    timeCtrl.Bind(masked.EVT_TIMEUPDATE, OnTimeChange )
                    infoSizer.Add(timeCtrl,0,wx.LEFT,2)
                    infoSizer.Add(spinBtn)
                else: #for time  relative (NOW) type
                    periodCtrl = masked.NumCtrl(
                        panel, row+150, num,
                        size=(85,22),min=1,integerWidth=9,
                        allowNegative=False,groupDigits=False,
                        autoSize=False,invalidBackgroundColour = "White",)
                    #periodCtrl.Bind(masked.EVT_NUM, OnPeriodChange)
                    periodCtrl.Bind(wx.EVT_TEXT, OnPeriodChange) #Otherwise problem with Dirty flag !
                    periodCtrl.SetValue(int(listRules2[row][2][:-1]))
                    infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                    infoSizer.Add(periodCtrl)
                    choicUnit=[eval("self.text."+tpl) for tpl in self.unitList]
                    unitCtrl=wx.Choice(panel, row+200, choices=choicUnit,size=(81, 22))
                    unitCtrl.SetSelection(int(listRules2[row][2][-1]))
                    unitCtrl.Bind(wx.EVT_CHOICE, OnUnitChoice)
                    infoSizer.Add(unitCtrl,0,wx.LEFT,2)
            self.mySizer.Add(infoSizer,(row,2))
            self.mySizer.Layout()

        def AddRow(x):
#Called from: OnAddButton, Main
            propertCtrl=wx.Choice(panel,x+50 , choices=choicesS,size=(132, 22))
            propertCtrl.Bind(wx.EVT_CHOICE, OnPropertChoice)
            self.mySizer.Add(propertCtrl,(x,0))
            CreateExprCtrl(x)
            CreateStrCtrl(x)
            btnAdd = wx.Button(panel, x, "+",size=(22, 22))
            btnAdd.Bind(wx.EVT_BUTTON,OnAddButton)
            btnRemove = wx.Button(panel, x, "-",size=(22, 22))
            btnRemove.Bind(wx.EVT_BUTTON,OnRemoveButton)
            self.mySizer.Add(btnAdd,(x,3))
            self.mySizer.Add(btnRemove,(x,4),flag=wx.LEFT,border=-10)
            self.mySizer.Layout()

        def UpdateChoiceExpr(row):
#Called from: updateRow, OnPropertChoice
            cnt=self.mySizer.FindItemAtPosition((row,1)).GetWindow().GetCount()
            tp=SONG_TABLE_FIELDS[listRules2[row][0]][1]
            myWnd=wx.FindWindowById(row+100)
            if cnt==0 or (tp=="D" and cnt==14) or (tp<>"D" and cnt<>14):
                self.mySizer.Detach(myWnd)
                myWnd.Destroy()
                CreateExprCtrl(row)
            else:
                myWnd.SetSelection(listRules2[row][1])

        def UpdateStr(row):
#Called from: updateRow, OnPropertChoice, OnExprChoice
            infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
            lng=len(infoSizer.GetChildren()) # old column 2 type markant
            tp=SONG_TABLE_FIELDS[listRules2[row][0]][1]
            tp2=listRules2[row][1]
            flag=False
            #First: Destroy old Ctrl(s)
            if tp=="D":
                if lng==1:
                    rng=(0,)
                    flag=True
                elif lng==2 and tp2<6 :
                    rng=(1,0)
                    flag=True
                elif lng==3 and tp2>5:
                    rng=(2,1,0)
                    flag=True
            else: #tp<>"D"
                if lng==2:
                    rng=(1,0,)
                    flag=True
                elif lng==3:
                    rng=(2,1,0)
                    flag=True
            if flag: #  update panel and value
                for indx in rng:
                    wnd=infoSizer.GetChildren()[indx].GetWindow()
                    infoSizer.Detach(wnd)
                    wnd.Destroy()
                self.mySizer.Detach(infoSizer)
                infoSizer.Destroy()
                #Second: Create new Ctrl(s)
                CreateStrCtrl(row) #Create and update value
            else: # update only value
                val=listRules2[row][2]
                wnd1=wx.FindWindowById(row+150)
                wnd2=wx.FindWindowById(row+200)
                if lng==1:
                    wnd1.SetValue(val)
                    if tp2>11:
                        wnd1.Enable(False)
                    else:
                        wnd1.Enable(True)
                else:
                    if tp2<6: # absolute date/time
                        wnd1.SetValue(ConvToWxDt(val))
                        wnd2.SetValue(val[11:])
                    else: # relative date/time
                        wnd1.SetValue(int(val[:-1]))
                        wnd2.SetSelection(int(val[-1]))

        def updateRow(row):
#Called from: OnAddButton, OnRemoveButton, Main
            if listRules2[row][0] > -1:
                wx.FindWindowById(row+50).SetStringSelection(choices[listRules2[row][0]])
            UpdateChoiceExpr(row)
            UpdateStr(row)

        def OnPropertChoice(evt):
            row=evt.GetId()-50
            field = wx.FindWindowById(evt.GetId()).GetStringSelection()
            listRules2[row][0]=choices.index(field)
            infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
            lng=len(infoSizer.GetChildren()) # old column 2 type markant
            tp=SONG_TABLE_FIELDS[listRules2[row][0]][1]
            cnt=self.mySizer.FindItemAtPosition((row,1)).GetWindow().GetCount()
            flg=False
            if tp=="D" and cnt==14: # change to absolute date/time format
                listRules2[row][2]=str(datetime.datetime.today())[:11]+'00:00:00'
                flg=True
            elif tp<>"D" and cnt<>14: #change to no date/time (single column) format
                listRules2[row][2]=""
                flg=True
            if flg: # set selection Expr to "no selection"
                listRules2[row][1]=-1
                wx.FindWindowById(row+100).SetSelection(-1)
            UpdateChoiceExpr(row)
            UpdateStr(row)
            validityCheck()

        def OnExprChoice(evt):
            row=evt.GetId()-100
            value=wx.FindWindowById(evt.GetId()).GetSelection() #
            listRules2[row][1]=value
            #enable=False if value>11 else True
            wnd=wx.FindWindowById(row+150)
            if SONG_TABLE_FIELDS[listRules2[row][0]][1]<>"D":
                if value>11:
                    wnd.Enable(False)
                    wnd.Clear()
                else:
                    wnd.Enable(True)
            else: # date/time format
                infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
                lng=len(infoSizer.GetChildren())
                if lng==2 and value<6:
                    listRules2[row][2]=str(datetime.datetime.today())[:11]+'00:00:00'
                elif lng==3 and value>5:
                    listRules2[row][2]='13'
                UpdateStr(row)
            validityCheck()

        def OnStrChange(evt):
            row=evt.GetId()-150
            listRules2[row][2]=wx.FindWindowById(evt.GetId()).GetValue()
            validityCheck()

        def OnClndrChange(evt):
            """Event handler for date change."""
            row=evt.GetId()-150
            dt=wx.FindWindowById(evt.GetId()).GetValue()
            listRules2[row][2]=time.strftime('%Y-%m-%d',time.strptime(str(dt),'%d.%m.%Y %H:%M:%S'))+' '+listRules2[row][2][11:]
            validityCheck()

        def OnTimeChange(evt):
            """Event handler for time change."""
            row=evt.GetId()-200
            listRules2[row][2]=listRules2[row][2][:11]+wx.FindWindowById(evt.GetId()).GetValue()
            validityCheck()

        def OnPeriodChange(evt):
            row=evt.GetId()-150
            wnd=wx.FindWindowById(evt.GetId())
            oldVal=listRules2[row][2]
            newVal=wnd.GetValue()
            listRules2[row][2]=str(newVal)+oldVal[-1]
            validityCheck()

        def OnUnitChoice(evt):
            row=evt.GetId()-200
            val=listRules2[row][2]
            listRules2[row][2]=val[:-1]+str(wx.FindWindowById(evt.GetId()).GetSelection())
            validityCheck()

        def OnAddButton(evt):
            """Event handler for the button '+' click."""
            if self.i<maxRules:
                #Insert new record at requested position
                listRules2.insert(evt.GetId()+1,[-1,-1,u""])
                #Create new row (bottom)
                AddRow(self.i)
                self.i+=1
                for x in range(evt.GetId()+1,self.i):
                    updateRow(x)
                self.mySizer.Layout()
                if self.i==2:
                    self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(True)
                if self.i==maxRules:
                    for x in range(0,maxRules):
                        self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(False)
            panel.EnableButtons(False) #New row is empty => allways not valid

        def OnRemoveButton(evt):
            """Event handler for the button '-' click."""
            CheckEnable=False #validityCheck "OFF"
            row=evt.GetId()
            if self.i>1:
                tp=SONG_TABLE_FIELDS[listRules2[self.i-1][0]][1]
                if tp<>"D":
                    rng=(0,)
                else:
                    if listRules2[self.i-1][1]>5:
                        rng=(1,0)
                    else:
                        rng=(2,1,0)
                #Remove last record
                del listRules2[row]
                #Remove last row
                infoSizer=self.mySizer.FindItemAtPosition((self.i-1,2)).GetSizer()
                for indx in rng:
                    wnd=infoSizer.GetChildren()[indx].GetWindow()
                    infoSizer.Detach(wnd)
                    wnd.Destroy()
                self.mySizer.Detach(infoSizer)
                infoSizer.Destroy()
                for col in (0,1,3,4):
                    myWnd=self.mySizer.FindItemAtPosition((self.i-1,col)).GetWindow()
                    self.mySizer.Detach(myWnd)
                    myWnd.Destroy()
                if self.i==maxRules:
                    for x in range(0,maxRules-1):
                        self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(True)
                if self.i==2:
                    self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(False)
                self.mySizer.Layout()
                self.i-=1
                for x in range(row,self.i):
                    updateRow(x)
            CheckEnable=True #validityCheck "ON"
            validityCheck()
            
        def OnRandom(evt=None):
            rnd = randomChkBoxCtrl.GetValue()
            if rnd:
                order = False
                orderChkBoxCtrl.SetValue(False)
                shuffle = 0
                shuffleChkBoxCtrl.SetValue(0)
            OnOrderSwitch()
            orderChkBoxCtrl.Enable(not rnd)
            shuffleChkBoxCtrl.Enable(not rnd)
            if evt is not None:
                validityCheck()

        def OnOrderSwitch(evt=None):
            enbl=orderChkBoxCtrl.GetValue()
            if enbl and critCtrl.GetSelection()==-1:
                critCtrl.SetSelection(wx.FindWindowById(50).GetSelection())
            dirCtrl.Enable(enbl)
            dirTxt1.Enable(enbl)
            dirTxt2.Enable(enbl)
            critCtrl.Enable(enbl)
            if evt is not None:
                validityCheck()

        def OnLimitSwitch(evt=None):
            enbl=limitChkBoxCtrl.GetValue()
            numCtrl.Enable(enbl)
            limitTxt1.Enable(enbl)
            limitTxt2.Enable(enbl)
            if evt is not None:
                validityCheck()

        def OnEventInterception(evt):
            validityCheck()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnEventInterception)
        nameCtrl.Bind(wx.EVT_TEXT, OnEventInterception)
        repeatChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        shuffleChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        crossfadeChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        clearPlaylistChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)

        randomChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnRandom)
        orderChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnOrderSwitch)
        limitChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnLimitSwitch)
        OnRandom()
        OnLimitSwitch()
#================================================
        self.i=len(listRules2)
        CheckEnable=False #validityCheck "OFF"
        for x in range(0,len(listRules2)):
            AddRow(x)
            updateRow(x)
        if self.i==1:
            self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(False)
        if self.i==maxRules:
            for x in range(0,maxRules):
                self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(False)
        if listRules2[0][0]==-1: #For new created empty filter
            panel.EnableButtons(False)
        CheckEnable=True #validityCheck "ON"
        self.myDirty=False

        while panel.Affirmed():
            panel.SetResult(
            nameCtrl.GetValue(),
            radioBoxMode.GetSelection(),
            listRules2,
            orderChkBoxCtrl.GetValue(),
            dirCtrl.GetSelection(),
            choices.index(critCtrl.GetStringSelection()),
            limitChkBoxCtrl.GetValue(),
            randomChkBoxCtrl.GetValue(),
            numCtrl.GetValue(),
            repeatChkBoxCtrl.Get3StateValue(),
            shuffleChkBoxCtrl.Get3StateValue(),
            crossfadeChkBoxCtrl.Get3StateValue(),
            clearPlaylistChkBoxCtrl.GetValue(),
            )

    class text:
        radioboxMode = "Select songs ..."
        modeAnd = "Matches all rules (AND)"
        modeOr = "Matches at least one rule (OR)"
        equal = "is equal to"
        notEqual = "is not equal to"
        greater = "is greater than"
        greatOrEqual = "is greater than or equal to"
        less = "is less than"
        lowerOrEqual = "is less than or equal to"
        notStartsWith = "does not start with"
        startsWith = "starts with"
        endsWith = "ends with"
        notEndsWith = "does not end with"
        includes = "includes"
        notIncludes = "excludes"
        isEmpty = "is empty"
        isNotEmpty = "is non-empty"
        beforeLess = "was earlier than - before ..."   #RELATIVE TO 'NOW' MODE
        beforeMore = "was later than - before ..."     #RELATIVE TO 'NOW' MODE
        filterName = "Filter name:"
        found = "%s/%s songs found"
        noFound = "no song found"
        asc = "ascending"
        desc = "descending"
        order1 = "Songs found are sorted in"
        order2 = "order by:"
        limit1 = "Select only the first"
        limit2 = "entry"
        #seconds = "seconds"
        minutes = "minutes"
        hours = "hours"
        days = "days"
        months = "months"
        years = "years"
#====================================================================

class LoadPlaylistBySql(eg.ActionBase):
    name = "Load Playlist by SQL query"
    description = ur'''<rst>**Loads a MediaMonkey playlist defined by SQL query.** 

This action is for advanced users only. Here you can write your own SQL
query and use it to select specific songs from **MediaMonkey**'s 
database . You need only enter the *WHERE* clause into the text field, 
but you can also add an *ORDER BY* clause and *LIMIT* clause 
(I tried the OFFSET clause too, but without success).

The simplest query might look like this: **Artist = "Beatles"**. 

**MediaMonkey**'s database is based on **SQLite**. 
Its documentation can be found at http://www.sqlite.org/docs.html . 
If you are new to SQL, you might get some help from a SQL tutorial. 
A good example can be found at http://www.firstsql.com/tutor2.htm . 
Pay particular attention to the `WHERE Clause`_ .

.. _`WHERE Clause`: http://www.firstsql.com/tutor2.htm#where'''

    def __init__(self):
        self.myDirty=None
        text=self.text

    def __call__(
        self,
        plName,
        sql,
        repeat,
        shuffle,
        crossfade,
        clear,
    ):
        if not self.plugin.workerThread2:
            self.plugin.workerThread2 = MediaMonkeyWorkerThread(self.plugin)
            self.plugin.workerThread2.Start(100.0)
        args = (
            self.plugin.workerThread2.LoadSqlPlaylist,
            plName,
            sql,
            repeat,
            shuffle,
            crossfade,
            clear,
        )
        self.plugin.workerThread2.Call(partial(*args))

    def Configure(
        self,
        plName="",
        query="",
        repeat=2,
        shuffle=2,
        crossfade=2,
        clear = True,
    ):
        tmpDict=dict(zip(Text.SongTableFields,[tpl[0] for tpl in SONG_TABLE_FIELDS]))
        panel = eg.ConfigPanel(self,resizable = True)
        text = self.text
        mySizer = wx.GridBagSizer(10, 10)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        sqlTextCtrl=wx.TextCtrl(panel,-1,query,style=wx.TE_MULTILINE)
        mySizer.Add(sqlTextCtrl, (0,0), (1, 3), flag = wx.EXPAND)
        mySizer.Add(
            wx.StaticText(panel, -1, text.cols),(1,0),(1,2),
            flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT
        )
        choices=['']
        choices.extend(Text.SongTableFields)
        choices.sort()
        colCtrl=wx.Choice(panel,-1 , choices=choices)
        mySizer.Add(colCtrl, (2,0), (1, 1), flag = wx.ALIGN_LEFT|wx.TOP,border = -6)
        callSizer = wx.BoxSizer(wx.VERTICAL)
        nameSizer = wx.BoxSizer(wx.VERTICAL)
        statBox = wx.StaticBox(panel, -1, "")
        stBsizer = wx.StaticBoxSizer(statBox, wx.HORIZONTAL)
        #stBsizer.SetMinSize((240,-1))
        stBsizer.Add(nameSizer,1,wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, plName)
        nameSizer.Add(wx.StaticText(panel, -1, text.filterName),0,wx.LEFT)
        nameSizer.Add(nameCtrl, 0,wx.TOP|wx.EXPAND,4)
        mySizer.Add(stBsizer, (1,2), (2, 1), flag = wx.ALIGN_RIGHT)

        repeatChkBoxCtrl = wx.CheckBox(panel, label=Text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=Text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=Text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        clearPlaylistChkBoxCtrl = wx.CheckBox(panel, label=Text.clearPlaylist)
        clearPlaylistChkBoxCtrl.SetValue(clear)
        mySizer.Add(repeatChkBoxCtrl,(3,0),(1,1),flag=wx.ALIGN_LEFT)
        mySizer.Add(shuffleChkBoxCtrl,(3,1),(1,1),flag=wx.ALIGN_LEFT)
        mySizer.Add(crossfadeChkBoxCtrl,(4,0),(1,1),flag=wx.ALIGN_LEFT)
        mySizer.Add(clearPlaylistChkBoxCtrl,(4,1),(1,2),flag=wx.RIGHT)
        headLabel = wx.StaticText(panel, -1, text.head)
        panel.sizer.Add(headLabel,flag = wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND|wx.TOP,border=4)
        headLabel.SetFocus()

        def onColCtrl(evt):
            field = colCtrl.GetStringSelection()
            if field:
                col = tmpDict[field]
                sqlTextCtrl.WriteText(col)
        colCtrl.Bind(wx.EVT_CHOICE,onColCtrl)
        
        def onSqlTextCtrl(evt):
            colCtrl.SetSelection(0)
            evt.Skip()
        sqlTextCtrl.Bind(wx.EVT_TEXT,onSqlTextCtrl)

        while panel.Affirmed():
            panel.SetResult(
            nameCtrl.GetValue(),
            sqlTextCtrl.GetValue(),
            repeatChkBoxCtrl.Get3StateValue(),
            shuffleChkBoxCtrl.Get3StateValue(),
            crossfadeChkBoxCtrl.Get3StateValue(),
            clearPlaylistChkBoxCtrl.GetValue(),
            )
            
    class text:
        filterName = "Filter name:"
        found = "%s/%s songs found"
        noFound = "no song found"
        asc = "ascending"
        desc = "descending"
        order1 = "Songs found are sorted in"
        order2 = "order by:"
        limit1 = "Select only the first"
        limit2 = "entry"
        head = "Condition part of SQL statement (WHERE clause):"
        cols = "Insert typical field from MM Songs table:"
#====================================================================

class Jukebox(eg.ActionBase):
    name = "Album jukebox"
    description = u'''<rst>**Album jukebox**.

Thanks to this action, your PC can function like a jukebox. In order to work 
properly, the event which triggers this action, must be carrying a payload. 
If this payload is a valid ID of an album, MediaMonkey will immediately start 
playing this album. 

One way to trigger an event with a payload is to use the plugin **Multitap** 
(Numpad mode).'''
        
    def Configure(self,repeat=2,shuffle=2,crossfade=2,clear = True, filePath='', stop = True):
        txt = self.text
        self.filePath = filePath
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        if filePath:
            startFolder = path_split(filePath)[1]
        else:
            startFolder = eg.folderPath.Documents
        filePathCtrl = eg.FileBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.plugin.text.toolTipFolder,
            dialogTitle = self.plugin.text.browseTitle,
            buttonText = eg.text.General.browse,
            initialValue=startFolder+'\\AlbumListMM.txt',
            fileMask="CSV files (*.csv)|*.csv|"\
                "Text file (*.txt)|*.txt|"\
                "All files (*.*)|*.*",
        )
        if filePath:
            filePathCtrl.SetValue(filePath)        

        Sizer = panel.sizer
        sizes = []
        sizes.append(panel.GetTextExtent(txt.saveButton)[0])
        sizes.append(panel.GetTextExtent(txt.openButton)[0])
        w=max(sizes)+24        
        exportButton = wx.Button(panel, -1, txt.saveButton, size = ((w,-1)))
        exportButton.SetToolTip(wx.ToolTip(txt.baloonBttn[0]))
        openButton = wx.Button(panel, -1, txt.openButton, size = ((w,-1)))
        openButton.SetToolTip(wx.ToolTip(txt.baloonBttn[1] % self.filePath))
        repeatChkBoxCtrl = wx.CheckBox(panel, label=Text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=Text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=Text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        clearPlaylistChkBoxCtrl = wx.CheckBox(panel, label=Text.clearPlaylist)
        stopChkBoxCtrl = wx.CheckBox(panel, label=Text.stopPlaying)
        clearPlaylistChkBoxCtrl.SetValue(clear)
        stopChkBoxCtrl.SetValue(stop)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        Sizer.Add(repeatChkBoxCtrl,0)
        Sizer.Add(shuffleChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(crossfadeChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(clearPlaylistChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(stopChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(label1Text, 0, wx.TOP,15)
        Sizer.Add(filePathCtrl,0,wx.TOP,3)
        Sizer.Add(exportButton,0,wx.TOP,10)
        Sizer.Add(openButton,0,wx.TOP,10)
            
        def onBtnClick(event):
            self.filePath=filePathCtrl.GetValue()
            self.jukeboxFrame = JukeboxFrame(parent=self)
            wx.CallAfter(
                self.jukeboxFrame.ShowJukeboxFrame,
                'Album',
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                True,
                stopChkBoxCtrl.GetValue(),
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue(),
            )
            openButton.Enable(True)
            event.Skip()
        exportButton.Bind(wx.EVT_BUTTON, onBtnClick)
        
        def onOpenBtnClick(event):
            if isfile(self.filePath):
                flag = False
            else:
                flag = True
                self.filePath=filePathCtrl.GetValue()
            self.jukeboxFrame = JukeboxFrame(parent = self)
            wx.CallAfter(
                self.jukeboxFrame.ShowJukeboxFrame,
                'Album',
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                flag,
                stopChkBoxCtrl.GetValue(),
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue(),
            )
            event.Skip()
        openButton.Bind(wx.EVT_BUTTON, onOpenBtnClick)
        
        while panel.Affirmed():
            panel.SetResult(
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue(),
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                stopChkBoxCtrl.GetValue()
            )

    def GetLabel(self,repeat,shuffle,crossfade,clear,filePath,stop):
        return self.name       

    def __call__(self,repeat=2,shuffle=2,crossfade=2,clear=True,filePath='',stop=True):
        ID = eg.event.payload
        self.plugin.Jubox(
            ID,
            clear,
            repeat,
            shuffle,
            crossfade,
            stop,
        )
            
    class text():
        label1 = "Target file to export albums:"
        saveButton = "Export album list to file"
        openButton = "Open album list file"
        baloonBttn =('''ATTENTION !!! This operation may take several minutes !!!
Click to export code, album name and album artist to selected file.
You can this file import for example to MS Excel or OOo Calc''',
            'Open file %s'
        )
#====================================================================

class SongJukebox(eg.ActionBase):
    name = "Song jukebox"
    description = u'''<rst>**Song jukebox**.

Thanks to this action, your PC can function like a jukebox. In order to work 
properly, the event which triggers this action, must be carrying a payload. 
If this payload is a valid ID of a song, MediaMonkey will immediately start 
playing the song. 

One way to trigger an event with a payload is to use the plugin **Multitap** 
(Numpad mode).'''
        
    def Configure(self,clear=False,filePath='',stop = True):
        self.filePath = filePath
        txt = self.text
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        if filePath:
            startFolder = path_split(filePath)[1]
        else:
            startFolder = eg.folderPath.Documents
        filePathCtrl = eg.FileBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.plugin.text.toolTipFolder,
            dialogTitle = self.plugin.text.browseTitle,
            buttonText = eg.text.General.browse,
            initialValue=startFolder+'\\SongListMM.txt',
            fileMask="CSV files (*.csv)|*.csv|"\
                "Text file (*.txt)|*.txt|"\
                "All files (*.*)|*.*",
        )
        if filePath:
            filePathCtrl.SetValue(filePath)        
        Sizer = panel.sizer
        sizes = []
        sizes.append(panel.GetTextExtent(txt.saveButton)[0])
        sizes.append(panel.GetTextExtent(txt.openButton)[0])
        w=max(sizes)+24        
        exportButton = wx.Button(panel, -1, txt.saveButton, size=((w,-1)))
        exportButton.SetToolTip(wx.ToolTip(txt.baloonBttn[0]))
        openButton = wx.Button(panel, -1, txt.openButton, size=((w,-1)))
        openButton.SetToolTip(wx.ToolTip(txt.baloonBttn[1] % self.filePath))
        clearPlaylistChkBoxCtrl = wx.CheckBox(panel, label=Text.clearPlaylist)
        clearPlaylistChkBoxCtrl.SetValue(clear)
        stopChkBoxCtrl = wx.CheckBox(panel, label=Text.stopPlaying)
        stopChkBoxCtrl.SetValue(stop)
        Sizer.Add(clearPlaylistChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(stopChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(label1Text, 0, wx.TOP,15)
        Sizer.Add(filePathCtrl,0,wx.TOP,3)
        Sizer.Add(exportButton,0,wx.TOP,20)
        Sizer.Add(openButton,0,wx.TOP,20)
            
        def onBtnClick(event):
            self.filePath=filePathCtrl.GetValue()
            self.jukeboxFrame = JukeboxFrame(parent = self)
            wx.CallAfter(
                self.jukeboxFrame.ShowJukeboxFrame,
                'Song',
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                True,
                stopChkBoxCtrl.GetValue(),
            )
            openButton.Enable(True)
            event.Skip()
        exportButton.Bind(wx.EVT_BUTTON, onBtnClick)

        def onOpenBtnClick(event):
            if isfile(self.filePath):
                flag = False
            else:
                self.filePath=filePathCtrl.GetValue()
                flag = True
            self.jukeboxFrame = JukeboxFrame(parent = self)
            wx.CallAfter(
                self.jukeboxFrame.ShowJukeboxFrame,
                'Song',
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                flag,
                stopChkBoxCtrl.GetValue(),
            )
            event.Skip()
        openButton.Bind(wx.EVT_BUTTON, onOpenBtnClick)
        
        while panel.Affirmed():
            panel.SetResult(
                clearPlaylistChkBoxCtrl.GetValue(),
                filePathCtrl.GetValue(),
                stopChkBoxCtrl.GetValue()
            )

    def GetLabel(self,clear,filePath, stop):
        return self.name       

    def __call__(self,clear=True,filePath='', stop = True):
        ID = eg.event.payload
        self.plugin.SongJubox(
            ID,
            clear,
            stop
        )
            
    class text():
        label1 = "Target file to export songs:"
        saveButton = "Export song list to file"
        openButton = "Open song list file"
        baloonBttn = ('''ATTENTION !!! This operation may take several minutes !!!
Click to export code, song name and song artist to selected file.
You can this file import for example to MS Excel or OOo Calc''',
            'Open file %s'
        )
#====================================================================

class SendKeys(eg.ActionBase):
    name = "Send keys"
    description = '''<rst>**Sends keys to MediaMonkey Window**.

Some features of MediaMonkey (for example executing a script) can be controlled 
from another program only using the hotkeys . On the menu 
*Tools - Options - General - Hotkeys*, set an appropriate hotkeys 
(you don't need to set the hotkeys as global !) and then in the text box *"Keystroke to send"* 
type the same (for example *Shift+Alt+E*). In the text box *"Name of hotkey"* 
you can label the keystrokes with your own description.'''
    
    def __call__(self, descr = "",keys = ""):
        hwnds = MyWindowMatcher()
        if hwnds:
            eg.SendKeys(hwnds[0],u'{'+keys+u'}', False)

    def Configure(self,descr="",keys = ""):
        text  = self.Text
        panel = eg.ConfigPanel(self)
        Sizer = panel.sizer
        #descrLabel.Enable(False)
        nameLabel = wx.StaticText(panel,-1,text.nameLabel)
        nameCtrl = wx.TextCtrl(panel,-1,descr)
        keysLabel = wx.StaticText(panel,-1,text.keysLabel)
        keysCtrl = wx.TextCtrl(panel,-1,keys)
        Sizer.Add(nameLabel,0,wx.TOP,18)
        Sizer.Add(nameCtrl,0,wx.TOP,4)
        Sizer.Add(keysLabel,0,wx.TOP,18)
        Sizer.Add(keysCtrl,0,wx.TOP,4)
        while panel.Affirmed():
            panel.SetResult(
            nameCtrl.GetValue(),
            keysCtrl.GetValue(),
        )
    def GetLabel(self,descr="",keys = ""):
        if descr != '':
            return descr
        else:
            return keys
        
    class Text():
        nameLabel = "Name of hotkey:"
        keysLabel = "Keystroke to send (e.g. Shift+Alt+E):"
       
#===============================================================================

class JukeboxFrame(wx.Frame):
    
    def __init__(self, parent):
        self.plugin = parent.plugin
        wx.Frame.__init__(
            self,
            None,
            -1,
            size=(-1, -1),
            style=wx.CAPTION|wx.RESIZE_BORDER
        )
        self.SetBackgroundColour(wx.NullColour)
        self.menuFlag = False
        self.parent=parent

    def ShowJukeboxFrame(
        self,
        case,
        clear,
        filePath,
        create,
        stop,
        repeat = None,
        shuffle = None,
        crossfade = None,
    ):

        eg.Bind("MediaMonkey.jukebox",self.CompleteForm)
        self.case = case
        self.clear = clear
        self.filePath = filePath
        self.create = create
        self.repeat = repeat
        self.shuffle = shuffle
        self.crossfade = crossfade
        self.stop = stop
        self.text = self.plugin.text
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        centralSizer = wx.GridBagSizer(10, 10)
        centralSizer.AddGrowableRow(0)
        centralSizer.AddGrowableCol(1)
        if case == 'Album':
            cols = self.text.labelsA
        else:
            cols = self.text.labelsS
        self.itemListCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, label in enumerate(cols):
            self.itemListCtrl.InsertColumn(
                i,
                label,
            )
        centralSizer.Add(self.itemListCtrl, (0,0),(1,3), flag = wx.EXPAND)

        #Buttons
        self.playButton = wx.Button(self, -1, self.text.popup)
        self.playButton.Enable(False)
        centralSizer.Add(self.playButton,(1,0), flag = wx.ALIGN_LEFT)
        self.closeButton = wx.Button(self, -1, self.text.close)
        centralSizer.Add(self.closeButton,(1,2), flag = wx.ALIGN_RIGHT)
        
        self.itemListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ListSelection)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.ListSelection)

        def OnSize(event):
            w = self.GetSize()[0]/2-52
            self.itemListCtrl.SetColumnWidth(1, w)
            self.itemListCtrl.SetColumnWidth(2, w)
            event.Skip()

        mainSizer.Add(centralSizer, 1,wx.EXPAND|wx.ALL,10)
        mainSizer.Layout()
        self.SetSizer(mainSizer)

        def OnCloseWindow(event):
            eg.Unbind("MediaMonkey.jukebox",self.CompleteForm)
            self.Show(False)
            self.MakeModal(False)
            self.Destroy()
            event.Skip()

        self.Bind(wx.EVT_CLOSE, OnCloseWindow)
        self.playButton.Bind(wx.EVT_BUTTON, self.onPlayButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)
        self.SetMinSize((475,200))
        self.CentreOnParent()
        self.SetTitle(self.filePath)
        sizes = (55,200,200)
        for i in range(3):
            self.itemListCtrl.SetColumnWidth(i, sizes[i])
        self.SetDimensions(-1, -1, 504, 400, sizeFlags=wx.SIZE_AUTO)
        self.Bind(wx.EVT_SIZE, OnSize)
        self.MakeModal(True)
        self.Show(True)
        self.RefreshList()
        
    def RefreshList(self):
        self.patientFrame = None
        if not self.create:
            self.CompleteForm()                  
        else:
            self.itemListCtrl.DeleteAllItems()
            self.Update()
            if self.plugin.checkWorkerThread():
                self.patientFrame = PatientFrame(self,self.text.please)
                if self.case=='Album':
                    self.plugin.workerThread.Call(partial(self.plugin.workerThread.ExportAlbumList,self.filePath))
                else:
                    self.plugin.workerThread.Call(partial(self.plugin.workerThread.ExportSongList,self.filePath))
                self.Enable(False)

    def CompleteForm(self,evt=None):
        row = 0
        file = codecs.open(self.filePath,encoding='utf-8', mode='r',errors='replace')
        albums = file.readlines()
        for album in albums:
            item = album.split('\t')
            self.itemListCtrl.InsertStringItem(row,item[0])
            self.itemListCtrl.SetStringItem(row, 1,item[1])
            self.itemListCtrl.SetStringItem(row, 2, item[2][:-1])
            row += 1
        file.close()
        if self.patientFrame:
            self.patientFrame.Destroy()
        self.Enable(True)
        self.Raise()

    def onCloseButton(self, evt):
        self.Close(True)
        #evt.Skip()

    def ListSelection(self, event=None):
        self.menuFlag = self.itemListCtrl.GetSelectedItemCount() == 1
        self.playButton.Enable(self.menuFlag)
        if event:
            event.Skip()

    def onPlayButton(self, evt):
        item = self.itemListCtrl.GetFirstSelected()
        ID = self.itemListCtrl.GetItemText(item)
        if self.case == 'Album':
            self.plugin.Jubox(
                ID,
                self.clear,
                self.repeat,
                self.shuffle,
                self.crossfade,
                self.stop
            )
        else:
            self.plugin.SongJubox(ID,self.clear,self.stop)
        evt.Skip()

    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.onPlayButton, id=self.popupID1)

        # make a menu
        menu = wx.Menu()
        # add some items
        if self.menuFlag:
            menu.Append(self.popupID1, self.text.popup)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
#===============================================================================

class UnaccessibleTracksFrame(wx.Frame):
    
    def __init__(self, parent):
        self.parent=parent
        self.plugin = parent.plugin
        wx.Frame.__init__(
            self,
            None,
            -1,
            size=(-1, -1),
            style=wx.CAPTION|wx.RESIZE_BORDER
        )
        self.SetBackgroundColour(wx.NullColour)
        self.menuFlag = False

    def ShowUnaccessibleTracksFrame(
        self,
        filePath,
        mode=True
    ):
        eg.Bind("MediaMonkey.unaccessible",self.CompleteForm)
        self.filePath = filePath
        self.mode = mode
        self.text = self.plugin.text
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        centralSizer = wx.GridBagSizer(10, 10)
        centralSizer.AddGrowableRow(0)
        centralSizer.AddGrowableCol(1)
        centralSizer.AddGrowableCol(3)
        cols = self.text.labelsU
        self.itemListCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, label in enumerate(cols):
            self.itemListCtrl.InsertColumn(
                i,
                label,
            )
        centralSizer.Add(self.itemListCtrl, (0,0),(1,5), flag = wx.EXPAND)

        #Buttons
        self.deleteButton = wx.Button(self, -1, self.text.popup2)
        self.deleteButton.Enable(False)
        centralSizer.Add(self.deleteButton,(1,0), flag = wx.ALIGN_LEFT)
        self.refreshButton = wx.Button(self, -1, self.text.refresh)
        centralSizer.Add(self.refreshButton,(1,2), flag = wx.ALIGN_CENTER)
        self.closeButton = wx.Button(self, -1, self.text.close)
        centralSizer.Add(self.closeButton,(1,4), flag = wx.ALIGN_RIGHT)
        
        self.itemListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ListSelection)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.ListSelection)

        def OnSize(event):
            w = self.GetSize()[0]/4-26
            self.itemListCtrl.SetColumnWidth(1, w)
            self.itemListCtrl.SetColumnWidth(2, 3*w)
            event.Skip()

        mainSizer.Add(centralSizer, 1,wx.EXPAND|wx.ALL,10)
        mainSizer.Layout()
        self.SetSizer(mainSizer)

        def OnCloseWindow(event):
            eg.Unbind("MediaMonkey.unaccessible",self.CompleteForm)
            self.Show(False)
            self.MakeModal(False)
            self.Destroy()
            self.parent.frameIsOpen = False

        self.Bind(wx.EVT_CLOSE, OnCloseWindow)
        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDeleteButton)
        self.refreshButton.Bind(wx.EVT_BUTTON, self.onRefreshButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)
        self.SetMinSize((475,200))
        self.CentreOnParent()
        self.SetTitle(filePath)
        row = 0
        sizes = (55,100,300)
        for i in range(2):
            self.itemListCtrl.SetColumnWidth(i, sizes[i])
        self.SetDimensions(-1, -1, 504, 400, sizeFlags=wx.SIZE_AUTO)
        self.Bind(wx.EVT_SIZE, OnSize)
        self.MakeModal(True)
        self.Show(True)
        self.onRefreshButton()
        
    def onCloseButton(self, evt):
        self.Close(True)

    def ListSelection(self, event=None):
        self.menuFlag = self.itemListCtrl.GetSelectedItemCount() > 0
        self.deleteButton.Enable(self.menuFlag)
        if event:
            event.Skip()

    def onDeleteButton(self, evt):
        item = self.itemListCtrl.GetFirstSelected()
        tmpList=[]
        while item != -1:
            ID = self.itemListCtrl.GetItemText(item)
            tmpList.append(ID)
            item = self.itemListCtrl.GetNextSelected(item)
        for n in range(self.itemListCtrl.GetItemCount()-1,-1,-1):
            for item in tmpList:
                if item == self.itemListCtrl.GetItemText(n):
                    if self.plugin.DeleteSong(item) == "0":
                        self.itemListCtrl.DeleteItem(n)
                    break
        n = self.itemListCtrl.GetItemCount()
        if n > 0:
            file = codecs.open(self.filePath,encoding='utf-8', mode='w',errors='replace')
            for item in range(n):
                file.write('\t'.join((
                    self.itemListCtrl.GetItemText(item),
                    self.itemListCtrl.GetItem(item,1).GetText(),
                    self.itemListCtrl.GetItem(item,2).GetText(),
                )))
                file.write('\n')
            file.close()
        elif isfile(self.filePath):
            remove_file(self.filePath)            
        evt.Skip()
        
    def onRefreshButton(self,evt=None):
        self.patientFrame = None
        if not evt and not self.mode and isfile(self.filePath):
            self.CompleteForm()                  
        else:
            self.itemListCtrl.DeleteAllItems()
            self.Update()
            if self.plugin.checkWorkerThread():
                self.patientFrame = PatientFrame(self,self.text.please)
                self.plugin.workerThread.Call(partial(self.plugin.workerThread.GetNotAccessibleTracks,self.filePath))
                self.Enable(False)
        if evt:
            evt.Skip()
            
    def CompleteForm(self,evt=None):
#        self.MakeModal(True)
        if isfile(self.filePath):
            file = codecs.open(self.filePath,encoding='utf-8', mode='r',errors='replace')
            tracks = file.readlines()
            row = 0
            for track in tracks:
                item = track.split('\t')
                self.itemListCtrl.InsertStringItem(row,item[0])
                self.itemListCtrl.SetStringItem(row, 1,item[1])
                self.itemListCtrl.SetStringItem(row, 2,item[2][:-1])
                row += 1
            file.close()
        if self.patientFrame:
            self.patientFrame.Destroy()
        self.Enable(True)
        self.Raise()

    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.onDeleteButton, id=self.popupID1)

        # make a menu
        menu = wx.Menu()
        # add some items
        if self.menuFlag:
            menu.Append(self.popupID1, self.text.popup2)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
#===============================================================================

class PatientFrame(wx.Frame):
    def __init__(
        self,
        parent,
        message,
    ):
        if parent is None and eg.document.frame:
            parent = eg.document.frame
        wx.Frame.__init__(self, parent, -1, eg.APP_NAME, wx.DefaultPosition, style=wx.RAISED_BORDER| wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.NullColour)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_CMN_DIALOG, (32, 32))
        staticBitmap = wx.StaticBitmap(self, -1, bmp)
        staticBitmap2 = wx.StaticBitmap(self, -1, bmp)
        staticText = wx.StaticText(self, -1, message)
        fnt = staticText.GetFont()
        fnt.SetPointSize(13)
        staticText.SetFont(fnt)
        sizer.Add(staticBitmap, 0, wx.ALL, 12)
        sizer.Add(staticText,0,wx.ALIGN_CENTER)
        sizer.Add(staticBitmap2, 0, wx.ALL, 12)
        self.SetSizerAndFit(sizer)
        self.CenterOnParent()
        self.Show()
        self.Update()
#===============================================================================

ACTIONS = (
    (GetSomeInfo, 'GetVolume', 'Get Volume', 'Get Volume.', (100,'Volume')),
    (GetSomeInfo, 'GetBalance', 'Get Balance', 'Get Balance.', (100,'Panning')),
    (GetSomeInfo, 'GetRepeat', 'Get Repeat', 'Get Repeat Status.', (1,'isRepeat')),
    (GetSomeInfo, 'GetShuffle', 'Get Shuffle', 'Get Shuffle Status.', (1,'isShuffle')),
    (GetSomeInfo, 'GetAutoDJ', 'Get AutoDJ', 'Get AutoDJ Status.', (1,'isAutoDJ')),
    (GetSomeInfo, 'GetCrossfade', 'Get Crossfade', 'Get Crossfade Status.', (1,'isCrossfade')),
    (GetSomeInfo, 'GetPosition', 'Get Position in ms', 'Get Position in ms.', (1,'PlaybackTime')),
)

ACTIONS2 = (
    (GetSongInfo, 'GetBasicSongInfo', 'Get Basic Song Info', 'Get Basic Song Info.', 0),
    (GetSongInfo, 'GetBasicSongInfoNextTrack', 'Get Basic Song Info Of Next Track', 'Get Basic Song Info Of Next Track.', 1),
    (GetSongInfo, 'GetBasicSongInfoPreviousTrack', 'Get Basic Song Info Of Previous Track', 'Get Basic Song Info Of Previous Track.', -1),
)
