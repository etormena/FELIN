# -*- coding: utf-8 -*-

def chemical_react(prop_type,mass,of):
    m_fuel = mass/(1+of)
    if prop_type == 'RP-1':
        mass_CO2 = 0.99 * m_fuel * (12.01 + 16*2)/(12.01 + 1.008*2)
        mass_H2O = 0.99 * m_fuel * (1.008*2 + 16)/(12.01 +1.008*2)
        mass_BC = 0.01 * m_fuel #estimation from De Sain
    if prop_type == 'LH2':
        mass_CO2 = 0
        mass_H2O = m_fuel * (1.008*2 + 16)/(1.008*2)
        mass_BC = 0
    if prop_type == 'CH4':
        mass_CO2 = 0.995 * m_fuel * (12.01 + 16*2)/(12.01 + 1.008*4)
        mass_H2O = 0.995 * m_fuel * 2 * (16 + 1.008*2)/(12.01 + 1.008*4)
        mass_BC = 0.005 * m_fuel
    return mass_CO2, mass_H2O, mass_BC

def radiative_forcing(co2, h2o, bc):
    #-------------------------- Constants----------------------------------------
    F = 2/3 # 2/3 of total propellant burned at the stratosphere assumption, Ross
    N = 1 # annual launch rate (studying the 'single-launch' case)
    tau = 4 # average stratospheric lifetime in years
    A = 1.2e14 # accumulation region area in m^2
    RF_data = {}
    RF_data['H2O'] = {'Abs_Factor': 4, 'I': 235}
    RF_data['CO2'] = {'Abs_Factor': 0.005, 'I': 235}
    RF_data['BC'] = {'Abs_Factor': 10000, 'I': 342}
    RF_data['Al2O3'] = {'Abs_Factor': (1881*235-342*619), 'I': 1}
    emissions = {'H2O':h2o, 'CO2':co2, 'BC':bc}
    RF = {}
    for index in list(emissions.keys()):
        if index in RF_data.keys():
            RF[index] =  F*RF_data[index]['Abs_Factor']*RF_data[index]['I']*(
            (1e3/A)*N*tau*emissions[index])
    RF = sum(RF.values())
    return RF