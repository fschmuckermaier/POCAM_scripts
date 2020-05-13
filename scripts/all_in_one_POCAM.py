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
import numpy as np

from generatePOCAM_Module import GeneratePOCAM_Module

import argparse
from optparse import OptionParser
import glob


parser = OptionParser(description="This script creates photons from the specified POCAM, propagates them and stores the output in an .i3 output file.")
parser.add_option("--output-i3-file", help = "I3 File to write the numbers of dom hits for each run to, e.g. tmp/numbers_of_dom_hits.i3")
parser.add_option("--number-of-photons", type = "float",default=1e9)
parser.add_option("--number-of-runs", type = "int",default=10)
parser.add_option("--use-isotropy",action="store_true", default=False,help="Uses isotropic emission when set, otherwise hemispherical")
parser.add_option("--add-cable",action="store_true", default=False,help="Places cable next to every POCAM position")
parser.add_option("--gcd-file", type = "str",default="/home/fschmuckermaier/gcd/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3.gz")
parser.add_option("--POCAM-index", type = "int",default=3,help="Number of POCAM to flash according to list below in script, default is the second POCAM at string 88")
parser.add_option("--seed",type="int",default=12345,help="Initial seed for the random number generator")
(options, args) = parser.parse_args()

gcd_file=expandvars(options.gcd_file)

#[x,y,z] of all 21 POCAMs:
pocam_positions=[            #index, (string,om-number)
		[18.3,-51.1,348.07], #0,  (87,4)
		[18.3,-51.1,-421.93],#1,  (87,84)
		[47.3,-57.0,398.07], #2,  (88,2)
		[47.3,-57.0,-385.93],#3,  (88,72)
		[14.3,-80.6,548.07], #4,  (89,2)
		[14.3,-80.6,298.07], #5,  (89,10)
		[14.3,-80.6,173.07], #6,  (89,13)
		[14.3,-80.6,-277.93],#7,  (89,38)
		[14.3,-80.6,-546.93],#8,  (89,107)
		[57.3,-83.7,298.07], #9,  (90,12)
		[57.3,-83.7,248.07], #10, (90,14)
		[57.3,-83.7,-457.93],#11, (90,100)
		[89.3,-59.0,123.07], #12, (91,15)
		[89.3,-59.0,-313.93],#13, (91,50)
		[62.6,-35.2,398.07], #14, (92,6)
		[62.6,-35.2,-101.93],#15, (92,18)
		[62.6,-35.2,-241.93],#16, (92,28)
		[27.0,-31.2,348.07], #17, (93,8)
		[27.0,-31.2,-76.93], #18, (93,17)
		[27.0,-31.2,-349.93],#19, (93,64)
		[27.0,-32.2,-646.93] #20, (93,113)
]
pocam_pos=pocam_positions[options.POCAM_index]

if options.add_cable: #Configure cables if set
    # Material properties
    cable_effective_scattering_length = 100.0 # metres
    cable_absorption_length = 0.0
    cable_radius = 0.02 # metres

    #Cable positions: 15cm in y direction from POCAM center
    cable_positions=[[pos[0], pos[1]+0.15, pos[2]] for pos in pocam_positions]
    cable_radii=[]
    cable_scattering_lengths=[]
    cable_absorption_lengths=[]
    for i in range(21):
        cable_radii.append(cable_radius)
        cable_scattering_lengths.append(cable_effective_scattering_length)
        cable_absorption_lengths.append(cable_absorption_length)

    def add_cable_to_geometry_frame(frame, positions = [], radii = [], scattering_lengths = [], absorption_lengths = []):
        positions = (dataclasses.I3Position(pos[0], pos[1], pos[2]) for pos in positions)
        frame.Put("HoleIceCylinderPositions", dataclasses.I3VectorI3Position(positions))
        frame.Put("HoleIceCylinderRadii", dataclasses.I3VectorFloat(radii))
        frame.Put("HoleIceCylinderScatteringLengths", dataclasses.I3VectorFloat(scattering_lengths))
        frame.Put("HoleIceCylinderAbsorptionLengths", dataclasses.I3VectorFloat(absorption_lengths))

