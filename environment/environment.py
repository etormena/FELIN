# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 19:12:39 2021

@author: Tormena Enrico & Ana Rita Texeira
"""

import numpy as np
from openmdao.api import ExplicitComponent
import environment.env_models as enm
class Environment_comp(ExplicitComponent):

    def setup(self):

        #Inputs
        self.add_input('Prop_mass_stage_1', val = 1e5)
        self.add_input('Prop_mass_stage_2', val = 1e5)
        self.add_input('OF_stage_1', val = 1e5)
        self.add_input('OF_stage_2', val = 1e5)
        self.add_input('r_ascent', shape = 4000)
        self.add_input('Dry_mass_stage_1', val = 1e4) 
        self.add_input('Dry_mass_stage_2', val = 1e4)
        self.add_input('GLOW', val = 1e5)
        
        ## Outputs
        self.add_output('Radiative_Forcing', val = 0)

    def compute(self, inputs, outputs):
# =============================================================================
#         treshold = 20e3; #meter of altitude (can be changed)
#         if inputs['r_ascent'] > treshold:
#             mass_propellant = inputs['GLOW'] - m_DRY [at moment t (how?)]
# =============================================================================
        prop_type = 'LOX/RP-1'
        stratospheric_emissions = enm.chemical_react(prop_type,inputs['Prop_mass_stage_1'],
                                  inputs['OF_stage_1'],
                                  inputs['Prop_mass_stage_2'],
                                  inputs['OF_stage_2'])
        outputs['Radiative_Forcing'] = enm.radiative_forcing(stratospheric_emissions)
