# `graphinference`

Infering computational networks from time series data.

This repo seeks to understand algorithms that augment our ability to identify true dynamic relationships in complex systems. Because complex systems can be discontinuous, non-linear, hybrid
systems and because they often involve a high degree of feedback and accumulation,
the assumptions of explanitory models that are fundamentally linear in nature,
like autoregressive models, fall short.

But to what extent do these algorithms fail? Are they still able to provide
useful information when the systems of interest do not satisfy the assumptions? When do they fail, and why? What are the alternatives?

This repo seeks to investigate the following:

1. Failure modes of autoregression and multilevel autoregression.
2. Alternate theoretical formulations of the concept of the *computational network* of a complex system.
3. Algorithmic approaches that assist the development of explanitory models of complex systems.

## Quick Start

There are two options for installation. The quick install only loads
the code library contained within the `graphinference` package, and
the second option, explained further down installs pinned dependencies so the
jupyter and Rmd notebooks can be reproduced exactly.

### Install `graphinference`

To install this repo as a Python package simply run
```
pip3 install git+https://github.com/djpasseyjr/graphinference.git
```

### Short Example

Then you can, for example, simulate a Ornstein–Uhlenbeck process 
with the following lines of Python:
```
import numpy as np
import matplotlib.pyplot as plt

import graphinference.libs.qspems_sim_core as qspems_sim_core

# Make adjacency matrix
adjacency_matrix = (np.random.rand(5, 5) < .2).astype(float)

# Generate the time series
stochastic_timeseries = qspems_sim_core.sim(adjacency_matrix, dt=1.0, sigma=.05)

# Plot
plt.plot(stochastic_timeseries.T, alpha=.5)
```

![](https://github.com/djpasseyjr/graphinference/raw/main/Images/OrnsteinUhlenbeckProcessExample.png)


## Reproduce the Results in a Virtual Environment

This repo install, loads pinned versions of the dependencies so that the results in the Jupyter notebooks can be reproduced.

**1. Install Java and Set `$JAVA_HOME`**

This package requires Java because some of the network inference methods call algorithms written in Java. You can install or update Java
from the [Java website](https://www.java.com/).

Then, set the `$JAVA_HOME` environment variable.

If you're using bash, all you have to do is:
```
echo export "JAVA_HOME=\$(/usr/libexec/java_home)" >> ~/.bash_profile
```
If you're using zsh (which probably means you're running macOS 
Catalina or newer), then it should instead be:
```
echo export "JAVA_HOME=\$(/usr/libexec/java_home)" >> ~/.zshrc
```
In either case, restart your shell.

See [this stack overflow answer](https://stackoverflow.com/questions/22842743/how-to-set-java-home-environment-variable-on-mac-os-x-10-9) for more details.

If you are using Windows, I wish you and DOS the *very* best.

**2. Clone Repo**
```
git clone https://github.com/djpasseyjr/graphinference.git
```

**3. Create and Activate Virtual Environment**

This package is pinned to specific dependency versions so that it is guarenteed to be executable in the future. For this reason, it needs to be installed in a virtual environment so that it does not conflict with Python packages that are already installed.

From the top level directory of this repo, set up the virtual environment with the following commands:

```
# Create virtual environment
python3 -m venv graphinf_venv

# Activate the environment
source graphinf_venv/bin/activate
```

This will initialize a virtual environment. All the necessary Python packages will be installed to a folder *within* this repo. The `deactivate` bash/zsh command turns off the environment and switches back to your system python packages.

**4. Install `graphinference` Dependencies and Package Via `pip`**

After `JAVA_HOME` is set properly, from the top level directory of this repo run:

```
pip3 install -r requirements.txt
```
to install all dependencies via pip and

```
pip3 install .
```
to install `graphinference`.

## Uninstall and Delete

If you quick installed the package, simply run
```
pip3 uninstall graphinference
```

If you initialized the virtual environment inside of this repository, then deleting this repository will delete the code here along with all of the locally installed python packages.

```
pip3 uninstall graphinference
deactivate
# Delete repo from your file system
rm -rdf path/to/graphinferece
```

## List of Useful Repos and Packages

* [`netrd`](https://github.com/netsiphd/netrd) A Library for network reconstruction, distances and dynamics

* [`pyboolnet`](https://github.com/hklarner/pyboolnet) Boolian network simulation library

* [`lmeresampler`](http://cran.r-project.org/package=lmeresampler) Bootstrapping mixed effect models in R

* [`jidt`](https://github.com/jlizier/jidt) Information theoretic measures of computation in Java

* [`idtxl`](https://github.com/pwollstadt/IDTxl) Inference of networks and their node dynamics from multivariate time series data using information theory in python.