#!/usr/bin/env python

# Takes input gcd and puts cables next to POCAM positions
# Note: Cable length?

input_gcd_file = "/home/fschmuckermaier/gcd/standard.i3.bz2"

# Data destination
destination_gcd_file = "/home/fschmuckermaier/gcd/standard_gcd_cable.i3.bz2"

# Material properties
cable_effective_scattering_length = 100.0 # metres
cable_absorption_length = 0.0
cable_radius = 0.02 # metres


import glob

import os
from os.path import expandvars
import sys
import pandas
import numpy as np

def expand_path(filename):
  return os.path.expandvars(os.path.expanduser(filename))

#[x,y,z] of all 21 POCAMs:
pocam_positions=[ 
		[18.3,-51.1,348.07], 
		[18.3,-51.1,-421.93],
		[47.3,-57.0,398.07],
		[47.3,-57.0,-385.93],
		[14.3,-80.6,548.07],
		[14.3,-80.6,298.07],
		[14.3,-80.6,173.07],
		[14.3,-80.6,-277.93],
		[14.3,-80.6,-546.93],
		[57.3,-83.7,298.07],
		[57.3,-83.7,248.07],
		[57.3,-83.7,-457.93],
		[89.3,-59.0,123.07],
		[89.3,-59.0,-313.93],
		[62.6,-35.2,398.07],
		[62.6,-35.2,-101.93],
		[62.6,-35.2,-241.93],
		[27.0,-31.2,348.07],
		[27.0,-31.2,-76.93],
		[27.0,-31.2,-349.93],
		[27.0,-32.2,-646.93]
]

# Compose cable cylinders:

#Example for cable positions: 20cm in x direction from POCAM center
cable_positions=[[pos[0]+0.2, pos[1], pos[2]] for pos in pocam_positions]
cable_radii=[]
cable_scattering_lengths=[]
cable_absorption_lengths=[]
for i in range(21):
    cable_radii.append(cable_radius) 
    cable_scattering_lengths.append(cable_effective_scattering_length)
    cable_absorption_lengths.append(cable_absorption_length)



# Process i3 file
from icecube import dataclasses
from icecube.dataclasses import *
from icecube import icetray, dataio, phys_services, clsim
from icecube.icetray import I3Tray
from icecube import simclasses
from I3Tray import * # otherwise the C++ modules have the wrong signatures

def add_cable_to_geometry_frame(frame, positions = [], radii = [], scattering_lengths = [], absorption_lengths = []):
  positions = (dataclasses.I3Position(pos[0], pos[1], pos[2]) for pos in positions)
  frame.Put("HoleIceCylinderPositions", dataclasses.I3VectorI3Position(positions))
  frame.Put("HoleIceCylinderRadii", dataclasses.I3VectorFloat(radii))
  frame.Put("HoleIceCylinderScatteringLengths", dataclasses.I3VectorFloat(scattering_lengths))
  frame.Put("HoleIceCylinderAbsorptionLengths", dataclasses.I3VectorFloat(absorption_lengths))

tray = I3Tray()
tray.AddModule("I3Reader",
               Filename = expand_path(input_gcd_file))
tray.AddModule(add_cable_to_geometry_frame,
               positions = cable_positions,
               radii = cable_radii,
               scattering_lengths = cable_scattering_lengths,
               absorption_lengths = cable_absorption_lengths,
               Streams = [icetray.I3Frame.Geometry])
tray.AddModule("I3Writer",
               Filename = expand_path(destination_gcd_file))
tray.AddModule("TrashCan")
tray.Execute()
tray.Finish()

print("Output file: " + destination_gcd_file)
