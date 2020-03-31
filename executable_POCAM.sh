#!/usr/bin/env bash

# Not sure about eval/env-shell setup:
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh)

#Data stored at:
path='/data/user/fschmuckermaier/data_raw/clsim_test'

/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/generate_and_simulate_POCAM.py --output-i3-file="${path}/test_output.i3"

#Create q frame with POCAM as light source:
#/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/create_qframe_i3_file.py --output-file="${path}/qframe.i3"

#Propagate photons to complete simulation:
#/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/propagate_POCAM_photons.py --output-i3-file="${path}/output.i3" --output-text-file="${path}/output.txt" "${path}/qframe.i3"
