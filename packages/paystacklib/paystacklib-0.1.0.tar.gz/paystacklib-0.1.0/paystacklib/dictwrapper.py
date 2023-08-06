from dotmap import DotMap

class DictWrapper(DotMap):
    def __init__(self, *args, **kwargs):
        DotMap.__init__(self, *args, **kwargs)

    def __repr__(self):
        return repr(self.toDict())

    def __str__(self):
        return str(self.toDict())
