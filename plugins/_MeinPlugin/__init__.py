import eg
from threading import Event, Thread

class MyPlugin(eg.PluginClass):

    def __start__(self):
        self.stopThreadEvent = Event()
        thread = Thread(target=self.ThreadWorker, args=(self.stopThreadEvent,))
        thread.start()
        
    def __stop__(self):
        self.stopThreadEvent.set()
        
    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            self.TriggerEvent("MyTimerEvent")
            stopThreadEvent.wait(5.0)
