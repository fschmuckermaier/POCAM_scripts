#!/usr/bin/env bash

#env:
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/setup.sh)

#configure:
metaproject='/home/fschmuckermaier/IceCube/meta-projects/combo/stable/build'
file_path="/data/user/fschmuckermaier/data_raw/ppc_test"
file_name="test"
string=88
dom=72
n_runs=10

#run:
$metaproject/env-shell.sh python /home/fschmuckermaier/POCAM_scripts/ppc_scripts/simple_POCAM_simulation.py --output-i3-file="${file_path}/${file_name}" --number-of-runs=$n_runs --string=$string --dom=$dom


#Choose flashing POCAMs:
# 87 4
# 87 84
# 88 2
# 88 72
# 89 2
# 89 10
# 89 13
# 89 38
# 89 107
# 90 12
# 90 14
# 90 100
# 91 15
# 91 50
# 92 6
# 92 18
# 92 28
# 93 8
# 93 17
# 93 64
# 93 113




