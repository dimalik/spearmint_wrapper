import sys
import json

PATH = ''
sys.path.insert(0, PATH)


def main(job_id, params):
    from main import main as m
    with file("config.json") as fin:
        params_ = json.load(fin)

    params['experiment_name'] = params_['experiment-name']
    params['dataset'] = params_['dataset']
    return m(job_id, params)
