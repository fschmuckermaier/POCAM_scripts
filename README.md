# POCAM_scripts
Clsim scripts to simulate POCAMs as an isotropic or double hemispheric lightsource with cable shadow.

## Usage
The simulation can be either run in two indivdual steps or in one go. The first step is to create the flasher pulse with `scripts/create_qframe.py`. In the next step `scripts/propagate_POCAM_photons.py` reads in the resulting i3-file, propagates the photons and saves the output in another i3-file. `all_in_one_POCAM.py` does both steps in one. 
The flasher pulse is created with the module `scripts/generatePOCAM_Module.py`, where the emission solid angle, number of photons, etc. is defined.  
Executing the scripts could look like this (similar to `executable_POCAM.sh`):
Setting up the environment first:
```
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh)
```
and then running either in two steps:
```
~IceCube/build/env-shell.sh python ~POCAM_scripts/scripts/create_qframe.py --output-i3-file="/path/test.i3"
~IceCube/build/env-shell.sh python ~POCAM_scripts/scripts/propagate_POCAM_photons.py --output-i3-file="/path/test_output.i3" "/path/test.i3"
```
or together:
```
~IceCube/build/env-shell.sh python ~POCAM_scripts/scripts/all_in_one_POCAM.py --output-i3-file="/path/test_all_in_one.i3" 
```

#### Note
Currently, the flasher simulation in clsim seems to be broken. Until this bug is not fixed the scripts cannot be run. 
