from icecube import icetray, dataclasses
from I3Tray import I3Units
from icecube.dataclasses import I3Position
from icecube.dataclasses import *
from icecube.clsim import I3CLSimFlasherPulse, I3CLSimFlasherPulseSeries
from datetime import datetime
import math
import random

class GeneratePOCAM_Module(icetray.I3Module):
    """
    Generate a POCAM Flash into a DAQ Frame.
    """
    def __init__(self, context):
        icetray.I3Module.__init__(self, context)
        self.AddParameter("SeriesFrameKey",
                          "Name of the I3Frame Key the photon flash should be written to",
                          "PhotonFlasherPulseSeries")
        self.AddParameter("PhotonPosition",
                          "The position of the photon source.",
                          I3Position(0,0,0))
        self.AddParameter("PhotonDirection",
                          "The direction of the photon source",
                          I3Direction(0,0,0))
        self.AddParameter("NumOfPhotons",
                          "The number of photons to inject from the given position.",
                          1)
        self.AddParameter("FlasherPulseType",
                          "The I3CLSimFlasherPulse.FlasherPulseType of the photon flashs. For a list, see: https://github.com/claudiok/clsim/blob/master/public/clsim/I3CLSimFlasherPulse.h#L59",
                          I3CLSimFlasherPulse.FlasherPulseType.LED405nm)
        self.AddParameter("Seed",
                          "Seed for the random number generator",
                          1234)
        self.AddOutBox("OutBox")

    def Configure(self):
        self.series_frame_key = self.GetParameter("SeriesFrameKey")
        self.photon_position = self.GetParameter("PhotonPosition")
        self.photon_direction = self.GetParameter("PhotonDirection")
        self.num_of_photons = self.GetParameter("NumOfPhotons")
        self.pulse_type = self.GetParameter("FlasherPulseType")
        self.seed = self.GetParameter("Seed")

    def generate_pulse(self, photon_position, photon_direction, number_of_photons):
        pulse = I3CLSimFlasherPulse()
        pulse.SetPos(photon_position)
        pulse.SetDir(photon_direction)
        pulse.SetTime(0.0*I3Units.ns)
        pulse.SetNumberOfPhotonsNoBias(number_of_photons)
        pulse.SetType(self.pulse_type)

        # Pulse duration:
        pulse.SetPulseWidth(5. * I3Units.ns) #POCAM: ~5ns
        # Isotropic emission (cover full sphere):
        pulse.SetAngularEmissionSigmaPolar( 180. * I3Units.deg ) 
        pulse.SetAngularEmissionSigmaAzimuthal( 360. * I3Units.deg )

        return pulse

    def DAQ(self, frame):
        random.seed(self.seed)

        pulse_series = I3CLSimFlasherPulseSeries()
        pulse = self.generate_pulse(self.photon_position, self.photon_direction, self.num_of_photons)
        pulse_series.append(pulse)

        frame[self.series_frame_key] = pulse_series
        self.PushFrame(frame, "OutBox")

