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
        self.add_output('Emissions_CO2', val = 0)
        self.add_output('Emissions_H2O', val = 0)
        self.add_output('Emissions_BC', val = 0)
        self.add_output('Radiative_Forcing', val = 0)

    def compute(self, inputs, outputs):
# =============================================================================
#         treshold = 20e3; #meter of altitude (can be changed)
#         if inputs['r_ascent'] > treshold:
#         extract time t from r_ascent trashold
#         extract mass at time t
#         mass_propellant = inputs['GLOW'] - m_burn - mass_jettisoned -m_fairing
#         remove 2/3 from RF
# =============================================================================
        prop_type_1 = 'LH2'
        prop_type_2 = 'LH2'
        co2_1, h2o_1, bc_1 = enm.chemical_react(prop_type_1,
                                                     inputs['Prop_mass_stage_1'],
                                                     inputs['OF_stage_1'])
        co2_2, h2o_2, bc_2 = enm.chemical_react(prop_type_2,
                                                     inputs['Prop_mass_stage_2'],
                                                     inputs['OF_stage_2'],)
        co2 = co2_1 + co2_2
        h2o = h2o_1 + h2o_2
        bc = bc_1 + bc_2
        outputs['Radiative_Forcing'] = enm.radiative_forcing(co2, h2o, bc)
        outputs['Emissions_CO2'] = co2
        outputs['Emissions_H2O'] = h2o
        outputs['Emissions_BC'] = bc