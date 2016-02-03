Spearmint Wrappers
==================

These classes provide some extra boilerplate functionality for Jasper Snoek's [Spearmint](https://github.com/HIPS/Spearmint) which aims tο find the best values for hyperparameters in as few runs as possible.

While immensely helpful, as the experiment and the number of parameters grow both in size and complexity it might be difficult (and repetitive) to keep your code clean. To fix this we provide a set of classes which are aimed at abstracting away thing that need repetition so you can focus more on running experiments rather than fiddling around with the code.

### Fix config.json ###

```Python

from utils import MakeExperiment

experiment = MakeExperiment(experiment_name, distributed, main_file)
experiment.addVar('x', "INT", 1, 0, 1)
experiment.addVar('y', "INT", 1, 0, 1)
experiment.save()

```

### Setup experiment ###

In order to setup a new simulation you need to sub-class from the `Simulation` class (or any child of it), define the `experiment_name` class attribute (so that it can be found) and fill in the `cleanParameters()`, `constraints()` and `run()` methods.

```Python

class Example(Simulation):

	experiment_name = 'example_experiment'

```

### Clean parameters ###

Spearmint can pass . Problems with that is
all the parameters listed in the `config.json` file are passed as instance attributes. For example, if you have an ![g](http%3A%2F%2Fwww.sciweavers.org%2Ftex2img.php%3Feq%3D%2520%255Ceta%2520%26bc%3DWhite%26fc%3DBlack%26im%3Djpg%26fs%3D12%26ff%3Darev%26edit%3D0)

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

```Python
def run(self,)
```


then at the `experiment.py` you need to define the path `main.py`

```Python
PATH = </path/to/main.py/>
```

```Bash
python main.py /path/to/config.json
```
