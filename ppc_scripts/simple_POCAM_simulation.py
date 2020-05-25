#!/usr/bin/env python

import os, sys
import numpy as np

if(os.getenv("I3_BUILD") == None):
    print("I3_BUILD not set.")
    sys.exit()

from os.path import expandvars

from I3Tray import *
from icecube import dataclasses, dataio, ppc
import argparse
from optparse import OptionParser

parser = OptionParser(description="This script creates photons from the specified POCAM, propagates them and stores the output in an .i3 output file.")
parser.add_option("--output-i3-file", help = "I3 File to write the numbers of dom hits for each run to, e.g. tmp/numbers_of_dom_hits.i3")
parser.add_option("--number-of-photons", type = "float",default=1e9)
parser.add_option("--number-of-runs", type = "int",default=100)
parser.add_option("--gcd-file", type = "str",default="/home/fschmuckermaier/gcd/GeoCalibDetectorStatus_ICUpgrade.v55.mixed_mergedGeo.V2.i3.bz2")
parser.add_option("--string", type="int", default=88, help="Flashing string")
parser.add_option("--dom", type="int", default=71, help="Flashing DOM")
(options, args) = parser.parse_args()

gcdfile=expandvars(options.gcd_file)


tray = I3Tray()

tray.AddModule("I3InfiniteSource", "muxer")(
    ("Prefix", gcdfile),
    ("Stream", icetray.I3Frame.DAQ)
    )

os.putenv("OGPU", "1")
os.putenv("PPCTABLESDIR",expandvars("$I3_BUILD/ice-models/resources/models/spice_3.2.2"))
os.putenv("FWID","-1") #-1 for isotropic emission
os.putenv("WFLA","405") #emitting wavelength


tray.AddModule("i3ppc", "ppc",HoleIceModel=expandvars("$I3_BUILD/ice-models/resources/models/spice_3.2.2/as.dat"))(
    ("nph", options.number_of_photons), #number of photons
    ("fla", OMKey(options.string,options.dom)), #flashing OM position
    ("wid",5)  #pulse width in ns
    )

tray.AddModule("I3Writer", "writer")(
    ("streams", [icetray.I3Frame.DAQ]),
    ("filename",os.path.join(options.output_i3_file+"_pocam_{s}_{d}.i3".format(s=options.string,d=options.dom)))
    )

tray.Execute(3+options.number_of_runs)

del tray
