import stackless


class Tasklet(stackless.tasklet):
    countTasklets = 0
    
    def __init__(self, *args, **kwargs):
        stackless.tasklet.__init__(self, *args, **kwargs)
        Tasklet.countTasklets += 1
        self.taskId = Tasklet.countTasklets
        
    @classmethod
    def GetCurrentId(cls):
        try:
            return stackless.getcurrent().taskId
        except AttributeError:
            return 0