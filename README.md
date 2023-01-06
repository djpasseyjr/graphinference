# `graphinference`

Infering computational networks from time series data.

## Installation

There are two options for installation. The first install only
the code library contained within the `graphinference` package, and
the second option installs pinned versions of the dependencies so that the results in the Jupyter notebooks can be reproduced.

### Option 1: Install `graphinference` Library Only

To install this repo as a Python package simply run
```
pip3 install git+https://github.com/djpasseyjr/graphinference.git
```

Then you can, for example, simulate a Ornstein–Uhlenbeck process 
with the following lines of Python:
```
import numpy as np
import matplotlib.pyplot as plt

import graphinference.libs.qspems_sim_core as qspems_sim_core

# Make adjacency matrix
adjacency_matrix = (np.random.rand(5, 5) < .2).astype(float)

# Generate the time series
stochastic_timeseries = qspems_sim_core.sim(adj, dt=1.0, sigma=.05)

# Plot
plt.plot(stochastic_timeseries.T, alpha=.5)
```

![](https://github.com/djpasseyjr/graphinference/raw/main/Images/OrnsteinUhlenbeckProcessExample.png)


### Option 2: Reproduce the Results in a Virtual Environment

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

This will initialize a virtual environment. All the Python necessary packages will be installed *within* this repo. The `deactivate` bash/zsh command turns this off and uses your system python packages.

**4. Install Dependencies and Package Via `pip`**

After `JAVA_HOME` is set properly, from the top level directory of this repo run:

```
# Install all dependencies via pip
pip3 install -r requirements.txt

# Install graphinference
pip3 install .
```

## Uninstall and Delete

If you installed without intending to reproduce the work run
```
pip3 uninstall graphinference
```

If you initialized the virtual environment inside of this repository, then deleting this repository will delete the code here along with all of the locally installed python packages.

```
pip3 uninstall graphinference
deactivate
# Delete repo
rm -rd path/to/graphinferece
```