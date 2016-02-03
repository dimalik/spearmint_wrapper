Spearmint Wrappers
==================

These classes provide some extra boilerplate functionality for Jasper Snoek's [Spearmint](https://github.com/HIPS/Spearmint) which aims tο find the best values for hyperparameters in as few runs as possible.

While immensely helpful Spearmint  such as adding constraints, cleaning parameters

### Fix config.json ###

```Python

from utils import MakeExperiment

experiment = MakeExperiment(experiment_name, distributed, main_file)
experiment.addVar('x', "INT", 1, 0, 1)
experiment.addVar('y', "INT", 1, 0, 1)
experiment.save()

```

### Setup experiment ###

In order to setup a new simulation you need to sub-class from the `Simulation` class (or any child of it), define the `experiment_name` class attribute (so that it can be found) and fill in the `cleanParameters`, `constraints` and `run` methods.

```Python

class Example(Simulation):

experiment_name = 'example_experiment'

```



### Clean parameters ###

Spearmint can pass . Problems with that is


```Python
def cleanParameters(self):
	self.x = self.negexp(self.x)  # 10 ** -x
	self.y = self.xn(self.y, 5)  # 5 * x
```

### Add constraints (optional) ###

```Python
def constraints(self):
	return (self.x + self.y) < 10  # x + y < 10
```
