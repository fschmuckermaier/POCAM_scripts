#!/usr/bin/env bash

# Not sure about eval/env-shell setup:
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh)

#Data stored at:
path='/data/user/fschmuckermaier/data_raw/clsim_test'

#Without propagation:
/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/scripts/create_qframe.py --output-i3-file="${path}/test_qframe2.i3"

/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/scripts/propagate_POCAM_photons.py --output-i3-file="${path}/test_output.i3" "${path}/test_qframe2.i3"

