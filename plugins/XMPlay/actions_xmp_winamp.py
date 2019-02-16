# -*- coding: utf-8 -*-
#


import eg
from eg.WinApi import SendMessageTimeout, WM_USER
import utils_xmp



# xmp-sdk\xmpfunc.h
# The following Winamp messages are also supported by XMPlay (see Winamp SDK for descriptions)
# Winamp\wa_ipc.h
WM_WA_IPC = WM_USER # = 0x0400
# Use this api to clear Winamp's internal playlist.
IPC_DELETE = 101

# Sending this will start playback and is almost the same as hitting the play button.
IPC_STARTPLAY = 102

# This is sent to retrieve the current playback state of Winamp.
# If it returns 1, Winamp is playing.
# If it returns 3, Winamp is paused.
# If it returns 0, Winamp is not playing.
IPC_ISPLAYING = 104

# SendMessage(hwnd_winamp,WM_WA_IPC,mode,IPC_GETOUTPUTTIME);
# This api can return two different sets of information about current playback status.
# If mode = 0 then it will return the position (in ms) of the currently playing track.
# Will return -1 if Winamp is not playing.
# If mode = 1 then it will return the current track length (in seconds).
# Will return -1 if there are no tracks (or possibly if Winamp cannot get the length).
# XMPlay with mode = 2 always returns -1!
# If mode = 2 then it will return the current track length (in milliseconds).
# Will return -1 if there are no tracks (or possibly if Winamp cannot get the length).
IPC_GETOUTPUTTIME = 105

# SendMessage(hwnd_winamp,WM_WA_IPC,ms,IPC_JUMPTOTIME);
# This api sets the current position (in milliseconds) for the currently playing song.
# The resulting playback position may only be an approximate time since some playback
# formats do not provide exact seeking e.g. mp3
# This returns -1 if Winamp is not playing, 1 on end of file, or 0 if it was successful.
IPC_JUMPTOTIME = 106

# SendMessage(hwnd_winamp,WM_WA_IPC,position,IPC_SETPLAYLISTPOS)
# IPC_SETPLAYLISTPOS sets the playlist position to the specified 'position'.
# It will not change playback status or anything else. It will just set the current
# position in the playlist and will update the playlist view if necessary.
IPC_SETPLAYLISTPOS = 121

# SendMessage(hwnd_winamp,WM_WA_IPC,volume,IPC_SETVOLUME);
# IPC_SETVOLUME sets the volume of Winamp (between the range of 0 to 255).
# If you pass 'volume' as -666 then the message will return the current volume.
# int curvol = SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETVOLUME);
IPC_SETVOLUME = 122

# SendMessage(hwnd_winamp,WM_WA_IPC,panning,IPC_SETPANNING);
# IPC_SETPANNING sets the panning of Winamp from 0 (left) to 255 (right).
# At least in Winamp 5.x+ this works from -127 (left) to 127 (right).
# If you pass 'panning' as -666 to this api then it will return the current panning.
# int curpan = SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETPANNING);
IPC_SETPANNING = 123

# IPC_GETLISTLENGTH returns the length of the current playlist as the number of tracks.
IPC_GETLISTLENGTH = 124

# IPC_GETLISTPOS returns the current playlist position.
IPC_GETLISTPOS = 125

# char *name=SendMessage(hwnd_winamp,WM_WA_IPC,index,IPC_GETPLAYLISTFILE);
# IPC_GETPLAYLISTFILE gets the filename of the playlist entry [index].
# returns a pointer to it. returns NULL on error.
IPC_GETPLAYLISTFILE = 211

# char *name=SendMessage(hwnd_winamp,WM_WA_IPC,index,IPC_GETPLAYLISTTITLE);
# IPC_GETPLAYLISTTITLE gets the title of the playlist entry [index].
# returns a pointer to it. returns NULL on error.
IPC_GETPLAYLISTTITLE = 212



