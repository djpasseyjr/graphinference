# Notebooks

The exploring, visualizing and learning component of this research is mainly done in computational notebooks.
This directory is the home for these kinds of investigatons.

## Table of Contents

1. [NetworkInferenceMethods.ipynb](Jupyter/NetworkInferenceMethods.ipynb) is a notebook that investigates
different methods for studying the network that underlies a dynamical system. This notebook studies
network inference via process motifs, multivariate transfer entropy and vector autoregression.

1. [NetworkInferenceMethods.Rmd](R/NetworkInferenceMethods.pdf) also explores network inference
methods. It examines GraphicalVAR and the unified structural equation model.

1. [VARvsODE.ipynb](Jupyter/VARvsODE.ipynb) looks at what happens when vector autoregression attempts to learn a
simple linear ODE. This investigates the effects of adding noise and detrending on stationarity and 
statistical significance.

1. [VARAlternateForms.ipynb](Jupyter/VARAlternateForms.ipynb) explores three different formulations
of basic vector autoregression and simulates each of them in order to understand why they are equivalent.
The three forms are, first, the standard difference equation form, second, a weighted infinite sum of
noise vectors and third, a continuous time version expressed in the standard form of linear control
theory.

1. [NonLinearModels.ipynb](Jupyter/NonLinearModels.ipynb) loads simulatable
System Dynamics models that can be used as a testbed in order to understand what happens
when network identification techniques are used on nonlinear systems.

1. [MultilevelModelExample.Rmd](R/MultilevelModelExample.pdf) dives deeper into the math underlying
mixed effects and multilevel models in order to better understand multilevel autoregression.