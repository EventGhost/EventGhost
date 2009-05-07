# -*- coding: utf-8 -*-

"""
    eg.Tasklet
    ~~~~~~~~~~
    
    A wrapper around stackless.tasklet

    :copyright: 2009 by EventGhost team, see AUTHORS.txt for more details.
    :license: GNU GPL v2, see LICENSE.txt for more details.
"""

import stackless


class Tasklet(stackless.tasklet):
    countTasklets = 0
    
    def __init__(self, func):
        stackless.tasklet.__init__(self)
        self.bind(func)
        Tasklet.countTasklets += 1
        self.taskId = Tasklet.countTasklets
        
    @classmethod
    def GetCurrentId(cls):
        try:
            return stackless.getcurrent().taskId
        except AttributeError:
            return 0