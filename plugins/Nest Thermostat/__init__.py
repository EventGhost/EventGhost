#Change Log --- CURRENT VERSION 1.2.0

#==================\
#1.2.0 - 2015/11/28\
#==================\
# Added:
# - Controls to allow the user to modify the state in which the HVAC is in
#
# Bugfixes:
# - AdjustTemp now works more appropriately
#==================\

#==================\
#1.1.0 - 2015/11/24\
#==================\
# Added:
# - Controls to allow the user to +/- temp if hvac mode == 'heat-cool'
# - Controls to allow the user to put the Nest into AWAY or HOME mode
#
# Bugfixes:
# - Disable TEST/OK/APPLY during invalid ConfigPanel states
# - Fixed EG crashing when trying to edit a CURRENT STATS action
#==================\

#==================\
#1.0.0 - 2015/11/20\
#==================\
# Initial Release!
# Features:
# - Supports Nest Thermostat device
# - Get Stats (w/ output to EG global)
# - Adjust Temperature (w/ output to EG global)
# == Set temperature to specific degree
# == Adjust temperature by 1-5 degrees UP/DOWN
#==================\

"""<rst>
**Notice:**
This plugin supports the Nest Thermostat device.

You will need the pyCurl librabry in order for this to run.

pyCurl: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl
WHL files can be installed on Windows via pip install [filename.whl]

If pip is not installed, this page can help:
http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows
"""

import eg

eg.RegisterPlugin(
    name = "Nest Thermostat",
    guid='{43095E8B-C9BF-49B7-AC59-F4966207433A}',
    author = "SupahNoob",
    version = "1.2.0",
    kind = "external",
    description = __doc__,
    url = "https://www.reddit.com/message/compose/?to=SupahNoob",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAA"
        "ACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAAF2+SX8VGAAADAFBMVEWS"
        "sLr////ExMXGycr////Iysutrq6VlpaGhoaGhoaVlpatrq7Iysv////GycrExMX////E"
        "xcXGyMnU2NmvsLF8fHxQUFA+Pj5SUlJTU1M/Pz9QUFB8fHyvsLHU2NnGyMnExcXGycrT"
        "2Nmmp6deXl40NDQxMTE4NzY3NjYxMTE0NDReXl6mp6fT2NnGycr///+wsbFeXl4xMTEz"
        "MjIzMjIxMTFeXl6wsbH////Iy8x+fn40NDQzMjIzMjI0NDR+fn7Iy8yvsLBSUlIxMTEx"
        "MTFSUlKvsLCYmZk9PT0yMjIyMjE9PT2YmZmMjIw3Nzc3NzeMjIyNjY43Nzc3NzeNjY6b"
        "nJw/Pz8yMjIyMjI/Pz+bnJyys7NYWFgxMTExMTFYWFiys7PExseIiIg3NzcyMjIyMjI3"
        "NzeIiIjEx8ff/f+ztbVsbG0zMzMyMjIyMjIzMzNsbG2ztbXf/f+4u7y+w8Strq5vb285"
        "OTkxMTEyMTEyMTExMTE5OTlvb2+trq6+w8S4u7y4ubm6vLy7v8CztLWPj5BiYmJGRkY9"
        "PT09PT1GRkZiYmKPj5CztLW7v8C4ubm2t7e1t7iuur67vb6ztLSkpaWam5yam5ykpaWz"
        "tLS7vb6uur61t7i2t7eSsLpmZGNnZWUzMzM2RUw5WWg5Wmk2Rk0zMzQ0Nzg9bIJHoclK"
        "rdtKrttHoco+b4U0ODkzMjI8Z3tKrdpKsN9Kr91Kr91KsN9Krts9an8zMzI1PkFGmL5K"
        "sd9Kr91Kr91Kr91Kr91KsN9Gm8E1P0QzMTE3S1RIp9JKr95Kr91Kr91Kr91Kr91Kr95J"
        "qdQ4TlgzMTEzMTE3SVFIptBKsN5Kr91Kr91Kr91Kr91KsN5Ip9I3TFUzMTE0OjxEkLNK"
        "seBKr91Kr91Kr91Kr91KseBFk7Y0Oz4zMjE6WGVIpc9KseBKsN5KsN5KseBIptE6Wmkz"
        "MjEzMzM5VmRDja9Io8xIo8xEjrA6WGYzMzQzMjE0ODo2RUs2RUw0OTszMjEyMTEyMTH/"
        "//+TT3ySAAAAn3RSTlMAAAAAAj6a2fLy2Zo+AgAAAAAAEobp////////6YYSAAAAEqb/"
        "/////////6YSAAKG////////hgI86f/////pPJb/////ltL/////0ur//+ro///ozv//"
        "///Oj/////+PN+X/////5TcBgf///////4EBABCk//////////+kEAAAABKJ7P//////"
        "/+yJEgAAAANDo+L9/eKjQwMAAADbXEJTAAAAAWJLR0T/pQfyxQAAAAlwSFlzAAALEwAA"
        "CxMBAJqcGAAAAAd0SU1FB98LEwQrFp9tLd4AAAEbSURBVBjTARAB7/4AAQIDBAUGBwgJ"
        "CgsMDQ4PEAAREhMUFRYXGBkaGxwdHh8gACEiIyQlJiefoCgpKissLS4ALzAxMjOhoqOk"
        "paY0NTY3OAA5Ojs8p6ipqqusra49Pj9AAEFCQ6+wsbKztLW2t7hERUYAR0hJubq7vL2+"
        "v8DBwkpLTABNTsPExcbHyMnKy8zNzk9QAFFSz9DR0tPU1dbX2NnaU1QAVVZX29zd3t/g"
        "4eLj5FhZWgBbXF3l5ufo6err7O3uXl9gAGFiY2Tv8PHy8/T19mVmZ2gAaWprbG33+Pn6"
        "+/xub3BxcgBzdHV2d3h5/f56e3x9fn+AAIGCg4SFhoeIiYqLjI2Ogo8AAJCRkpOUlZaX"
        "mJmam5ydnqXUfwSx5ibgAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE1LTExLTE5VDA0OjQz"
        "OjIyKzAxOjAwL/kFqgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNS0xMS0xOVQwNDo0Mzoy"
        "MiswMTowMF6kvRYAAAAASUVORK5CYII="
           ),
)

