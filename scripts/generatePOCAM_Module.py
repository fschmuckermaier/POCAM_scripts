# Icetray module to initiate a POCAM as a light source

from icecube import icetray, dataclasses
from I3Tray import I3Units
from icecube.dataclasses import *
from icecube.clsim import I3CLSimFlasherPulse, I3CLSimFlasherPulseSeries
from datetime import datetime
import math
import random
import numpy as np

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
        self.AddParameter("NumOfPhotons",
                          "The number of photons to inject from the given position.",
                          1)
        self.AddParameter("FlasherPulseType",
                          "The I3CLSimFlasherPulse.FlasherPulseType of the photon flashs. For a list, see: https://github.com/claudiok/clsim/blob/master/public/clsim/I3CLSimFlasherPulse.h#L59",
                          I3CLSimFlasherPulse.FlasherPulseType.LED405nm)
        self.AddParameter("Seed",
                          "Seed for the random number generator",
                          1234)
        self.AddParameter("Isotropy",
                          "Using isotropic or hemispheric photon emission",
			  True)
        self.AddOutBox("OutBox")

    def Configure(self):
        self.series_frame_key = self.GetParameter("SeriesFrameKey")
        self.photon_position = self.GetParameter("PhotonPosition")
        self.num_of_photons = self.GetParameter("NumOfPhotons")
        self.pulse_type = self.GetParameter("FlasherPulseType")
        self.seed = self.GetParameter("Seed")
        self.isotropy = self.GetParameter("Isotropy")


    def generate_pulse(self, photon_position, photon_direction, number_of_photons, isotropy):
        pulse = I3CLSimFlasherPulse()
        pulse.SetPos(photon_position)
        pulse.SetDir(photon_direction)
        pulse.SetTime(0.0*I3Units.ns)
        pulse.SetNumberOfPhotonsNoBias(number_of_photons)
        pulse.SetType(self.pulse_type)

        # Pulse duration:
        pulse.SetPulseWidth(5. * I3Units.ns) #POCAM: ~5ns

        if isotropy: # Isotropic emission (cover full sphere)
            pulse.SetAngularEmissionSigmaPolar( 180. * I3Units.deg )
            pulse.SetAngularEmissionSigmaAzimuthal( 360. * I3Units.deg )
        else: # Hemispheric emission (cover half of sphere)
            pulse.SetAngularEmissionSigmaPolar( 90. * I3Units.deg )
            pulse.SetAngularEmissionSigmaAzimuthal( 360. * I3Units.deg )

        return pulse

    def DAQ(self, frame):
        random.seed(self.seed)

        pulse_series = I3CLSimFlasherPulseSeries()
        if self.isotropy:
            photon_direction = I3Direction()
            photon_direction.set_theta_phi(0., 0.) #direction arbitrary due to isotropy

            pulse = self.generate_pulse(self.photon_position, photon_direction, self.num_of_photons, self.isotropy)
            pulse_series.append(pulse)
        else:
            #Define position of two hemispheres:
            pocam_position=self.photon_position
            pocam_position1 = I3Position(*[pocam_position[0],pocam_position[1],pocam_position[2]+0.125]) #shift hemisphere 12.5cm upwards
            pocam_position2 = I3Position(*[pocam_position[0],pocam_position[1],pocam_position[2]-0.125]) #shift hemisphere 12.5cm downwards

            #Define emission directions of two hemispheres:
            photon_direction1 = I3Direction()
            photon_direction2 = I3Direction()
            photon_direction1.set_theta_phi(0., 0.) #one hemisphere points upwards
            photon_direction2.set_theta_phi(np.pi, 0.) #one downwards

            pulse1 = self.generate_pulse(pocam_position1, photon_direction1, 0.5*self.num_of_photons, self.isotropy)
            pulse2 = self.generate_pulse(pocam_position2, photon_direction2, 0.5*self.num_of_photons, self.isotropy)
            pulse_series.append(pulse1)
            pulse_series.append(pulse2)

        frame[self.series_frame_key] = pulse_series
        self.PushFrame(frame, "OutBox")


