# -*- coding: utf-8 -*-

def chemical_react(prop_type,m1,of1,m2,of2):
    emissions = {}
    if prop_type == 'LOX/RP-1':
        m_rp1 = 1/(1+of1) +  m2/(1+of2)
        m_lox = (m1+m2) - m_rp1
        emissions['CO2']: 0.99 * m_rp1 * (12.01 + 16*2)/(12.01 + 1.008*2)
        emissions['H2O']: 0.99 * m_rp1 * (1.008*2 + 16)/(12.01 +1.008*2)
        emissions['BC']:  0.01 * m_rp1 #estimation from De Sain
    return emissions

def radiative_forcing(emissions):
    #-------------------------- Constants----------------------------------------
    F = 2/3 # 2/3 of total propellant burned at the stratosphere assumption, Ross
    N = 1 # annual launch rate (studying the 'single-launch' case)
    tau = 4 # average stratospheric lifetime in years
    A = 1.2e14 # accumulation region area in m^2
    RF_data = {}
    RF_data['H2O'] = {'Abs_Factor': 4, 'I': 235}
    RF_data['CO2'] = {'Abs_Factor': 0.005, 'I': 235}
    RF_data['C'] = {'Abs_Factor': 10000, 'I': 342}
    RF_data['Al2O3'] = {'Abs_Factor': (1881*235-342*619), 'I': 1}
    RF = {}
    
    for index in list(emissions.keys()):
        if index in RF_data.keys():
            RF[index] =  F*RF_data[index]['Abs_Factor']*RF_data[index]['I']*(
            (1e3/A)*N*tau*emissions[index])
    RF = sum(RF.values())
    return RF