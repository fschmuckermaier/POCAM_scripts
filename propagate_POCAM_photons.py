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
parser.add_option("--number-of-frames", type = "int", default = 0)
parser.add_option("--number-of-parallel-runs", type = "int", default=1)

(options, args) = parser.parse_args()

input_files = args

#if isinstance(input_files, basestring):
#    input_files = eval(input_files)


tray = I3Tray()
tray.AddModule("I3Reader",
               FilenameList = input_files
)
tray.AddService("I3SPRNGRandomServiceFactory",
                Seed = 123456,
                NStreams = 2,
                StreamNum = 1)
randomService = phys_services.I3SPRNGRandomService(seed = options.seed,
                                                   nstreams = 10000,
                                                   streamnum = 1)

common_clsim_parameters = dict(
    PhotonSeriesName = "PropagatedPhotons",
    RandomService = randomService,
    IceModelLocation = expandvars("$I3_SRC/clsim/resources/ice/spice_mie"),
    UnWeightedPhotons = True,
    ParallelEvents = options.number_of_parallel_runs,
    UnWeightedPhotonsScalingFactor = 1.0,
    DOMOversizeFactor = 5.0,
    UnshadowedFraction = 1.0,
    FlasherInfoVectName = ("I3FlasherInfo" if options.use_flasher_info_vect else ""),
    FlasherPulseSeriesName = ("PhotonFlasherPulseSeries" if not options.use_flasher_info_vect else ""),
)

tray.AddSegment(clsim.I3CLSimMakeHits,
                StopDetectedPhotons = True,
                ExtraArgumentsToI3CLSimModule = extra_args,
                **common_clsim_parameters
                )

tray.AddModule("I3Writer",
               Filename = options.output_i3_file)
tray.AddModule("TrashCan")

if options.number_of_frames == 0:
    tray.Execute()
else:
    tray.Execute(options.number_of_frames)

tray.Finish()





