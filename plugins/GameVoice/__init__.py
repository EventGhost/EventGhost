eg.RegisterPlugin(
    name = "Sidewinder Game Voice",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "remote",
    canMultiLoad = False,
    description = (
        'Allows the communication with the Microsoft Sidewinder Game Voice.<br/>'
        'This plug in also demonstrates how to use EventGhost\'s HID API.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

import eg.WinApi.HIDHelper
import eg.WinApi.HIDThread

class GameVoice(eg.PluginClass):
    def __start__(self):
        pass

    def __stop__(self):
        pass        
