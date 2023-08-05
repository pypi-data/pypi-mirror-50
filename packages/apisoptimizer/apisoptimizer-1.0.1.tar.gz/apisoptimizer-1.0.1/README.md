# ApisOptimizer: Artificial Bee Colony for Tuning Function Parameters

[![GitHub version](https://badge.fury.io/gh/tjkessler%2FApisOptimizer.svg)](https://badge.fury.io/gh/tjkessler%2FApisOptimizer)
[![PyPI version](https://badge.fury.io/py/apisoptimizer.svg)](https://badge.fury.io/py/apisoptimizer)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/TJKessler/ApisOptimizer/master/LICENSE.txt)
[![Build Status](https://dev.azure.com/travisjkessler/personal-repos/_apis/build/status/tjkessler.ApisOptimizer?branchName=master)](https://dev.azure.com/travisjkessler/personal-repos/_build/latest?definitionId=6&branchName=master)

ApisOptimizer is an open source Python package used to tune parameters for user-supplied functions. Inspired by [artificial bee colonies](https://inis.iaea.org/collection/NCLCollectionStore/_Public/41/115/41115772.pdf), ApisOptimizer is able to optimize variables in a multidimensional search space to minimize a "cost" (e.g. an error value returned by the user-supplied function).

<p align="center">
  <img align="center" src="docs/img/abc_visual_convergence.gif" width="75%" height="75%">
</p>

# Installation:

### Prerequisites:
- Have Python 3.X installed
- Have the ability to install Python packages

### Method 1: pip
If you are working in a Linux/Mac environment:
```
sudo pip install apisoptimizer
```

Alternatively, in a Windows or virtualenv environment:
```
pip install apisoptimizer
```

To update your version of ApisOptimizer to the latest version, use:
```
pip install --upgrade apisoptimizer
```

Note: if multiple Python releases are installed on your system (e.g. 2.7 and 3.7), you may need to execute the correct version of pip. For Python 3.7, change **"pip install apisoptimizer"** to **"pip3 install apisoptimizer"**.

### Method 2: From source
Download the ApisOptimizer repository, navigate to the download location on the command line/terminal, and execute:
```
python setup.py install
```

There are currently no additional dependencies for ApisOptimizer.

# Usage:

To start using ApisOptimizer, you need a couple items:
- a cost function (objective function) to optimize
- parameters used by the cost function

For example, let's define a cost function to minimize the sum of three integers:

```python
def minimize_integers(integers):

    return sum(integers)

```

Your objective function must accept a **list** from ApisOptimizer. The list values represent the current "food source", i.e. parameter values, being exploited by a given bee.

Now that we have our objective function, let's import the Colony object from ApisOptimizer, initialize the colony, and add our parameters:

```python
from apisoptimizer import Colony

def minimize_integers(integers):

    return sum(integers)

abc = Colony(10, minimize_integers)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.add_param(0, 10)
```

Here we initialize the colony with 10 employer bees, supply our objective function and add our parameters. Parameters are added with minimum/maximum values for its search space. By default, parameter mutations (searching a neighboring food source) will not exceed the specified parameter bounds [min_val, max_val]; if this limitation is not desired, supply the "restrict=False" argument:

```python
abc.add_param(0, 10, restrict=False)
```

Once we have created our colony and added our parameters, we then need to "initialize" the colony's bees:

```python
from apisoptimizer import Colony

def minimize_integers(integers):

    return sum(integers)

abc = Colony(10, minimize_integers)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.initialize()
```

Initializing the colony's bees deploys employer bees (in this example, 10 bees) to random food sources (random parameter values are generated), their fitness is evaluated (in this example, lowest sum is better), and onlooker bees (equal to the number of employers) are deployed proportionally to neighboring food sources of well-performing bees.

We then send the colony through a predetermined of "search cycles":

```python
from apisoptimizer import Colony

def minimize_integers(integers):

    return sum(integers)

abc = Colony(10, minimize_integers)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.initialize()
for _ in range(10):
    abc.search()
```

A search cycle consists of:
- each bee searches a neighboring food source (performs a mutation on one parameter)
- if the food source produces a better fitness than the bee's current food source, move there
- otherwise, the bee stays at its current food source
    - if the bee has stayed for (NE * D) cycles (NE = number of employers, D = dimension of the function, 3 in our example), abandon the food source
        - if the bee is an employer, go to a new random food source
        - if the bee is an onlooker, go to a food source neighboring a well-performing bee

We can access the colony's average fitness score, average objective function return value, best fitness score, best objective function return value and best parameters at any time:

```python
print(abc.average_fitness)
print(abc.average_ret_val)
print(abc.best_fitness)
print(abc.best_ret_val)
print(abc.best_params)
```

ApisOptimizer can utilize multiple CPU cores for concurrent processing:

```python
abc = Colony(10, minimize_integers, num_processes=8)
```

Tying everything together, we have:

```python
from apisoptimizer import Colony

def minimize_integers(integers):

    return sum(integers)

abc = Colony(10, minimize_integers)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.add_param(0, 10)
abc.initialize()
for _ in range(10):
    abc.search()
    print('Average fitness: {}'.format(abc.average_fitness))
    print('Average obj. fn. return value: {}'.format(abc.average_ret_val))
    print('Best fitness score: {}'.format(abc.best_fitness))
    print('Best obj. fn. return value: {}'.format(abc.best_ret_val))
    print('Best parameters: {}\n'.format(abc.best_params))
```

Running this script produces:

```
Average fitness: 0.07630512762091708
Average obj. fn. return value: 12.55
Best fitness score: 0.1
Best obj. fn. return value: 9
Best parameters: [0, 2, 7]

Average fitness: 0.08782728601807548
Average obj. fn. return value: 11.25
Best fitness score: 0.14285714285714285
Best obj. fn. return value: 6
Best parameters: [1, 2, 3]

Average fitness: 0.10526010753951928
Average obj. fn. return value: 9.45
Best fitness score: 0.25
Best obj. fn. return value: 3
Best parameters: [1, 0, 2]

Average fitness: 0.13604097291597292
Average obj. fn. return value: 8.1
Best fitness score: 0.5
Best obj. fn. return value: 1
Best parameters: [1, 0, 0]

Average fitness: 0.15408098845598844
Average obj. fn. return value: 6.8
Best fitness score: 0.5
Best obj. fn. return value: 1
Best parameters: [1, 0, 0]

Average fitness: 0.1892857142857143
Average obj. fn. return value: 5.75
Best fitness score: 0.5
Best obj. fn. return value: 1
Best parameters: [1, 0, 0]

Average fitness: 0.22303266178266182
Average obj. fn. return value: 5.2
Best fitness score: 1.0
Best obj. fn. return value: 0
Best parameters: [0, 0, 0]

Average fitness: 0.24969932844932846
Average obj. fn. return value: 4.65
Best fitness score: 1.0
Best obj. fn. return value: 0
Best parameters: [0, 0, 0]

Average fitness: 0.2911525974025974
Average obj. fn. return value: 4.2
Best fitness score: 1.0
Best obj. fn. return value: 0
Best parameters: [0, 0, 0]

Average fitness: 0.4092478354978355
Average obj. fn. return value: 3.4
Best fitness score: 1.0
Best obj. fn. return value: 0
Best parameters: [0, 0, 0]
```

To run this script yourself, head over to our [examples](https://github.com/tjkessler/ApisOptimizer/tree/master/examples) directory.

# Contributing, Reporting Issues and Other Support:

To contribute to ApisOptimizer, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).
