#!/usr/bin/env bash

# Not sure about eval/env-shell setup:
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh)

#Data stored at:
path='/data/user/fschmuckermaier/data_raw/clsim_test'

/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/scripts/generate_and_simulate_POCAM.py --output-i3-file="${path}/test_output.i3"

