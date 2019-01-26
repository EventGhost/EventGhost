# -*- coding: utf-8 -*-


class InstanceSingleton(type):
    _objects = {}

    def __call__(cls, id, *args):

        if id not in InstanceSingleton._objects:
            InstanceSingleton._objects[id] = (
                super(InstanceSingleton, cls).__call__(id, *args)
            )

        return InstanceSingleton._objects[id]
