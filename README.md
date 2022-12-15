# `graphinference`

Infering computational networks from time series data.

## Install
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

After `JAVA_HOME` is set, clone this repo, and from the top level directory, run:

```
# Create and activate virtual environment
python3 -m venv graphinf_venv
source graphinf_venv/bin/activate

# Install all dependencies via pip
pip3 install -r requirements.txt

# Install graphinference
pip3 install .
```

When you are finished, to delete the virtual environment, and thereby delete all locally installed dependencies, in the top level directory, run:
```
deactivate
rm -rd graphinf_venv
```

This should completely remove the packages installed to run this code.

>*Why Use A Virtual Environement?*
>
>*This package is pinned to specific software versions so that it is guarenteed to be executable in the future. For this reason, it needs to be installed in a virtual environment so that it does not conflict with Python packages that are already installed.*
