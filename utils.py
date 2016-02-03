import os
import logging

import numpy as np

from simulation import Simulation


models = Simulation.getSubclasses()


class ConstraintError(Exception):
    pass


def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    if not len(logger.handlers):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S %p')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        file_handler = logging.FileHandler(
            filename=os.path.join(config.log_path, mod_name),
            mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger


def CheckConstraints(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConstraintError:
            return np.nan
    return wrapper


def getModel(experiment_name):

    logging.info("Available models are {}".format(
        ', '.join([str(x) for x in models])
    ))
    for model in models:
        if model.experiment_name == experiment_name:
            logging.info("Model {} found!".format(experiment_name))
            return model
