import os
import sys
import logging
import math

from sklearn import cross_validation

from scipy.stats import spearmanr, kendalltau
from sklearn.linear_model import LinearRegression

from skll.metrics import kappa

import config
from utils.callGWET import getGWET

from exceptions import ConstraintError
from utils import get_module_logger


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

    def __init__(self, experiment_name, seed=config.seed, debug=False,
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


class VectorScoringSimulation(Simulation):

    def __init__(self, *args, **kwargs):
        self.score = None
        super(VectorScoringSimulation, self).__init__(*args, **kwargs)

    def getScores(self, X, y, train_test=config.train_test_scoring,
                  train_valid=config.train_valid_scoring):

        logger.info('Splitting between train and test\
 (ratio: %f)' % train_test)
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(
            X, y, test_size=train_test, random_state=self.seed)
        logger.info('Splitting between train and valid\
 (ratio: %f)' % train_valid)
        X_train, X_valid, y_train, y_valid = cross_validation.train_test_split(
            X_train, y_train, test_size=train_valid, random_state=self.seed)

        lr = LinearRegression(n_jobs=config.n_jobs)
        lr.fit(X_train, y_train)
        score = 1 - lr.score(X_valid, y_valid)

        # also report correlation and AC score
        logger.info("Score on test set: {}".format(lr.score(X_test, y_test)))
        sr = spearmanr(lr.predict(X_test), y_test)
        kt = kendalltau(lr.predict(X_test), y_test)
        logger.info("Metrics information:")
        logger.info("Spearman rho: {} ({})".format(sr[0], sr[1]))
        logger.info("Kendall tau: {} ({})".format(kt[0], kt[1]))
        logger.info("AC score: {}".format(getGWET(lr.predict(X_test), y_test)))
        logger.info("Cohen's kappa (no weights): {}".format(
            kappa(lr.predict(X_test), y_test)))
        logger.info("Cohen's kappa (quadratic): {}".format(
            kappa(lr.predict(X_test), y_test), weights='quadratic'))
        logger.info("Cohen's kappa (linear): {}".format(
            kappa(lr.predict(X_test), y_test), weights='linear'))

        return score if score >= 0 else 1

    def processTexts(self, docs):
        '''Helper routine to do special preprocessing'''
        raise NotImplementedError

    def __str__(self):
        ans = self.__class__.experiment_name
        if self.score:
            ans += ' ' + str(self.score)
        return ans
