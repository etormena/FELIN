# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 19:12:39 2021

@author: Tormena Enrico & Ana Rita Texeira
"""

import numpy as np
from openmdao.api import ExplicitComponent
from functions import chemical_react, radiative_forcing

class Trajectory_comp(ExplicitComponent):

    def setup(self): #/!\TO BE CHANGED ALL VAR NAMES AND VALUES /!\

        #Inputs
        self.add_input('m_prop', val=0)
        self.add_input('prop_type', val=0)
        self.add_input('altitude', val=0)
        self.add_input('m_vehicle', val = 0)
        self.add_input('m_dry', val = 0) #depends on staging
        
        ## Outputs
        self.add_output('stratospheric_emissions',shape = 0) 
        self.add_output('RF', val=0)

    def compute(self, inputs, outputs):
        treshold = 20e3; #meter of altitude (can be changed)
        if inputs['altitude'] > treshold:
            mass_propellant = inputs['m_vehicle'] - inputs['m_dry']
            products = chemical_react('prop_type',mass_propellant)
            outputs['RF'] = radiative_forcing(products)