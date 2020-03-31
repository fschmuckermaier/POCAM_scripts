#!/usr/bin/env python


from os.path import expandvars

from icecube.icetray import I3Tray
from I3Tray import * # otherwise the C++ modules have the wrong signatures
from icecube import simclasses
from icecube import dataclasses
from icecube.dataclasses import *
from icecube import icetray, dataio, phys_services, clsim

import math
import random

from generatePOCAM_Module import GeneratePOCAM_Module

import argparse
from optparse import OptionParser
import glob


parser = OptionParser(description="This script creates photons at the given position, propagates them and stores the output in an  .i3 output file.")
parser.add_option("--output-i3-file", help = "I3 File to write the numbers of dom hits for each run to, e.g. tmp/numbers_of_dom_hits.i3")
parser.add_option("--number-of-photons", type = "float",default=1e9)
parser.add_option("--number-of-parallel-runs", type = "int",default=1)
parser.add_option("--number-of-runs", type = "int",default=10)
parser.add_option("--gcd_file", type = "str",default="/home/fschmuckermaier/gcd/standard.i3.bz2")
(options, args) = parser.parse_args()


#[x,y,z] of all 21 POCAMs:
pocam_positions=[                    #string,om-number
		[18.3,-51.1,348.07], #87,4 
		[18.3,-51.1,-421.93],#87,84
		[47.3,-57.0,398.07], #88,2
		[47.3,-57.0,-385.93],#88,72
		[14.3,-80.6,548.07], #89,2
		[14.3,-80.6,298.07], #89,10
		[14.3,-80.6,173.07], #89,13
		[14.3,-80.6,-277.93],#89,38
		[14.3,-80.6,-546.93],#89,107
		[57.3,-83.7,298.07], #90,12
		[57.3,-83.7,248.07], #90,14
		[57.3,-83.7,-457.93],#90,100
		[89.3,-59.0,123.07], #91,15
		[89.3,-59.0,-313.93],#91,50
		[62.6,-35.2,398.07], #92,6
		[62.6,-35.2,-101.93],#92,18
		[62.6,-35.2,-241.93],#92,28
		[27.0,-31.2,348.07], #93,8
		[27.0,-31.2,-76.93], #93,17
		[27.0,-31.2,-349.93],#93,64
		[27.0,-32.2,-646.93] #93,113
]

# Configure POCAM geometry: 

pocam_position = I3Position(*pocam_positions[0]) #e.g. first POCAM at (87,4)
theta= 0. #dircetion irrelevant due to isotropic emission
phi= 0.
photon_direction = I3Direction()
photon_direction.set_theta_phi(theta, phi)

gcd_file=expandvars(options.gcd_file)


tray = I3Tray()
tray.AddModule("I3InfiniteSource",
               Prefix = gcd_file,
               Stream = icetray.I3Frame.DAQ)

tray.AddModule(GeneratePOCAM_Module,
               SeriesFrameKey = "PhotonFlasherPulseSeries",
               PhotonPosition = pocam_position,
               PhotonDirection = photon_direction,
               NumOfPhotons = options.number_of_photons,
               Seed = 1234,
               FlasherPulseType = clsim.I3CLSimFlasherPulse.FlasherPulseType.LED405nm)

#tray.AddService("I3SPRNGRandomServiceFactory",
#                Seed = 123456,
#                NStreams = 2,
#                StreamNum = 1)

#randomService = phys_services.I3SPRNGRandomService(seed = 1234,
#                                                   nstreams = 10000,
#                                                   streamnum = 1)

randomService = phys_services.I3GSLRandomService(seed = 1234)

common_clsim_parameters = dict(
    PhotonSeriesName = "PropagatedPhotons",
    RandomService = randomService,
    IceModelLocation = expandvars("$I3_SRC/clsim/resources/ice/spice_mie"),
    GCDFile = gcd_file,    
    UnWeightedPhotons = True,
    #ParallelEvents = number_of_parallel_runs,
    UnWeightedPhotonsScalingFactor = 1.0,
    DOMOversizeFactor = 1.0,
    UnshadowedFraction = 1.0,
    FlasherPulseSeriesName = "PhotonFlasherPulseSeries"
)

tray.AddSegment(clsim.I3CLSimMakeHits,
                StopDetectedPhotons = True,
                #ExtraArgumentsToI3CLSimModule = extra_args,
                **common_clsim_parameters
                )

tray.AddModule("I3Writer",
               Filename = options.output_i3_file)
tray.AddModule("TrashCan")

if number_of_runs == 0:
    tray.Execute()
else:
    tray.Execute(options.number_of_runs)

tray.Finish()


