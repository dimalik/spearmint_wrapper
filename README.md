Spearmint Wrappers
==================

These classes provide some extra boilerplate functionality for Jasper Snoek's [Spearmint](https://github.com/HIPS/Spearmint) which aims tο find the best values for hyperparameters in as few runs as possible.

While immensely helpful Spearmint  such as adding constraints, cleaning parameters

### Fix config.json ###

```
experiment = MakeExperiment(experiment_name, distributed, main_file)

experiment.addVar('x', "INT", 1, 0, 1)

experiment.addVar('y', "INT", 1, 0, 1)

experiment.save()

```