import os
import fileinput
import certifi
import string
import random
import wx
import json
import pycurl
import time
import StringIO
import requests
import re
from datetime import datetime, timedelta
from urllib import urlencode
from threading import Thread

def version_tuple(v):
    return tuple(map(int, (v.split("."))))

def secure_randomizer(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

class NestThermostat(eg.PluginBase):
    def OAuthDialog(self):
        dlg = wx.TextEntryDialog(None, 'Enter your PINCODE below...', 'Nest OAuth2 Setup')
        print "..."
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            if len(response) != 8:
                print "Incorrect PIN length entered, please try setup again.."
                dlg.Destroy()
            else:
                wd = os.getcwd()
                url = (  'https://api.home.nest.com/oauth2/access_token?client_id=eaf0d5f3-c043-429f-82b6-4a24767d5dbf'
                       + '&code=' + response + '&client_secret=EutnujN4SpedJykLat7c11GJB&grant_type=authorization_code')

                c = pycurl.Curl()
                c.setopt(pycurl.CAINFO, os.environ['REQUESTS_CA_BUNDLE'])
                c.setopt(pycurl.URL, url)
                tempbuff = StringIO.StringIO()
                c.setopt(pycurl.WRITEFUNCTION, tempbuff.write)

                post_data = {'code':response, 'client_id':'eaf0d5f3-c043-429f-82b6-4a24767d5dbf', 'client_secret':'EutnujN4SpedJykLat7c11GJB',
                             'grant_type':'authorization_code'}
                postfields = urlencode(post_data)
                c.setopt(pycurl.POSTFIELDS, postfields)

                c.perform()
                self._access_token = json.loads(tempbuff.getvalue())['access_token']
                c.close()

                return_dict = self.curl_read(command = ['structure_id', 'name', 'device_id', 'temperature_scale', 'postal_code', 'humidity',
                                                        'ambient_temperature_', 'target_temperature_', 'target_temperature_high_',
                                                        'target_temperature_low_', 'has_leaf', 'hvac_mode'])

                fdir = os.path.join(self._wd, 'plugins', 'Nest Thermostat')
                if not os.path.exists(fdir):
                    os.makedirs(fdir)
                with open(os.path.join(fdir, 'dict.json'), 'w') as g:
                    json.dump(return_dict, g)

                # Move PERM DATA to a new dictionary for purposes of recording to file - necessary in case EG closes and re-initializes.
                perm_data = ['structure_id', 'name', 'device_id', 'temperature_scale', 'postal_code']
                new_dict = {}
                for k in return_dict.keys():
                    if k in perm_data:
                        new_dict[k] = return_dict[k]

                # Write PERM DATA to file
                with open(self._wd + '\\plugins\\Nest Thermostat\\perm.json', 'w') as h:
                    json.dump(new_dict, h)

                self.structure_id = new_dict['structure_id']
                self.dev_name = new_dict['name']
                self.device_id = new_dict['device_id']
                self.temperature_scale = new_dict['temperature_scale']
                self.postal_code = new_dict['postal_code']

                # Write ACCESS TOKEN to file
                with open(self._wd + '\\plugins\\Nest Thermostat\\creds.txt', 'w') as f:
                    f.write(self._access_token)

                for x in xrange(0,2):
                    print " "
                print "Success! You can now move to the options."
                for x in xrange(0,2):
                    print " "
        else:
            print "Setup cancelled ..."
        dlg.Destroy()

    def curl_write(self, command):
        # command = {}
        counter = 0

        write_data = '{'
        for k, v in command.items():
            if counter != 0:
                write_data += ', '
            counter += 1

            if type(v) == int:
                write_data += '"{0}": {1}'.format(k, v)
            else:
                write_data += '"{0}": "{1}"'.format(k, v)
        else:
            write_data += '}'

        if command.keys()[0] in ['away', 'trip_id', 'estimated_arrival_window_begin', 'estimated_arrival_window_end']:
            url = 'https://developer-api.nest.com/structures/{0}?auth={1}'.format(self.structure_id, self._access_token)
            if command.keys()[0] != ['away']:
                write_data = '{"eta": {0}}'.format(write_data)
        else:
            url = 'https://developer-api.nest.com/devices/thermostats/{0}?auth={1}'.format(self.device_id, self._access_token)

        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, os.environ['REQUESTS_CA_BUNDLE'])
        c.setopt(c.URL, url)
        c.setopt(c.CUSTOMREQUEST, "PUT")
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, write_data)
        c.setopt(c.HTTPHEADER, [
            'Content-Type: application/json'
            ])
        c.setopt(c.FOLLOWLOCATION, True)

        tempbuff = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, tempbuff.write)

        c.perform()
        api_response = json.loads(tempbuff.getvalue())
        c.close()

        eg.globals.Nest_currTemp = self.curr_temp

        try:
            test = api_response['error']
            return api_response
        except KeyError:
            if 'target_temperature_' + self.temperature_scale in api_response:
                self.tar_temp = api_response['target_temperature_' + self.temperature_scale]
            if 'target_temperature_high_' + self.temperature_scale in api_response:
                self.tar_temp_high = api_response['target_temperature_high_' + self.temperature_scale]
            if 'target_temperature_low_' + self.temperature_scale in api_response:
                self.tar_temp_low = api_response['target_temperature_low_' + self.temperature_scale]
            if 'away' in api_response:
                self.away = api_response['away']
            if 'eta' in api_response:
                self.eta_id = api_response['eta']['trip_id']
                self.eta_start = api_response['eta']['estimated_arrival_window_begin']
                self.eta_end = api_response['eta']['estimated_arrival_window_end']
            return api_response

    def curl_read(self, command):
        # command = []

        url = 'https://developer-api.nest.com/'
        thermo_id = []

        temp_dict = dict.fromkeys(command, 0)

        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, [
            'Authorization: Bearer %s' % str(self._access_token),
            'Accept: application/json'
            ])
        c.setopt(pycurl.FOLLOWLOCATION, True)

        tempbuff = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, tempbuff.write)
        c.perform()
        api_response = json.loads(tempbuff.getvalue())
        c.close()

        if 'message' in api_response and api_response['message'] == 'unauthorized':
            self.PrintError('Unauthorized: ' + api_response.get('type', ''))
            return temp_dict

        for i in api_response['devices']['thermostats']:
            thermo_id.append(i)
            units = api_response['devices']['thermostats'][i]['temperature_scale'].lower()

        for w in command:
            if w == 'temperature_scale':
                temp_dict[w] = units
            elif w in ['away', 'postal_code']:
                for x in api_response['structures']:
                    temp_dict[w] = api_response['structures'][x][w]
            else:
                if w.endswith('_'):
                    del temp_dict[w]
                    w += units
                for n in thermo_id:
                    temp_dict[w] = api_response['devices']['thermostats'][n][w]

        eg.globals.Nest_currTemp = self.curr_temp

        return temp_dict

    def get_configpanel_stats(self):
        try:
            with open(self._wd + '\\plugins\\Nest Thermostat\\dict.json', 'r') as g:
                try:
                    temp_dict = json.load(g)
                except ValueError:
                    pass
            os.remove(self._wd + '\\plugins\\Nest Thermostat\\dict.json')
        except IOError:
            temp_dict = self.curl_read(command = ['humidity', 'ambient_temperature_', 'target_temperature_', 'target_temperature_high_',
                                                  'target_temperature_low_', 'has_leaf', 'hvac_mode'])

        self.curr_temp = temp_dict.get('ambient_temperature_' + str(self.temperature_scale), 0)
        self.tar_temp = temp_dict.get('target_temperature_' + str(self.temperature_scale), 0)
        self.tar_temp_low = temp_dict.get('target_temperature_low_' + str(self.temperature_scale), 0)
        self.tar_temp_high = temp_dict.get('target_temperature_high_' + str(self.temperature_scale), 0)
        self.humidity = temp_dict['humidity']
        self.hvac_mode = temp_dict['hvac_mode']

    def print_errors(self, resp):
        try:
            if resp['type'] == 'https://developer.nest.com/documentation/cloud/error-messages#blocked':
                print "We've hit the rate limit for calls to the Nest."
                print "This is a API call limit that I hope to work around soon."
                print "For now, please try to make the least amount of calls possible."
            elif resp['type'] in ['https://developer.nest.com/documentation/cloud/error-messages#internal-error',
                                  'https://developer.nest.com/documentation/cloud/error-messages#forbidden',
                                  'https://developer.nest.com/documentation/cloud/error-messages#service-unavailable']:
                print "The Nest service seems to be having issues ..."
                time.sleep(1)
                print "Opening the Nest System Status webpage now ..."
                time.sleep(.5)
                wx.LaunchDefaultBrowser('https://nest.com/support/article/software-update-issue#status')
            elif resp['type'] == 'https://developer.nest.com/documentation/cloud/error-messages#auth-error':
                print "For whatever reason, your Auth Token is not valid."
                print "Please re-do in the EventGhost Nest plugin panel."
            elif resp['type'] in ['https://developer.nest.com/documentation/cloud/error-messages#mode-error',
                                  'https://developer.nest.com/documentation/cloud/error-messages#range-error',
                                  'https://developer.nest.com/documentation/cloud/error-messages#low-c-value',
                                  'https://developer.nest.com/documentation/cloud/error-messages#high-c-value',
                                  'https://developer.nest.com/documentation/cloud/error-messages#low-f-value',
                                  'https://developer.nest.com/documentation/cloud/error-messages#high-f-value',
                                  'https://developer.nest.com/documentation/cloud/error-messages#low-high-error']:
                print resp['message'] + '.'
            return True
        except (KeyError, TypeError):
            return False

    def UpgradePlugin(self):
        re_version = re.compile(ur'<em>v([^\"]+)</em>')
        eg_post = 'http://www.eventghost.net/forum/viewtopic.php?f=9&t=7750'
        r = requests.get(eg_post)
        remoteVersion = re_version.search(r.text).groups(1)[0]

        if version_tuple(self.info.version) >= version_tuple(remoteVersion):
            print "Nest Plugin is up to date!"
        else:
            print "There is a new version (v{0}) of this plugin available!".format(remoteVersion)
            print "Please copy and paste the link below into your browser."
            print eg_post

    def __init__(self):
        Thread(target = self.UpgradePlugin).start()

        self._wd = os.getcwd()
        self._pid = 'eaf0d5f3-c043-429f-82b6-4a24767d5dbf'
        self._sec = 'EutnujN4SpedJykLat7c11GJB'

        if os.path.isfile(self._wd + '\\plugins\\Nest Thermostat\\creds.txt'):
            if os.stat(self._wd + '\\plugins\\Nest Thermostat\\creds.txt').st_size == 0:
                self._access_token = ''
            else:
                with open(self._wd + '\\plugins\\Nest Thermostat\\creds.txt', "r") as f:
                    self._access_token = f.read()
        else:
            self._access_token = ''

        self.last_write_call = datetime.now()

        self.structure_id = ''
        self.dev_name = ''
        self.device_id = ''
        self.temperature_scale = ''
        self.postal_code = ''

        self.curr_temp = ''
        self.hvac_mode = ''
        self.tar_temp = ''
        self.tar_temp_low = ''
        self.tar_temp_high = ''
        self.humidity = ''
        self.away = ''
        self.eta_id = ''
        self.eta_start = ''
        self.eta_end = ''

        self.AddAction(GetStats)
        self.AddAction(AdjustTemp)
        self.AddAction(SetAway)
        self.AddAction(SetHVACState)
        #self.AddAction(ETACall)

    def Configure(self):
        # need to add OVERRIDE option in case of incorrect ACCESS TOKEN / new account

        panel = eg.ConfigPanel()

        conf_title = panel.StaticText("There are currently no setup in this panel that you need to set.")
        conf_notice = panel.StaticText('Press "OK" to being the Authorization process.')
        vers_ind = panel.StaticText("version " + self.info.version)
        empty_space = panel.StaticText("\n\n\n")
        empty_space2 = panel.StaticText("\n\n")

        if self._access_token == '':
            conf_title.Show(False)
            titleBox = panel.BoxedGroup(
                "Notice", conf_notice)
        else:
            conf_notice.Show(False)
            titleBox = panel.BoxedGroup(
            "Notice", conf_title)

        panel.sizer.AddMany([
            (empty_space, 0, wx.ALIGN_CENTER),
            (titleBox, 0, wx.ALIGN_CENTER),
            (empty_space2, 0, wx.ALIGN_CENTER),
            (vers_ind, 0, wx.BOTTOM | wx.ALIGN_LEFT)
             ])

        while panel.Affirmed():
          panel.SetResult(
            )

    def __start__(self):
        if len(self._access_token) == 0:
            print "Making initial call to Nest platform for authentication..."

            # REQUEST AUTH TO NEST ACCT
            url = 'https://home.nest.com/login/oauth2?client_id=eaf0d5f3-c043-429f-82b6-4a24767d5dbf&state=STATE'
            wx.LaunchDefaultBrowser(url)

            # Create OAuth Dialog box
            wx.CallAfter(self.OAuthDialog)
        else:
            print "Welcome back ... your Nest is set up and ready to go!"

            fdir = os.path.join(self._wd, 'plugins', 'Nest Thermostat')
            if not os.path.exists(fdir):
                os.makedirs(fdir)
            with open(os.path.join(fdir, 'perm.json'), 'r') as h:
                temp_dict = json.load(h)
                self.structure_id = temp_dict['structure_id']
                self.dev_name = temp_dict['name']
                self.device_id = temp_dict['device_id']
                self.temperature_scale = temp_dict['temperature_scale']
                self.postal_code = temp_dict['postal_code']

            return_dict = self.curl_read(command=['humidity', 'ambient_temperature_', 'target_temperature_', 'target_temperature_high_', 'target_temperature_low_', 'has_leaf', 'hvac_mode'])

            with open(self._wd + '\\plugins\\Nest Thermostat\\dict.json', 'w') as g:
                json.dump(return_dict, g)

