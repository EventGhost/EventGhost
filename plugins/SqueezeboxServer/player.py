"""
PySqueezeCenter: Python Wrapper for Logitech SqueezeCenter CLI
(Telnet) Interface

Copyright (C) 2010 JingleManSweep <jinglemansweep [at] gmail [dot] com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import urllib

class Player(object):
    
    """
    SqueezeCenter Player
    """
    
    # internals
    
    def __init__(self, server=None, index=None, update=True):
        """
        Constructor
        """
        self.server = server
        self.logger = None
        self.index = None
        self.ref = None
        self.uuid = None
        self.name = None
        self.model = None
        self.ip_address = None
        self.is_connected = None
        self.is_player = None
        self.display_type = None
        self.can_power_off = None
        self.wifi_signal_strength = None        
        self.mode = None
        self.time = None
        self.power_state = None
        self.ir_state = None
        self.muting = None
        self.volume = None
        self.bass = None
        self.treble = None
        self.pitch = None
        self.rate = None
        self.mixing = None
        self.track_genre = None
        self.track_artist = None
        self.track_album = None
        self.track_title = None
        self.track_duration = None
        self.track_remote = None
        self.track_current_title = None
        self.track_path = None
        self.update(index, update=update)

    def __repr__(self):
        return "Player: %s" % (self.ref)
    
    def request(self, command_string, preserve_encoding=False):
        """Executes Telnet Request via SqueezeCenter"""
        return self.server.request("%s %s" % (self.ref, command_string), preserve_encoding)
    
    def update(self, index, update=True):
        """Update Player Properties from SqueezeCenter"""
        self.index = index
        self.ref = str(urllib.unquote(
            self.server.request("player id %i ?" % index)
        ))        
        self.name = str(urllib.unquote(
            self.server.request("player name %i ?" % index)
        )) 
        if update:
            self.uuid = str(urllib.unquote(
                self.server.request("player uuid %i ?" % index)
            ))
            self.ip_address = str(urllib.unquote(
                self.server.request("player ip %i ?" % index)
            ))    
            self.model = str(urllib.unquote(
                self.server.request("player model %i ?" % index)
            ))   
            self.display_type = str(urllib.unquote(
                self.server.request("player displaytype %i ?" % index)
            ))
            self.can_power_off = bool(urllib.unquote(
                self.server.request("player canpoweroff %i ?" % index)
            )) 
            self.is_player = bool(urllib.unquote(
                self.server.request("player isplayer %i ?" % index)
            )) 
            self.is_connected = bool(urllib.unquote(
                self.server.request("player connected %i ?" % index)
            )) 

    ## getters/setters

    def get_ref(self):
        """Get Player Ref"""
        return self.ref
    
    def get_uuid(self):
        """Get Player UUID"""
        return self.uuid

    def get_name(self):
        """Get Player Name"""
        return self.name

    def set_name(self, name):
        """Set Player Name"""
        self.request("name %s" % (name))
        self.update(self.index)
    
    def get_ip_address(self):
        """Get Player IP Address"""
        return self.ip_address
    
    def get_model(self):
        """Get Player Model String"""
        return self.model
    
    def get_display_type(self):
        """Get Player Display Type String"""
        return self.display_type
    
    def get_wifi_signal_strength(self):
        """Get Player WiFi Signal Strength"""
        self.wifi_signal_strength = self.request("signalstrength ?")
        return self.wifi_signal_strength

    def has_permission(self, request_terms):
        """Check Player User Permissions"""
        request_terms = urllib.quote(request_terms)
        granted = int(self.request("can %s ?" % (request_terms)))
        return (granted == 1)
    
    def get_pref_value(self, name, namespace=None):
        """Get Player Preference Value"""
        pref_string = ""
        if namespace:
            pref_string += namespace + ":"
        pref_string += name
        value = self.request("playerpref %s ?" % (pref_string))
        return value

    def set_pref_value(self, name, value, namespace=None):
        """Set Player Preference Value"""
        pref_string = ""
        if namespace:
            pref_string += namespace + ":"
        pref_string += name
        value = urllib.quote(value)
        valid = self.request("playerpref validate %s %s" % 
            (pref_string, value))
        if "valid:1" in valid:
            self.request("playerpref %s %s" % (pref_string, value))
            return True
        else:
            return False
    
    def get_mode(self):
        """Get Player Mode"""
        self.mode = str(self.request("mode ?"))
        return self.mode
    
    def get_time_elapsed(self):
        """Get Player Time Elapsed"""
        try:
            self.time = float(self.request("time ?"))
        except TypeError:
            self.time = float(0)
        return self.time
    
    def get_time_remaining(self):
        """Get Player Time Remaining"""
        if self.get_mode() == "play":
            remaining = self.get_track_duration() - self.get_time_elapsed()
            return remaining
        else:
            return 0
    
    def get_power_state(self):
        """Get Player Power State"""
        state = int(self.request("power ?"))
        self.power_state = (state != 0)
        return self.power_state
    
    def set_power_state(self, state):
        """Set Player Power State"""
        self.request("power %i" % (int(state)))
        self.get_power_state()    

    def get_ir_state(self):
        """Get Player Infrared State"""
        state = int(self.request("irenable ?"))
        self.ir_state = (state != 0)
        return self.ir_state

    def set_ir_state(self, state):
        """Set Player Power State"""
        self.request("irenable %i" % (int(state)))
        self.get_ir_state()   
               
    def get_volume(self):
        """Get Player Volume"""
        try:
            self.volume = int(self.request("mixer volume ?"))
        except TypeError:
            self.volume = -1
        return self.volume           

    def get_bass(self):
        """Get Player Bass"""
        self.bass = int(self.request("mixer bass ?"))
        return self.bass    

    def get_treble(self):
        """Get Player Treble"""
        self.treble = int(self.request("mixer treble ?"))
        return self.treble 

    def get_pitch(self):
        """Get Player Pitch"""
        self.pitch = int(self.request("mixer pitch ?"))
        return self.pitch
    
    def get_rate(self):
        """Get Player Rate"""
        self.rate = int(self.request("mixer rate ?"))
        return self.rate     

    def get_muting(self):
        """Get Player Muting Status"""
        state = int(self.request("mixer muting ?"))
        self.muting = (state != 0)
        return self.muting

    def set_muting(self, state):
        """Set Player Muting Status"""
        self.request("mixer muting %i" % (int(state)))
        self.get_muting()
    
    def get_track_genre(self):
        """Get Players Current Track Genre"""
        self.track_genre = str(self.request("genre ?"))
        return self.track_genre

    def get_track_artist(self):
        """Get Players Current Track Artist"""
        self.track_artist = str(self.request("artist ?"))
        return self.track_artist
    
    def get_track_album(self):
        """Get Players Current Track Album"""
        self.track_album = str(self.request("album ?"))
        return self.track_album
    
    def get_track_title(self):
        """Get Players Current Track Title"""
        self.track_title = str(self.request("title ?"))
        return self.track_title
    
    def get_track_duration(self):
        """Get Players Current Track Duration"""
        self.track_duration = float(self.request("duration ?"))
        return self.track_duration    
    
    def get_track_remote(self):
        """Is Players Current Track Remotely Hosted?"""
        remote = int(self.request("remote ?"))
        self.track_remote = (remote != 0)
        return self.track_remote  

    def get_track_current_title(self):
        """Get Players Current Track Current Title"""
        self.track_current_title = str(self.request("current_title ?"))
        return self.track_current_title

    def get_track_path(self):
        """Get Players Current Track Path"""
        self.track_path = str(self.request("path ?"))
        return self.track_path
    
    # playlist
    
    def playlist_play(self, item):
        """Play Item Immediately"""
        item = urllib.quote(item)
        self.request("playlist play %s" % (item))        

    def playlist_add(self, item):
        """Add Item To Playlist"""
        item = urllib.quote(item)
        self.request("playlist add %s" % (item))    
    
    def playlist_insert(self, item):
        """Insert Item Into Playlist (After Current Track)"""
        item = urllib.quote(item)
        self.request("playlist insert %s" % (item))

    def playlist_delete(self, item):
        """Delete Item From Playlist By Name"""
        item = urllib.quote(item)
        self.request("playlist deleteitem %s" % (item))
    
    def playlist_clear(self):
        """Clear the entire playlist. Will stop the player."""
	self.request("playlist clear")

    def playlist_move(self, from_index, to_index):
        """Move Item In Playlist"""
        self.request("playlist move %i %i" % (from_index, to_index))
 
    def playlist_erase(self, index):
        """Erase Item From Playlist"""
        self.request("playlist delete %i" % (index))
    
    def playlist_track_count(self):
        """Get the amount of tracks in the current playlist"""
	return int(self.request('playlist tracks ?'))
    
    def playlist_play_index(self, index):
        """Play track at a certain position in the current playlist (index is zero-based)"""
	return self.request('playlist index %i' % index)
    
    def playlist_get_info(self):
        """Get info about the tracks in the current playlist"""
        amount = self.playlist_track_count()
        response = self.request('status 0 %i' % amount, True)
        encoded_list = response.split('playlist%20index')[1:]
        playlist = []
        for encoded in encoded_list:
            data = [urllib.unquote(x) for x in ('position' + encoded).split(' ')]
            item = {}
            for info in data:
                info = info.split(':')
                key = info.pop(0)
                if key:
                    item[key] = ':'.join(info)
            item['position'] = int(item['position'])
            item['id'] = int(item['id'])
            item['duration'] = float(item['duration'])
            playlist.append(item)
        return playlist
    
    # actions
               
    def show(self, line1="", 
                   line2="", 
                   duration=3, 
                   brightness=4, 
                   font="standard", 
                   centered=False):
        """Displays text on Player display"""
        if font == "huge":
            line1 = ""
        line1, line2 = urllib.quote(line1), urllib.quote(line2)
        req_string = "show line1:%s line2:%s duration:%s "
        req_string += "brightness:%s font:%s centered:%i"
        self.request(req_string % 
                     (line1, line2, str(duration), str(brightness), font, int(centered)))

    def display(self, line1="",
                      line2="",
                      duration=3):
        line1, line2 = urllib.quote(line1), urllib.quote(line2)
        req_string = "display %s %s %s"
        self.request(req_string % 
                     (line1, line2, str(duration)))

    def play(self):
        """Play"""
        self.request("play")

    def stop(self):
        """Stop"""
        self.request("stop")

    def pause(self):
        """Pause On"""
        self.request("pause 1")

    def unpause(self):
        """Pause Off"""
        self.request("pause 0")

    def toggle(self):
        """Play/Pause Toggle"""
        self.request("pause")

    def next(self):
        """Next Track"""
        self.request("playlist jump +1")

    def prev(self):
        """Previous Track"""
        self.request("playlist jump -1")
    
    def set_volume(self, volume):
        """Set Player Volume"""
        try:
            volume = int(volume)            
            if volume < 0: 
                volume = 0
            if volume > 100: 
                volume = 100
            self.request("mixer volume %i" % (volume))
        except TypeError:
            pass

    def set_bass(self, bass):
        """Set Player Bass"""
        try:
            bass = int(bass)
            if bass < -100: 
                bass = -100
            if bass > 100: 
                bass = 100
            self.request("mixer bass %i" % (bass))
        except TypeError:
            pass

    def bass_up(self, amount=5):
        """Increase Player Bass"""
        self.request("mixer bass +%i" % (amount))
        self.get_bass()

    def bass_down(self, amount=5):
        """Decrease Player Bass"""
        try:
            amount = int(amount)            
            self.request("mixer bass -%i" % (amount))
            self.get_bass()
        except TypeError:
            pass

    def set_treble(self, treble):
        """Set Player Treble"""
        try:
            treble = int(treble)       
            if treble < -100:
                treble = -100
            if treble > 100:
                treble = 100
            self.request("mixer treble %i" % (treble))
        except TypeError:
            pass

    def treble_up(self, amount=5):
        """Increase Player Treble"""
        try:
            amount = int(amount)
            self.request("mixer treble +%i" % (amount))
            self.get_treble()
        except TypeError:
            pass

    def treble_down(self, amount=5):
        """Decrease Player Treble"""
        try:
            amount = int(amount)
            self.request("mixer treble -%i" % (amount))
            self.get_treble()
        except TypeError:
            pass

    def set_pitch(self, pitch):
        """Set Player Pitch"""
        try:
            pitch = int(pitch)
            if pitch < 80: 
                pitch = 80
            if pitch > 120: 
                pitch = 120
            self.request("mixer pitch %i" % (pitch))
        except TypeError:
            pass

    def pitch_up(self, amount=5):
        """Increase Player Pitch"""
        try:
            amount = int(amount)        
            self.request("mixer pitch +%i" % (amount))
            self.get_pitch()
        except TypeError:
            pass

    def pitch_down(self, amount=5):
        """Decrease Player Pitch"""
        try:
            amount = int(amount)  
            self.request("mixer pitch -%i" % (amount))
            self.get_pitch()
        except TypeError:
            pass

    def set_rate(self, rate):
        """Set Player Rate"""
        try:
            rate = int(rate)
            if rate < -4: 
                rate = 4
            if rate > 4: 
                rate = 4
            self.request("mixer rate %i" % (rate))
        except TypeError:
            pass

    def rate_up(self, amount=1):
        """Increase Player Rate"""
        try:
            amount = int(amount)
            self.request("mixer rate +%i" % (amount))
            self.get_rate()
        except TypeError:
            pass

    def rate_down(self, amount=1):
        """Decrease Player Rate"""
        try:
            amount = int(amount)
            self.request("mixer rate -%i" % (amount))
            self.get_rate()
        except TypeError:
            pass

    def volume_up(self, amount=5):
        """Increase Player Volume"""
        try:
            amount = int(amount)
            self.request("mixer volume +%i" % (amount))
            self.get_volume()
        except TypeError:
            pass

    def volume_down(self, amount=5):
        """Decrease Player Volume"""
        try:
            amount = int(amount)            
            self.request("mixer volume -%i" % (amount))
            self.get_volume()
        except TypeError:
            pass
    
    def mute(self):
        """Mute Player"""
        self.set_muting(True)
        
    def unmute(self):
        """Unmute Player"""
        self.set_muting(False)
    
    def seek_to(self, seconds):
        """Seek Player"""
        try:
            seconds = int(seconds)
            self.request("time %s" % (seconds))
        except TypeError:
            pass
        
    def forward(self, seconds=10):
        """Seek Player Forward"""
        try:
            seconds = int(seconds)
            self.request("time +%s" % (seconds))        
        except TypeError:
            pass

    def rewind(self, seconds=10):
        """Seek Player Backwards"""
        try:
            seconds = int(seconds)
            self.request("time -%s" % (seconds))   
        except TypeError:
            pass

    def ir_button(self, button):
        """Simulate IR Button Press"""
        self.request("button %s" % (button))   
