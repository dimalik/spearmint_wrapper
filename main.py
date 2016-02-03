from utils import get_module_logger, CheckConstraints


@CheckConstraints
def main(job_id, params):
    from utils import getModel
    from utils import getDataset

    logger = get_module_logger(__name__)
    logger.info('Starting job with id: %d' % job_id)
    logger.info('Fetching dataset %s' % params['dataset'])
    dataset = getDataset(params['dataset'])()

    logger.info('Using model %s' % params['experiment_name'])
    simulation = getModel(params['experiment_name'])(**params)
    logger.info('Starting training ...')
    vecs = simulation.run(dataset)
    logger.info('Getting scores')
    score = simulation.getScores(vecs, dataset.scores)
    logger.info('Score was: %f' % score)
    return score
