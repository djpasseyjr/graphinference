#!/bin/sh

module purge
module load python/3.9.6
pip install sktime torch pysindy
pip install /nas/longleaf/home/djpassey/graphinference/

python /nas/longleaf/home/djpassey/graphinference/experiments/noise_experiments.py $1