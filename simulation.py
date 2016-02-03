import os
import sys
import logging
import math

from utils import get_module_logger, ConstraintError


logger = get_module_logger(__name__)


class DerivationRegistry(type):
    def __init__(cls, name, bases, cls_dict):
        type.__init__(cls, name, bases, cls_dict)
        cls._subclasses = set()
        for base in bases:
            if isinstance(base, DerivationRegistry):
                base._subclasses.add(cls)

    def getSubclasses(cls):
        return list(reduce(
            set.union,
            (succ.getSubclasses() for succ in cls._subclasses
             if isinstance(succ, DerivationRegistry)),
            cls._subclasses))


class Simulation(object):

    __metaclass__ = DerivationRegistry

    def __init__(self, experiment_name, seed=1337, debug=False,
                 **params):
        self.experiment_name = experiment_name
        self.seed = seed
        self.debug = debug

        self.__dict__.update(**params)

        self._cleanParameters()
        self._checkConstraints()

    @classmethod
    def getName(cls):
        return os.path.basename(
            sys.modules[cls.__module__].__file__).split('.')[0]

    def _checkConstraints(self):
        if self.constraints():
            logger.error('Constraints were not satisfied, exiting')
            raise ConstraintError

    def constraints(self):
        raise NotImplementedError

    def _cleanParameters(self):
        self.cleanParameters()
        for k, v in self.__dict__.iteritems():
            logging.info('{}: {}'.format(k, v))

    def cleanParameters(self):
        raise NotImplementedError

    @staticmethod
    def xn(self, param, n=10):
        return n * param

    @staticmethod
    def negexp(self, param):
        return 10 ** -int(param)

    @staticmethod
    def logn(self, param, base=2):
        return math.log(param, base)

    def run(self):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.experiment_name
