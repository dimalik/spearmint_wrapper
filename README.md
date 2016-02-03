Spearmint Wrappers
==================

These classes provide some extra boilerplate functionality for Jasper Snoek's [Spearmint](https://github.com/HIPS/Spearmint) which aims tο find the best values for hyperparameters in as few runs as possible.

While immensely helpful, as the experiment and the number of parameters grow both in size and complexity it might be difficult (and repetitive) to keep your code clean. To fix this we provide a set of classes which are aimed at abstracting away thing that need repetition so you can focus more on running experiments rather than fiddling around with the code.

### Setup experiment ###

In order to setup a new simulation you need to sub-class from the `Simulation` class (or any child of it), define the `experiment_name` class attribute (so that it can be found) and fill in the `cleanParameters()`, `constraints()` and `run()` methods.

```Python

class Example(Simulation):

	experiment_name = 'example_experiment'

```

### Clean parameters ###

In Spearmint you can pass INTs and FLOATs in some range or ENUMs which are lists of different discrete values. The problem with this approach is that you might need to pass a subset of the values in that range (e.g. 2, 4, 6, 8 instead of 1, 2, 3, 4, 5, 6, 7, 8). While ENUMs seem to take care of that they don't preserve the sequential nature of these numbers. To fix this we provide a way to preprocess the parameters sent from Spearmint in the `cleanParameters()` method. All the parameters listed in the `config.json` file are passed as instance attributes to some abstract `Simulation` class. You can then preprocess them before they enter you simulation. As an example three preprocessing functions are provided:

```Python
def cleanParameters(self):
	self.x = self.negexp(self.x)  # 10 ** -self.x
	self.y = self.xn(self.y, 5)  # 5 * self.y
	self.z = self.logn(self.z, 4)  # log4(self.z)
```

`negexp`, for example, can be used to get negative exponention which is particularly useful for learning rates (e.g. 0.001, 0.0001, 0.00001)

### Add constraints (optional) ###

You might need to add some constraints to your simulation. For example, if the sum of two parameters exceeds 10 then this would be invalid. In that case we should tell Spearmint that these values returned `np.nan`. To add constraints you need to fill in the `constraints()` method provided by the `Simulation` class which needs to return a `bool`. If `constraints()` returns `True` then a `ConstraintError` exception is elicited which in turn sends `np.nan` as the result.

```Python
def constraints(self):
	return (self.x + self.y) < 10  # x + y < 10
```

Having taken care of how the model should process the parameters we need to define the `run()` method which returns the score on the objective. All the parameters passed from Spearmint are going to be available as instance attributes and any 

```Python
def run(self, **kwargs):
    # get the score
    # ...
	return score
```

then at the `experiment.py` you need to define the path `main.py`

```Python
PATH = </path/to/main.py/>
```

### Fix config.json ###

`makeExperiment.py` provides some additional functionality which lets you create a `config.json` file in the form Spearmint expects it to be.


```Python

from utils import MakeExperiment

experiment = MakeExperiment(experiment_name, distributed, main_file)
experiment.addVar('x', "INT", 1, 0, 10)
experiment.addVar('y', "INT", 1, 0, 5)
experiment.addVar('z', "INT", 1, 0, 10)
experiment.save()

```

```Bash
python main.py /path/to/config.json
```

