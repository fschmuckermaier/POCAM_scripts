# POCAM scripts
Scripts to simulate the Precision Optical Calibration Module (POCAM). The example script for ppc contains a simple approach by simulating an isotropic source. The clsim scripts allow an adding of a cable and non-isotropic emission profile. 


## Clsim scripts
Clsim scripts to simulate POCAMs as an isotropic or double hemispheric lightsource with or without cable shadow.

### Descritpion
The simulation is performed in two steps. The first step is to create the flasher pulse and the second is the propagation of the photons. `all_in_one_POCAM.py` does both steps in one and saves the output as in i3 file. Here, a cable can be added next to all POCAM locations. The cable is per default 1 m long, has a radius of 2 cm and is placed 10 cm next to the POCAM middle axis. The cable is added with the option `--add-cable`.
The flasher pulse is created with the module `scripts/generatePOCAM_Module.py`, where the emission solid angle, number of photons, etc. is defined. The module creates either a fully isotropic emission in 4pi or an emission from two hemispheres in 2pi seperated by 25 cm, to account for the POCAMs design. Default is the double hemispheric emission, but isotropic emission can be set with `--use-isotropy` in `all_in_one_POCAM.py`. 

### Usage
`clsim_executable.sh` is an example bash script, which can be submitted to a cluster. 
Executing the POCAM simulation could look like this (similar to `clsim_executable.sh`):
Setting up the environment first:
```
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh)
```
and then running:
```
~IceCube/build/env-shell.sh python ~POCAM_scripts/clsim_scripts/all_in_one_POCAM.py --output-i3-file="/path/test.i3" --add-cable --number-of-runs=100 <... and further options>
```

## ppc scripts
ppc scripts to perform a simple simulation. Here, the POCAM is treated as an isotropic lightsource. 

### Description
`simple_POCAM_simulation.py` is a slightly modified version of the standard example script in ppc. It produces isotropic flashes at the given DOM position. The default gcd contains the current upgrade geometry. Somehow non-optical module positions, e.g. positions for calibration devices, are not flashable. For the time being the next position under the real POCAM position (d=3m) is used for flashing. If exact position becomes relevant this issue is probably worth fixing. 

### Usage
`ppc_executable.sh` is an example bash script, which can be submitted to a cluster. 
Running the POCAM simulation could look like this (similar to `ppc_executable.sh`):
```
~IceCube/build/env-shell.sh python ~POCAM_scripts/ppc_scripts/simple_POCAM_simulation.py --output-i3-file="/path/test.i3" --string=88 --dom=71 --number-of-runs=100 <... and further options>
```
