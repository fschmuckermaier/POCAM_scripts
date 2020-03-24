#!/usr/bin/env python

from icecube.icetray import I3Tray
from I3Tray import * # otherwise the C++ modules have the wrong signatures

from icecube import dataclasses
from icecube.dataclasses import *
from icecube import icetray, dataio, phys_services, clsim

import math
import random

from GeneratePOCAM_Module import GeneratePOCAM_Module

parser = argparse.ArgumentParser(description="This script creates photons at the given position and stores them in a qframe in an .i3 output file.")
parser.add_argument('--output-file', type=str, required=True)
args = parser.parse_args()


# Table of POCAM positions (String, OM-number, x , y, z):
'''
87 4   18.3 -51.1 348.07
87 84  18.3 -51.1 -421.93
88 2   47.3 -57.0 398.07
88 72  47.3 -57.0 -385.93
89 2   14.3 -80.6 548.07
89 10  14.3 -80.6 298.07
89 13  14.3 -80.6 173.07
89 38  14.3 -80.6 -277.93
89 107 14.3 -80.6 -546.93
90 12  57.3 -83.7 298.07
90 14  57.3 -83.7 248.07
90 100 57.3 -83.7 -457.93
91 15  89.3 -59.0 123.07
91 50  89.3 -59.0 -313.93
92 6   62.6 -35.2 398.07
92 18  62.6 -35.2 -101.93
92 28  62.6 -35.2 -241.93
93 8   27.0 -31.2 348.07
93 17  27.0 -31.2 -76.93
93 64  27.0 -31.2 -349.93
93 113 27.0 -31.2 -646.93
'''


# Configure POCAM: 

pocam_position = '18.3,-51.1,348.07' #e.g. POCAM at (87,4)
pocam_position = I3Position(*[float(coordinate) for coordinate in photon_position.split(",")])

theta= 0. #dircetion irrelevant due to isotropic emission
phi= 0.
photon_direction = I3Direction()
photon_direction.set_theta_phi(theta, phi)

number_of_photons = 1e4
number_of_runs = 1
gcd_file = 'standard.i3.bz2'
output_file = args.output_file

# Create fram:
tray = I3Tray()
tray.AddModule("I3InfiniteSource",
               Prefix = gcd_file,
               Stream = icetray.I3Frame.DAQ)

tray.AddModule(GeneratePOCAM_Module,
               SeriesFrameKey = "PhotonFlasherPulseSeries",
               PhotonPosition = pocam_position,
               PhotonDirection = photon_direction,
               NumOfPhotons = number_of_photons,
               Seed = 1234,
               FlasherPulseType = clsim.I3CLSimFlasherPulse.FlasherPulseType.LED405nm)

tray.AddModule("I3Writer",
               Filename = output_file)
tray.AddModule("TrashCan")
tray.Execute(number_of_frames)
tray.Finish()
