#!/usr/bin/env bash

#env:
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/setup.sh)

#configure:
metaproject='/home/fschmuckermaier/IceCube/meta-projects/combo/stable/build'
file_path="/data/user/fschmuckermaier/data_raw/ppc_test"
file_name="test"
string=88
dom=71
n_runs=10

#run:
$metaproject/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/ppc_scripts/simple_POCAM_simulation.py --output-i3-file="${file_path}/${file_name}" --number-of-runs=$n_runs --string=$string --dom=$dom


#Choose flashing POCAMs:  (all true POCAM positions were shifted by 1 downwards (e.g. true position = 87,4), since only OMs can be flashed somehow...)
# 87 3
# 87 83
# 88 1
# 88 71
# 89 1
# 89 9
# 89 12
# 89 37
# 89 106
# 90 11
# 90 13
# 90 99
# 91 14
# 91 49
# 92 5
# 92 17
# 92 27
# 93 7
# 93 16
# 93 63
# 93 112




