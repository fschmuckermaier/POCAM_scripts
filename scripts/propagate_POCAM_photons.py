#!/usr/bin/env python

# Takes photons from qframe and propagates them. Saves results in output-i3-file.

from optparse import OptionParser
import glob
from os.path import expandvars

from icecube import dataclasses
from icecube.dataclasses import *
from icecube import icetray, dataio, phys_services, clsim
from icecube.icetray import I3Tray
from icecube import simclasses
from I3Tray import * # otherwise the C++ modules have the wrong signatures


### Command line options
# =============================================================================

parser = OptionParser(usage = "Usage: python propagate_photons_with_clsim.py options infile1.i3 infile2.i3 ...")
parser.add_option("--output-i3-file", help = "I3 File to write the numbers of dom hits for each run to, e.g. tmp/numbers_of_dom_hits.i3")
parser.add_option("--number-of-runs", type = "int", default = 0)
parser.add_option("--gcd-file", type = "str",default="/home/fschmuckermaier/gcd/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3.gz")
parser.add_option("--seed",type="int",default=12345,help="Initial seed for the random number generator")
(options, args) = parser.parse_args()
input_files = args

gcd_file=expandvars(options.gcd_file)


tray = I3Tray()
tray.AddModule("I3Reader",
               FilenameList = input_files)

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
    FlasherPulseSeriesName = "PhotonFlasherPulseSeries"
)

tray.AddSegment(clsim.I3CLSimMakeHits,
                **common_clsim_parameters
                )

tray.AddModule("I3Writer",
               Filename = options.output_i3_file)
tray.AddModule("TrashCan")

if options.number_of_frames == 0:
    tray.Execute()
else:
    tray.Execute(3+options.number_of_runs)

tray.Finish()