class IPC(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(): return
        return SendMessageTimeout(self.plugin.xmp_window, WM_WA_IPC, *self.value)

        
        
class IPC1000(eg.ActionBase):
    """IPC with miliseconds to seconds converter."""
    def __call__(self):
        if self.plugin.is_xmp_off(): return
        retval = SendMessageTimeout(self.plugin.xmp_window, WM_WA_IPC, *self.value)
        return retval if retval == -1 else retval / 1000.0
        
        
        
class IPCPlayStatus(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(): return
        status = SendMessageTimeout(self.plugin.xmp_window, WM_WA_IPC, 0, IPC_ISPLAYING)
        if status == 1:
            return "playing"
        elif status == 3:
            return "paused"
        else: #0
            return "stopped"

            
            
class IPCSetter(utils_xmp.IntSetter):

    def __call__(self, value=0, from_eg_result=False):
        if self.plugin.is_xmp_off(): return
        if from_eg_result:
            # ValueError expected from users, its OK
            value = int(eg.result)
        return SendMessageTimeout(self.plugin.xmp_window, WM_WA_IPC, value, self.value)


        
class IPCSetter1000(utils_xmp.IntSetter):
    """IPCSetter with miliseconds to seconds converter."""
    def __call__(self, value=0, from_eg_result=False):
        if self.plugin.is_xmp_off(): return
        if from_eg_result:
            # ValueError expected from users, its OK
            value = int(eg.result)
        return SendMessageTimeout(self.plugin.xmp_window, WM_WA_IPC, value * 1000, self.value)


        
class IPCFromMemory(IPCSetter):
    
    def __call__(self, value=0, from_eg_result=False):
        address = super(IPCFromMemory, self).__call__(value, from_eg_result)
        return self.plugin.xmp_memory_reader.read_string(address).decode("utf-8")

        
        
actions = (
    (IPC, 
        "ClearPlaylist", 
        "Clear Playlist", 
        "Clear the playlist.", 
        (0, IPC_DELETE)
    ),
    (IPC, 
        "Play", 
        "Play", 
        "Start playback.", 
        (0, IPC_STARTPLAY)
    ),
    (IPCPlayStatus, 
        "GetPlayingStatusNow", 
        "Get Play Status", 
        "Get the play status, returns \"playing\", \"paused\" or \"stopped\".", 
        None
    ),
    (IPC1000, 
        "GetElapsed", 
        "Get Track Elapsed", 
        "Get the elapsed time in seconds of the currently playing track. Will return -1 if not playing.", 
        (0, IPC_GETOUTPUTTIME)
    ),
    (IPC, 
        "GetDuration", 
        "Get Track Duration", 
        "Get the duration in seconds of the current track. Will return -1 if cannot get it.", 
        (1, IPC_GETOUTPUTTIME)
    ),
    (IPCSetter1000, 
        "JumpToTime", 
        "Jump to Time", 
        "Jump to time in seconds of the currently playing track. Will return -1 if not playing.", 
        IPC_JUMPTOTIME
    ),
    # (IPCSetter, 
        # "JumpToTrack", 
        # "Jump to Track", 
        # "Set the current position in the playlist. This action will not change playback status.", 
        # IPC_SETPLAYLISTPOS
    # ),
    (IPCSetter, 
        "SetVolumeRaw", 
        "Set Volume", 
        "Set the volume level between the range of 0 to 255.", 
        IPC_SETVOLUME
    ),
    (IPC, 
        "GetVolumeRaw", 
        "Get Volume", 
        "Get the volume level between the range of 0 to 255.", 
        (-666, IPC_SETVOLUME)
    ),
    (IPCSetter, 
        "SetBalanceRaw", 
        "Set Balance", 
        "Set the balance of XMPlay from 0 (left) to 127 (middle) to 255 (right).", 
        IPC_SETPANNING
    ),
    (IPC, 
        "GetBalanceRaw", 
        "Get Balance", 
        "Get the balance of XMPlay from 0 (left) to 127 (middle) to 255 (right).", 
        (-666, IPC_SETPANNING)
    ),
    (IPC, 
        "GetLength", 
        "Get Playlist Length", 
        "Get the number of tracks in the playlist.", 
        (0, IPC_GETLISTLENGTH)
    ),
    (IPCSetter, 
        "SetPosition", 
        "Set Playlist Position", 
        ("Set the current position in the playlist. "
        "This action will not change playback status. "
        "To that end add DDE command No. 372 (\"List - Play\")"), 
        IPC_SETPLAYLISTPOS
    ),
    (IPC, 
        "GetPosition", 
        "Get Playlist Position", 
        "Get the current position in the playlist.", 
        (0, IPC_GETLISTPOS)
    ),
    (IPCFromMemory, 
        "GetPlaylistFile", 
        "Get Playlist File", 
        "Get the file name at the position in the playlist.", 
        IPC_GETPLAYLISTFILE
    ),
    (IPCFromMemory, 
        "GetPlaylistTitle", 
        "Get Playlist Title", 
        "Get the track title at the position in the playlist.", 
        IPC_GETPLAYLISTTITLE
    ),
)

