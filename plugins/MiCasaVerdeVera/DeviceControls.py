# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, 


import xml.etree.ElementTree as ET
from copy import deepcopy as dc


class Database(object):

    def __init__(self, new, old):
        self.new = new
        self.old = old
        self.newkeys = set(new.keys())
        self.oldkeys = set(old.keys())
        self.matches = self.newkeys.intersection(self.oldkeys)
        self.res = dict(NewData=self.new, OldData=self.old, ChangedData=self.new)

    def Added(self):
        if self.newkeys - self.matches: return dc(self.res)
        else: return None
    def Removed(self):
        if self.oldkeys - self.matches: return dc(self.res)
        else: return None
    def Changed(self):
        res = [[o, self.new[o]] for o in self.matches if self.old[o] != self.new[o]]
        self.res['ChangedData'] = dict(res)
        if res: return dc(self.res)
        else: return None

class VDL:

    def __init__(self, plugin, STATIC):
        self.CATEGORIES = STATIC.CATEGORIES
        self.ALLOWEDEVENTS = STATIC.ALLOWEDEVENTS
        self.plugin = plugin

    def start(self):
        self.system = []
        self.sections = []
        self.categories = []
        self.rooms = []
        self.devices = []
        self.scenes = []

    def Length(self, one, two):
        one += [{}]*(len(two)-len(one)) if len(two) > len(one) else []
        return one

    def TriggerEvent(self, payload, eventdata):
        olddata = payload.pop('OldData')
        newdata = payload.pop('NewData')
        changeddata = payload.pop('ChangedData')

        d = dc(newdata)
        if not d: d = dc(olddata)
        try: name = d.pop('name')
        except: name = None
        try: room = d.pop('room')
        except: room = None

        roomname = self.GetRoom(room)
        sectionname = self.GetSection(room)
        cat = d.pop('category')
        catname = self.GetCategory(cat)
        events  = [sectionname] if sectionname else []
        events += [roomname] if roomname else []
        events += [name] if name else ['ID-'+str(d.pop('id'))]

        def triggerevent(suffix):
            self.plugin.TriggerEvent(suffix='.'.join(suffix), payload=dc(newdata))

        if eventdata is None:
            eventdata = []
            events += [catname] if catname else []
            keys = sorted(changeddata.keys())
            event = [self.GetEvent(cat, key) for key in keys]
            for i, evt in enumerate(event):
                if evt is None: continue
                val = str(changeddata[keys[i]])
                if isinstance(evt[0], list):
                    eventdata += [[evt[0][int(val)]]]
                else:
                    eventdata += [[evt[0], val]]
            for event in eventdata: triggerevent(events+event)
        else:
            if catname: events.insert(0, catname)
            triggerevent([eventdata]+events)

    def GetID(self, device=None, scene=None):
        searchdata = dc(self.devices) if device else dc(self.scenes)
        searchname = dc(device) if device else dc(scene)
        try: return searchdata[int(searchname)]['id']
        except: pass
        try: searchname = searchname.split('.')[2]
        except: pass

        for ID, namedata in enumerate(searchdata):
            if not namedata: continue
            if namedata['name'] == searchname: return str(dc(ID))
        return None

    def GetEvent(self, category, event):
        try: return dc(self.ALLOWEDEVENTS[str(category)][event])
        except: return None

    def GetCategory(self, category):
        try: return dc(self.CATEGORIES[str(category)])
        except: return None

    def GetRoom(self, room):
        try: return dc(self.rooms[int(room)]['name'])
        except: return None

    def GetDevice(self, device):
        try: return dc(self.devices[int(device)]['name'])
        except: return None

    def GetSection(self, room):
        try: return dc(self.sections[int(self.rooms[int(room)]['section'])]['name'])
        except: return None

    def GetVersion(self):
        return dc(self.system[0]['version'])
        
    def GetDataMark(self):
        return [dc(self.system[0][item]) for item in ['loadtime', 'dataversion']]

    def GetThermalUnit(self):
        return dc(self.system[0]['temperature'])

    def GetComment(self):
        return dc(self.system[0]['comment'])

    def GetLUUPState(self):
        return dc(self.system[0]['state'])

    def GetSerialNumber(self):
        return dc(self.system[0]['serial_number'])

    def GetModelNumber(self):
        return dc(self.system[0]['model'])

    def Update(self, XMLStr):
        self.XMLStr = XMLStr
        XML = ET.fromstring(XMLStr)
        XMLlist = [[None, 'devices'], ['-5', 'scenes'], ['-3', 'rooms'], ['-4', 'categories'], ['-2', 'sections'], ['-1', None]]
        datalist = [dc(self.system), dc(self.sections), dc(self.categories), dc(self.rooms), dc(self.scenes), dc(self.devices)]

        for i, group in enumerate(XMLlist):
            t = group.pop()
            try: XMLpath = '/'.join(['.', t, t[:-1]])
            except: group += [[XML.attrib]]
            else:
                group += [[]]
                for item in XML.findall(XMLpath):
                    group[1] += [item.attrib]

            pos = (len(datalist)-1)-i
            datalist[pos] = dict(new=self.ParseData(*group), old=datalist[pos])

        if datalist[0]['new'][0]['full'] == '0':
            datalist = [self.PartialUpdate(**item) for item in datalist]
        datalist = [self.FullUpdate(**item) for item in datalist]

        self.system, self.sections, self.categories, self.rooms, self.scenes, self.devices = datalist

        mark = self.GetDataMark()
        state = self.GetLUUPState()
        state = 4 if state == '2' or state == '3' else int(state)

        return [state]+mark

    def ParseData(self, category, nVDL):
        if not nVDL: return [{}]

        def Grow(res, ID, item):
            try: res[ID] = dc(item)
            except: res = Grow(res+[{}], ID, item)
            finally: return res

        res = []
        for item in nVDL:
            if category is not None: item['category'] = category
            try: item['id']
            except: item['id'] = '0'
            finally: ID = int(item['id'])
            if 'name' in item:
                item['name'] = item['name'].replace(".", "*")
            res = Grow(res, ID, item)

        return dc(res)

    def FullUpdate(self, new, old):
        old = self.Length(old, new)
        new = self.Length(new, old)

        try: res = [Database(dc(item), dc(old[i])) for i, item in enumerate(new)]
        except: res = [Database(dc(item), {}) for i, item in enumerate(new)]
        res = [[dc(item.Added()), dc(item.Removed()), dc(item.Changed())] for item in res]

        for i, item in enumerate(res):
            if not item: continue
            item = zip(item, ['Added', 'Removed', None])
            for payload, eventdata in item:
                if payload is None: continue
                self.TriggerEvent(payload, eventdata)

        return dc(new)

    def PartialUpdate(self, new, old):
        newdata = dc(old)
        ID = len(new)-1
        for key in new[ID].keys():
            newdata[ID][key] = new[ID].pop(key)

        return dict(new=dc(newdata), old=dc(old))
