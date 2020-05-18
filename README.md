# POCAM_scripts
Clsim scripts to simulate POCAMs as an isotropic or double hemispheric lightsource with or without cable shadow.

## Descritpion
The simulation is performed in two steps. The first step is to create the flasher pulse and the second is the propagation of the photons. `all_in_one_POCAM.py` does both steps in one and saves the output as in i3 file. Here, a cable can be added next to all POCAM loations. The cable is per default 1 m long, has a radius of 2 cm and is placed 10 cm next to the POCAM middle axis. The cable is added with the option `--add-cable`.
The flasher pulse is created with the module `scripts/generatePOCAM_Module.py`, where the emission solid angle, number of photons, etc. is defined. The module creates either a fully isotropic emission in 4pi or an emission from two hemispheres in 2pi seperated by 25 cm, to account for the POCAMs design. Default is the double hemispheric emission, but isotropic emission can be set with `--use-isotropy` in `all_in_one_POCAM.py`. 

## Usage
`executable_POCAM.sh` is an example bash script, which can be submitted to a cluster. 
Executing the POCAM simulation could look like this (similar to `executable_POCAM.sh`):
Setting up the environment first:
```
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh)
```
and then running:
```
~IceCube/build/env-shell.sh python ~POCAM_scripts/scripts/all_in_one_POCAM.py --output-i3-file="/path/test.i3" --add-cable --number-of-runs=100 <... and further options>
```
