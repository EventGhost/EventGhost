

import eg
from Utils import SetClass

class CustomMetaclass(type):
    def __new__(cls, name, bases, dct):
        if len(bases):
            moduleName = dct["__module__"].split(".")[-1]
            class NewCls:
                pass
            NewCls.__dict__ = dct
            trans = getattr(eg.text, moduleName, None)
            if trans is None:
                class Trans:
                    pass
                trans = Trans()
            SetClass(trans, NewCls)
            setattr(eg.text, moduleName, trans)
            return trans
        return type.__new__(cls, name, bases, dct)


class TranslatableStrings:
    __metaclass__ = CustomMetaclass
        
