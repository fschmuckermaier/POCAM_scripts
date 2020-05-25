#!/usr/bin/env bash

#env:
eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.1.0/setup.sh)

#configure:
file_path="/data/user/fschmuckermaier/data_raw/clsim_test"
file_name="test"
n_runs=100
gcd="/home/fschmuckermaier/gcd/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3.gz"

#run:
/home/fschmuckermaier/IceCube2/build/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/scripts/all_in_one_POCAM.py --add-cable --use-isotropy --output-i3-file="${file_path}/${file_name}" --number-of-runs=$n_runs --gcd-file="${gcd}"

