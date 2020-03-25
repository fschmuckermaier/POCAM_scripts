#!/usr/bin/env bash

# Not sure about eval/env-shell setup:
#eval $(/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh)
#/home/fschmuckermaier/IceCube/build/env-shell.sh

#Create q frame with POCAM as light source:
python create_qframe_i3_file.py --output-file="path/qframe.i3"

#Propagate photons to complete simulation:
python propagate_POCAM_photons.py --output-i3-file="path/output.i3" --output-text-file="path/output.txt" "path/qframe.i3" 

