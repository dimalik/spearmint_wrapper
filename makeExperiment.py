class MakeExperiment(object):
    def __init__(self, experiment_name, distributed, main_file,
                 noise="GAUSSIAN", distributed_concurrent=5, description=""):
        self.experiment_name = experiment_name
        self.distributed = distributed
        self.main_file = main_file
        self.noise = noise
        self.distributed_concurrent = distributed_concurrent
        self.description = description
        self.init()

    def init(self):
        self.d = {}
        self.d['language'] = 'PYTHON'
        self.d['experiment-name'] = self.experiment_name
        self.d['polling-time'] = 1
        self.d['resources'] = {
            "local": {
                "scheduler": "local",
                "max-concurrent": 1,
                "max-finished-jobs": 100
            }
        }

        if self.distributed:
            self.d['resources']["cluster"] = {
                "scheduler": "SGE",
                "max-concurrent": self.distributed_concurrent,
                "max-finished-jobs": 1000
            }

        self.d['tasks'] = {
            self.experiment_name: {
                'type': "OBJECTIVE",
                'likelihood': self.noise,
                'main-file': self.main_file,
                'resources': ['cluster']
            }
        }
        self.d['tasks'][self.experiment_name]['resources'] =\
            self.d['resources'].keys()

        self.d['variables'] = {}
        self.d['description'] = self.description

    def addVar(self, name, type_, size, min_, max_):
        self.d['variables'][name] = {
            "type": type_,
            "size": size,
            "min": min_,
            "max": max_
        }

    def save(self, fname="config.json"):
        import json
        with file(fname, "w") as fout:
            json.dump(self.d, fout, indent=4)
