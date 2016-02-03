from functools import reduce


class DerivationRegistry(type):
    def __init__(cls, name, bases, cls_dict):
        type.__init__(cls, name, bases, cls_dict)
        cls._subclasses = set()
        for base in bases:
            if isinstance(base, DerivationRegistry):
                base._subclasses.add(cls)

    def getSubclasses(cls):
        return reduce(
            set.union,
            (succ.getSubclasses() for succ in cls._subclasses
             if isinstance(succ, DerivationRegistry)),
            cls._subclasses)

class Base(object):
    __metaclass__ = DerivationRegistry

class Cls1(object):
    pass

class Cls2(Base):
    pass


print(Base.getSubclasses())