#===================================================================================================================================================#
#===================================================================================================================================================#

class GetStats(eg.ActionBase):
    name = "Get Current Stats"
    description = "Show stats like Current Temperature, Target Temperature, Current Humidity, etc."

    def Configure(self, *args):
        panel = eg.ConfigPanel(self)

        # SETUP CALL for config panel / refresh values
        self.plugin.get_configpanel_stats()

        gs_title = panel.StaticText("On this panel, you will find multiple checkboxes to")
        gs_title2 = panel.StaticText("indicate which stats are to be read from your thermostat.")
        gs_footer = panel.StaticText("eg.globals.Nest_getStats")
        dev_name = panel.CheckBox(0, " Thermostat Name", style=wx.CHK_3STATE)
        cHum = panel.CheckBox(0, " Current Humidity", style=wx.CHK_3STATE)
        cTemp = panel.CheckBox(-1, " Current Temp", style=wx.CHK_3STATE)
        tTemp = panel.CheckBox(0, " Target Temp", style=wx.CHK_3STATE)
        thTemp = panel.CheckBox(0, " Target High Temp", style=wx.CHK_3STATE)
        tlTemp = panel.CheckBox(0, " Target Low Temp", style=wx.CHK_3STATE)
        leaf = panel.CheckBox(0, " Has Leaf", style=wx.CHK_3STATE)

        if self.plugin.hvac_mode == 'heat-cool':
            tTemp.Show(False)
        else:
            thTemp.Show(False)
            tlTemp.Show(False)

        currentBox = panel.BoxedGroup(
            "Current Data", (cTemp, cHum))

        if self.plugin.hvac_mode == 'heat-cool':
            targetBox = panel.BoxedGroup(
                "Target Temps", (tlTemp, thTemp))
        else:
            targetBox = panel.BoxedGroup(
                "Target Temp", tTemp)

        miscBox = panel.BoxedGroup(
            "Misc. Data", (dev_name, leaf))

        eg.EqualizeWidths((cTemp, cHum, tTemp, thTemp, tlTemp, dev_name, leaf))

        panel.sizer.AddMany([
            (gs_title, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (gs_title2, 1, wx.ALIGN_CENTER_HORIZONTAL),
            (currentBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (targetBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (miscBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (gs_footer, 0, wx.BOTTOM | wx.ALIGN_RIGHT)
             ])

        def OnCheckBox(event):
            dev_name.Get3StateValue()
            cHum.Get3StateValue()
            cTemp.Get3StateValue()
            tTemp.Get3StateValue()
            thTemp.Get3StateValue()
            tlTemp.Get3StateValue()
            leaf.Get3StateValue()

            if self.plugin.hvac_mode == 'heat-cool':
                if (  dev_name.Get3StateValue() + cHum.Get3StateValue() + cTemp.Get3StateValue() + thTemp.Get3StateValue()
                    + tlTemp.Get3StateValue() + leaf.Get3StateValue()) == 0:
                    panel.EnableButtons(False)
                else:
                    panel.EnableButtons(True)
            else:
                if (  dev_name.Get3StateValue() + cHum.Get3StateValue() + cTemp.Get3StateValue()
                    + tTemp.Get3StateValue() + leaf.Get3StateValue()) == 0:
                    panel.EnableButtons(False)
                else:
                    panel.EnableButtons(True)

        dev_name.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        cHum.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        cTemp.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        tTemp.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        thTemp.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        tlTemp.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        leaf.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():
          panel.SetResult(
            dev_name.Get3StateValue(),
            cHum.Get3StateValue(),
            cTemp.Get3StateValue(),
            tTemp.Get3StateValue(),
            thTemp.Get3StateValue(),
            tlTemp.Get3StateValue(),
            leaf.Get3StateValue()
            )

    def GetLabel(self, dev_name, cHum, cTemp, tTemp, thTemp, tlTemp, leaf):
        return "Current Stats: Execute to see!"

    def __call__(self, dev_name, cHum, cTemp, tTemp, thTemp, tlTemp, leaf):
        commands = []

        cmds = []
        cmds.append(['name', dev_name])
        cmds.append(['humidity', cHum])
        cmds.append(['ambient_temperature_' + str(self.plugin.temperature_scale), cTemp])
        cmds.append(['target_temperature_' + str(self.plugin.temperature_scale), tTemp])
        cmds.append(['target_temperature_high_' + str(self.plugin.temperature_scale), thTemp])
        cmds.append(['target_temperature_low_' + str(self.plugin.temperature_scale), tlTemp])
        cmds.append(['has_leaf', leaf])

        for x in cmds:
            if x[1] != 0:
                commands.append(x[0])

        resp = self.plugin.curl_read(commands)
        eg.globals.Nest_getStats = resp

        if not self.plugin.print_errors(resp):
            for k, v in resp.items():
                if k == 'name':
                    print "Your device's name is {0}".format(v)
                if k == 'humidity':
                    print "The humidity is currently {0}%".format(v)
                    self.plugin.humidity = v
                if k == 'ambient_temperature_' + self.plugin.temperature_scale:
                    print "It's currently {0}{1} in here.".format(v, self.plugin.temperature_scale)
                    self.plugin.curr_temp = v
                if k == 'target_temperature_' + self.plugin.temperature_scale:
                    print "The target temperature is {0}{1}".format(v, self.plugin.temperature_scale)
                    self.plugin.tar_temp = v
                if k == 'target_temperature_high_' + self.plugin.temperature_scale:
                    print "The target HIGH temperature is {0}{1}".format(v, self.plugin.temperature_scale)
                    self.plugin.tar_temp_high = v
                if k == 'target_temperature_low_' + self.plugin.temperature_scale:
                    print "The target LOW temperature is {0}{1}".format(v, self.plugin.temperature_scale)
                    self.plugin.tar_temp_low = v
                if k == 'has_leaf':
                    if v == 'true':
                        print "You're currently saving enough energy to achieve a Leaf! :)"
                    else:
                        print "You're not currently saving enough energy to achieve a Nest Leaf. :("

#===================================================================================================================================================#
#===================================================================================================================================================#

class AdjustTemp(eg.ActionBase):
    name = "Change Temperature"
    description = "Set/Adjust the current target temperatures."

    def Configure(self, *args):
        panel = eg.ConfigPanel(self)

        # SETUP CALL for config panel / refresh values
        self.plugin.get_configpanel_stats()

        at_title = panel.StaticText("On this panel, you are able to set various temperature indicators.")
        at_footer = panel.StaticText("eg.globals.Nest_setTemp")

        adjust_temp = panel.CheckBox(0)
        adj_direction = panel.Choice(2, ['Up', 'Down'])
        adj_amount = panel.SpinIntCtrl(0, min=1, max=5)

        if self.plugin.temperature_scale == 'f':
            tar_temp_high = panel.SpinIntCtrl(value=self.plugin.tar_temp_high, min=50, max=90)
            tar_temp_low = panel.SpinIntCtrl(value=self.plugin.tar_temp_low, min=50, max=90)
            tar_temp = panel.SpinIntCtrl(value=self.plugin.curr_temp, min=50, max=90)
        else:  # self.plugin.temperature_scale == 'c':
            tar_temp_high = panel.SpinIntCtrl(value=self.plugin.tar_temp_high, min=9, max=32)
            tar_temp_low = panel.SpinIntCtrl(value=self.plugin.tar_temp_low, min=9, max=32)
            tar_temp = panel.SpinIntCtrl(value=self.plugin.curr_temp, min=9, max=32)

        if self.plugin.hvac_mode == 'heat-cool':
            tar_temp.Show(False)
        else:
            tar_temp_high.Show(False)
            tar_temp_low.Show(False)

        if self.plugin.hvac_mode == 'heat-cool':
            tempBox = panel.BoxedGroup(
                "Set a Temperature Range", (tar_temp_low, tar_temp_high))
        else:
            tempBox = panel.BoxedGroup(
                "Set the Temp", tar_temp)

        directionBox = panel.BoxedGroup(
            "Adjust Temp by Amount", (adjust_temp, adj_direction, adj_amount))

        eg.EqualizeWidths((tar_temp_low, tar_temp_high, tar_temp, adj_direction, adj_amount))

        panel.sizer.AddMany([
            (at_title, 1, wx.ALIGN_CENTER_HORIZONTAL),
            (tempBox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL),
            (directionBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (at_footer, 0, wx.BOTTOM | wx.ALIGN_RIGHT)
             ])

        adj_direction.Enable(adjust_temp.GetValue())
        adj_amount.Enable(adjust_temp.GetValue())

        def OnCheckBox(event):
            flag = adjust_temp.GetValue()
            adj_direction.Enable(flag)

            if not flag:
                adj_direction.SetValue(-1)
                adj_amount.Enable(flag)
                panel.EnableButtons(not flag)
            else:
                panel.EnableButtons(not flag)

            if self.plugin.hvac_mode == 'heat-cool':
                tar_temp_high.GetValue()
                tar_temp_low.GetValue()
                tar_temp_high.Enable(not flag)
                tar_temp_low.Enable(not flag)
                tar_temp_high.SetValue(self.plugin.tar_temp_high)
                tar_temp_low.SetValue(self.plugin.tar_temp_low)
            else:
                tar_temp.GetValue()
                tar_temp.Enable(not flag)
                if flag:
                    tar_temp.SetValue(self.plugin.tar_temp)
                else:
                    tar_temp.SetValue(self.plugin.curr_temp)

        def OnEventChoice(event):
            panel.EnableButtons(True)
            adj_amount.Enable(True)

        adjust_temp.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        adj_direction.Bind(wx.EVT_CHOICE, OnEventChoice)

        while panel.Affirmed():
            panel.SetResult(
                tar_temp.GetValue(),
                tar_temp_high.GetValue(),
                tar_temp_low.GetValue(),
                adjust_temp.GetValue(),
                adj_direction.GetValue(),
                adj_amount.GetValue(),
                )

    def GetLabel(self, tar_temp, tar_temp_high, tar_temp_low, adjust_temp, adj_direction, adj_amount):
        if adjust_temp:
            if adj_direction == 0: #Up
                return "Turn up by {0}".format(adj_amount)
            elif adj_direction == 1: #Down
                return "Turn down by {0}".format(adj_amount)
        else:
            if self.plugin.hvac_mode == 'heat-cool':
                return "Set to {0} - {1}".format(tar_temp_low, tar_temp_high)
            else:
                if tar_temp != self.plugin.tar_temp:
                    return "Set to {0}".format(tar_temp)

    def __call__(self, tar_temp, tar_temp_high, tar_temp_low, adjust_temp, adj_direction, adj_amount):
        write_commands = {}
        tdelta = datetime.now() - self.plugin.last_write_call
        if tdelta >= timedelta(minutes = 5):
            recent_call = False
            self.plugin.last_write_call = datetime.now()
        else:
            recent_call = True

        if adjust_temp:
            if self.plugin.hvac_mode == 'heat-cool':
                if adj_direction == 0:
                    if recent_call:
                        write_commands['target_temperature_low_' + self.plugin.temperature_scale] = self.plugin.tar_temp_low + adj_amount
                        if self.plugin.tar_temp_high < self.plugin.curr_temp + adj_amount + 3:
                            write_commands['target_temperature_high_' + self.plugin.temperature_scale] = self.plugin.tar_temp_high + adj_amount + 3
                    else:
                        write_commands['target_temperature_low_' + self.plugin.temperature_scale] = self.plugin.curr_temp + adj_amount
                        if self.plugin.tar_temp_high < self.plugin.curr_temp + adj_amount + 3:
                            write_commands['target_temperature_high_' + self.plugin.temperature_scale] = self.plugin.curr_temp + adj_amount + 3
                elif adj_direction == 1:
                    if recent_call:
                        write_commands['target_temperature_high_' + self.plugin.temperature_scale] = self.plugin.tar_temp_high - adj_amount
                        if self.plugin.tar_temp_low > self.plugin.curr_temp - adj_amount - 3:
                            write_commands['target_temperature_low_' + self.plugin.temperature_scale] = self.plugin.tar_temp_low - adj_amount - 3
                    else:
                        write_commands['target_temperature_high_' + self.plugin.temperature_scale] = self.plugin.curr_temp - adj_amount
                        if self.plugin.tar_temp_low > self.plugin.curr_temp - adj_amount - 3:
                            write_commands['target_temperature_low_' + self.plugin.temperature_scale] = self.plugin.curr_temp - adj_amount - 3
            else:
                if adj_direction == 0: #Up
                    if recent_call:
                        write_commands['target_temperature_' + self.plugin.temperature_scale] = self.plugin.tar_temp + adj_amount
                    else:
                        write_commands['target_temperature_' + self.plugin.temperature_scale] = self.plugin.curr_temp + adj_amount
                elif adj_direction == 1: #Down
                    if recent_call:
                        write_commands['target_temperature_' + self.plugin.temperature_scale] = self.plugin.tar_temp - adj_amount
                    else:
                        write_commands['target_temperature_' + self.plugin.temperature_scale] = self.plugin.curr_temp - adj_amount

        if write_commands == {}:
            print "\nNo command was executed, these changes are unnecessary.\n"
        else:
            resp = self.plugin.curl_write(write_commands)
            eg.globals.Nest_setTemp = resp

            if not self.plugin.print_errors(resp):
                for k, v in resp.items():
                        if adjust_temp:
                            if adj_direction == 0:
                                if k == 'target_temperature_low_' + self.plugin.temperature_scale:
                                    print "Target LOW temperature increased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                                elif k == 'target_temperature_high_' + self.plugin.temperature_scale:
                                    print "Target HIGH temperature increased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                                else:
                                    print "Target temperature increased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                            if adj_direction == 1:
                                if k == 'target_temperature_low_' + self.plugin.temperature_scale:
                                    print "Target LOW temperature increased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                                elif k == 'target_temperature_high_' + self.plugin.temperature_scale:
                                    print "Target HIGH temperature increased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                                else:
                                    print "Target temperature decreased by {0}{2} to {1}{2}.".format(adj_amount, v, self.plugin.temperature_scale.upper())
                        else:
                            if k == 'target_temperature_' + self.plugin.temperature_scale:
                                print "Target temperature set to {0}{1}.".format(v, self.plugin.temperature_scale.upper())
                            if k == 'target_temperature_low_' + self.plugin.temperature_scale:
                                print "Target LOW temperature set to {0}{1}.".format(v, self.plugin.temperature_scale.upper())
                            if k == 'target_temperature_high_' + self.plugin.temperature_scale:
                                print "Target HIGH temperature set to {0}{1}.".format(v, self.plugin.temperature_scale.upper())

#===================================================================================================================================================#
#===================================================================================================================================================#

class SetAway(eg.ActionBase):
    name = "Adjust Away"
    description = "Set AWAY mode to 'Home' or 'Away'"

    def Configure(self, *args):
        panel = eg.ConfigPanel(self)

        # SETUP CALL for config panel / refresh values
        self.plugin.get_configpanel_stats()

        if self.plugin.away == 'home':
            home_val = -1
            away_val = 0
        else:
            home_val = 0
            away_val = -1

        aa_title = panel.StaticText("On this panel, you are able to set whether you are away or not.")
        aa_footer = panel.StaticText("eg.globals.Nest_setAway")

        aa_spacer1 = panel.StaticText(' ')
        aa_spacer2 = panel.StaticText(' ')

        set_Home = panel.RadioButton(home_val, label='Home')
        set_Away = panel.RadioButton(away_val, label='Away')

        awayBox = panel.BoxedGroup(
            "Set Away Value", (set_Home, set_Away))

        panel.sizer.AddMany([
            (aa_title, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (aa_spacer1, 1),
            (awayBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (aa_spacer2, 1),
            (aa_footer, 0, wx.BOTTOM | wx.ALIGN_RIGHT)
             ])

        eg.EqualizeWidths((set_Home, set_Away))

        while panel.Affirmed():
            panel.SetResult(
                set_Home.GetValue(),
                set_Away.GetValue(),
                )

    def GetLabel(self, set_Home, set_Away):
        if set_Home == 1:
            return "Set to HOME"
        if set_Away == 1:
            return "Set to AWAY"

    def __call__(self, set_Home, set_Away):
        write_commands = {}

        if set_Home == 1:
            write_commands['away'] = 'home'
        if set_Away == 1:
            write_commands['away'] = 'away'

        resp = self.plugin.curl_write(write_commands)
        eg.globals.Nest_setAway = resp

        if not self.plugin.print_errors(resp):
            if set_Home == 1:
                print "You are now marked as 'HOME'."
            if set_Away == 1:
                print "You are now marked as 'AWAY'."

#===================================================================================================================================================#
#===================================================================================================================================================#

class SetHVACState(eg.ActionBase):
    name = "Set HVAC State"
    description = "Set the HVAC mode to 'Cool', 'Heat', or 'Heat-Cool'."

    def Configure(self, *args):
        panel = eg.ConfigPanel(self)

        # SETUP CALL for config panel / refresh values
        self.plugin.get_configpanel_stats()

        if self.plugin.hvac_mode == 'cool':
            cool_val = -1
            heat_val = 0
            heatcool_val = 0
            sh_indicator = panel.StaticText("HVAC mode is currently set to COOL")
        elif self.plugin.hvac_mode == 'heat':
            cool_val = 0
            heat_val = -1
            heatcool_val = 0
            sh_indicator = panel.StaticText("HVAC mode is currently set to HEAT")
        else:
            cool_val = 0
            heat_val = 0
            heatcool_val = -1
            sh_indicator = panel.StaticText("HVAC mode is currently set to HEAT-COOL")

        sh_title = panel.StaticText("On this panel, you are able to set the HVAC to one of three states.")
        sh_footer = panel.StaticText("eg.globals.Nest_setHVAC")

        sh_spacer1 = panel.StaticText(' ')
        sh_spacer2 = panel.StaticText(' ')
        sh_spacer3 = panel.StaticText(' ')

        set_Cool = panel.RadioButton(cool_val, label='Cool')
        set_Heat = panel.RadioButton(heat_val, label='Heat')
        set_HeatCool = panel.RadioButton(heatcool_val, label='Heat-Cool')

        hvacBox = panel.BoxedGroup(
            "Set HVAC Mode", (set_Cool, set_Heat, set_HeatCool))

        panel.sizer.AddMany([
            (sh_title, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (sh_spacer1, 1),
            (sh_indicator, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (sh_spacer2, 1),
            (hvacBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (sh_spacer3, 1),
            (sh_footer, 0, wx.BOTTOM | wx.ALIGN_RIGHT)
             ])

        eg.EqualizeWidths((set_Cool, set_Heat, set_HeatCool))

        while panel.Affirmed():
            panel.SetResult(
                set_Cool.GetValue(),
                set_Heat.GetValue(),
                set_HeatCool.GetValue()
                )

    def GetLabel(self, set_Cool, set_Heat, set_HeatCool):
        if set_Cool == 1:
            return "Set HVAC to 'Cool'"
        if set_Heat == 1:
            return "Set HVAC to 'Heat'"
        if set_HeatCool == 1:
            return "Set HVAC to 'Heat-Cool'"

    def __call__(self, set_Cool, set_Heat, set_HeatCool):
        write_commands = {}

        if set_Cool == 1:
            write_commands['hvac_mode'] = 'cool'
        if set_Heat == 1:
            write_commands['hvac_mode'] = 'heat'
        if set_HeatCool == 1:
            write_commands['hvac_mode'] = 'heat-cool'

        resp = self.plugin.curl_write(write_commands)
        eg.globals.Nest_setHVAC = resp

        if not self.plugin.print_errors(resp):
            if set_Cool == 1:
                print "You have now marked the HVAC to be in COOL mode."
            if set_Heat == 1:
                print "You have now marked the HVAC to be in HEAT mode."
            if set_HeatCool == 1:
                print "You have now marked the HVAC to be in HEAT-COOL mode."

#===================================================================================================================================================#
#===================================================================================================================================================#

#class ETACall(eg.ActionBase):
#    def Configure(self, *args):
#        panel = eg.ConfigPanel(self)
#
#        *NOTE* - If the away mode isn't set to AWAY, ETACall has no effect, thus, you must run an AWAY action if you want to schedule this.
#               - "SCHEDULE TIME" is the equivalent of "In X minutes"?
#
#        TO DO: Radio Buttons to use eg.event.payload OR schedule ETA time
#        TO DO: IMG to show how to use based on eg.event.payload?

#    def __call__(self):
#        TO DO: VariableCMD eta call
#        TO DO: https://developer.nest.com/documentation/cloud/eta-reference
#        TO DO: write_commands['trip_id'] = secure_randomizer(6)
#        TO DO: write_commands['estimated_arrival_window_begin'] = TIMEZONE DATA ('2015-10-31T22:42:59.000Z') ISO 8601 FORMAT
#        TO DO: write_commands['estimated_arrival_window_end'] = TIMEZONE DATA ('2015-10-31T23:59:59.000Z') ISO 8601 FORMAT
