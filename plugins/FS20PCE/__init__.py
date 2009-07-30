eg.RegisterPlugin(
    name = "ELV FS20 PCE",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "remote",
    canMultiLoad = False,
    description = (
        'Allows to recieve events from FS20 remote controls.<br/>'
        'This plug in also demonstrates how to use EventGhost\'s HID API.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

class FS20PCE(eg.PluginClass):
    def __start__(self):
        pass

    def __stop__(self):
        pass        