tray = I3Tray()
tray.AddModule("I3InfiniteSource",
               Prefix = gcd_file,
               Stream = icetray.I3Frame.DAQ)

if options.add_cable: #add cables if set
    tray.AddModule(add_cable_to_geometry_frame,
                   positions = cable_positions,
                   radii = cable_radii,
                   scattering_lengths = cable_scattering_lengths,
                   absorption_lengths = cable_absorption_lengths,
                   Streams = [icetray.I3Frame.Geometry])

if options.use_isotropy: #Use isotropic emission profile
    #Configure geometry:
    pocam_position = I3Position(*pocam_pos)
    photon_direction = I3Direction()
    photon_direction.set_theta_phi(0., 0.) #direction arbitrary due to isotropy

    tray.AddModule(GeneratePOCAM_Module,
                   SeriesFrameKey = "PhotonFlasherPulseSeries",
                   PhotonPosition = pocam_position,
                   PhotonDirection = photon_direction,
                   NumOfPhotons = options.number_of_photons,
                   Seed = options.seed,
      	           Isotropy= True,
                   FlasherPulseType = clsim.I3CLSimFlasherPulse.FlasherPulseType.LED405nm)

else: #Use two seperated hemispheres as emission profile
    #Configure geometry:
    pocam_position1 = I3Position(*[pocam_pos[0],pocam_pos[1],pocam_pos[2]+0.125]) #shift hemisphere 12.5cm upwards
    pocam_position2 = I3Position(*[pocam_pos[0],pocam_pos[1],pocam_pos[2]-0.125]) #shift hemisphere 12.5cm downwards

    photon_direction1 = I3Direction()
    photon_direction2 = I3Direction()
    photon_direction1.set_theta_phi(0., 0.) #one hemisphere points upwards
    photon_direction2.set_theta_phi(np.pi, 0.) #one downwards

    tray.AddModule(GeneratePOCAM_Module,
                   SeriesFrameKey = "PhotonFlasherPulseSeries",
                   PhotonPosition = pocam_position1,
                   PhotonDirection = photon_direction1,
                   NumOfPhotons = 0.5*options.number_of_photons,
                   Seed = options.seed,
                   Isotropy=False,
                   FlasherPulseType = clsim.I3CLSimFlasherPulse.FlasherPulseType.LED405nm)
    tray.AddModule(GeneratePOCAM_Module,
                   SeriesFrameKey = "PhotonFlasherPulseSeries",
                   PhotonPosition = pocam_position2,
                   PhotonDirection = photon_direction2,
                   NumOfPhotons = 0.5*options.number_of_photons,
                   Seed = options.seed,
                   Isotropy=False,
                   FlasherPulseType = clsim.I3CLSimFlasherPulse.FlasherPulseType.LED405nm)

try:
    randomService = phys_services.I3SPRNGRandomService(
        seed = options.seed,
        nstreams = 10000,
        streamnum = 1)
except AttributeError:
    randomService = phys_services.I3GSLRandomService(
        seed = options.seed)

common_clsim_parameters = dict(
    PhotonSeriesName = "PropagatedPhotons",
    RandomService = randomService,
    IceModelLocation = expandvars("$I3_SRC/clsim/resources/ice/spice_mie"),
    GCDFile = gcd_file,
    UnWeightedPhotons = True,
    UnWeightedPhotonsScalingFactor = 1.0,
    DOMOversizeFactor = 1.0,
    UnshadowedFraction = 1.0,
    DoNotParallelize=True,
    UseGPUs=True,
    UseCPUs=False,
    StopDetectedPhotons = True,
    FlasherPulseSeriesName = "PhotonFlasherPulseSeries")

tray.AddSegment(clsim.I3CLSimMakeHits,
                **common_clsim_parameters
                )

tray.AddModule("I3Writer", #labeling=name_index-number-of-POCAM_number-of-flashes.i3
               Filename = options.output_i3_file+"_{a}_{b}.i3".format(a=options.POCAM_index,b=options.number_of_runs))
tray.AddModule("TrashCan")

if options.number_of_runs == 0:
    tray.Execute()
else:
    tray.Execute(3+options.number_of_runs)

tray.Finish()


