#!/usr/bin/env python

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
parser.add_option("--output-text-file", help = "File to write the number of dom hits for each run to, one line per run, e.g. tmp/numbers_of_dom_hits.txt", default = "tmp/number_of_dom_1_1_hits.txt")
parser.add_option("--ice-model", dest = "ice_model_file", help = "e.g. $I3_SRC/clsim/resources/ice/spice_mie")
parser.add_option("--seed", type = "int", help = "e.g. 123456")
parser.add_option("--number-of-frames", type = "int", default = 0)
parser.add_option("--number-of-parallel-runs", type = "int")
parser.add_option("--save-photon-paths", default = False)
parser.add_option("--use-flasher-info-vect", default = False)
parser.add_option("--thinning-factor", type = "float", default = 1.0, help = "Run expensive simulations with less photons. See https://github.com/fiedl/hole-ice-study/issues/85.")

(options, args) = parser.parse_args()

input_files = args

if isinstance(input_files, basestring):
    input_files = eval(input_files)

om_key = OMKey(1,1)

counter = 0
numbers_of_dom_hits = []
def ReadOutAngularAcceptance(frame):
    global numbers_of_dom_hits
    n = 0
    if (frame['MCPESeriesMap'].items() != []):
        if not frame['MCPESeriesMap'].get(om_key) is None:
            n = len(frame['MCPESeriesMap'].get(om_key))
    numbers_of_dom_hits.append(n)
    global counter
    counter += 1

tray = I3Tray()
tray.AddModule("I3Reader",
               FilenameList = input_files)
tray.AddService("I3SPRNGRandomServiceFactory",
                Seed = options.seed,
                NStreams = 2,
                StreamNum = 1)
randomService = phys_services.I3SPRNGRandomService(seed = options.seed,
                                                   nstreams = 10000,
                                                   streamnum = 1)

common_clsim_parameters = dict(
    PhotonSeriesName = "PropagatedPhotons",
    RandomService = randomService,
    IceModelLocation = options.ice_model_file,
    UnWeightedPhotons = True,
    ParallelEvents = options.number_of_parallel_runs,
    UnWeightedPhotonsScalingFactor = options.thinning_factor,
    DOMOversizeFactor = 1.0,
    UnshadowedFraction = 1.0,
    FlasherInfoVectName = ("I3FlasherInfo" if options.use_flasher_info_vect else ""),
    FlasherPulseSeriesName = ("PhotonFlasherPulseSeries" if not options.use_flasher_info_vect else ""),
)

tray.AddSegment(clsim.I3CLSimMakeHits,
                StopDetectedPhotons = True,
                ExtraArgumentsToI3CLSimModule = extra_args,
                **common_clsim_parameters
                )

if not options.save_photon_paths:
    # This does only work with the `I3CLSimMakeHits` module, thus does
    # not work with `save_photon_paths`.
    tray.AddModule(ReadOutAngularAcceptance,
                   Streams = [icetray.I3Frame.DAQ])

tray.AddModule("I3Writer",
               Filename = options.output_i3_file)
tray.AddModule("TrashCan")

if options.number_of_frames == 0:
    tray.Execute()
else:
    tray.Execute(options.number_of_frames)

tray.Finish()

outfile = open(options.output_text_file, 'w')
for number_of_dom_hits in numbers_of_dom_hits:
  print >> outfile, number_of_dom_hits
outfile.close()




