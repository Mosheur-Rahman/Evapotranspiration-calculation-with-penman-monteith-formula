#!/usr/bin/env python
# coding: utf-8

# In[30]:


import numpy as np
import cmf
import matplotlib.pyplot as plt
import pandas as pd


# In[31]:


###Create all component function for ET formula
def vap_press_deficit (T,rH):
    es = 0.6108**((17.27*T)/(T+237.3))
    ea = es*(rH/100)
    vapour_deficit = es-ea
    return vapour_deficit


def Net_radiation (Tmax,Tmin,Ra_extra,h,R_solar,Fraction_hour_nByN, albedo,rH):
    #short_wave
    rs = (0.25+0.5*Fraction_hour_nByN)*Ra_extra
    rns = (1-albedo)*rs
    #clear_sky
    rs0 = (0.75+(2*10*h**-5))*Ra_extra
    Tmean = ((Tmax+273.15)**4)+((Tmin+273.15)**4)/2
    Radiation_Ratio = R_solar/rs0
    e_x = 0.6108**((17.27*Tmax)/(Tmax+237.3))
    e_n = 0.6108**((17.27*Tmin)/(Tmin+237.3))
    e_mean = (e_x+e_n)/2
    ea = e_mean*(rH/100)
    rnl = (4.903*10**-9)*Tmean*(0.34-0.14*ea**0.5)*(1.35*Radiation_Ratio-0.35)
    rn = rns-rnl
    return rn

def Aerodynamic_resistance (h,U):
    d = 0.65*h
    Z = 0.13*h
    Zoh = 0.2*Z
    upper_line1 = np.log((2-d)/Z)
    upper_line2 = np.log((2-d)/Zoh)
    ra = (upper_line1*upper_line2)/(0.16*U)
    return ra


# In[32]:


##Add weather data
w_data=pd.read_excel(r"/Users/shourovrahman/Documents/Disk Y/ET Model Data/ET_weather_data1.xlsx")

##Add plant data
p_data=pd.read_excel(r"/Users/shourovrahman/Documents/Disk Y/ET Model Data/Plants_data.xlsx")


# In[33]:


#Dayone
#weather
one_day = w_data.iloc[0]

#plant
Grass= p_data.iloc[0]


# In[34]:


###the values of albedo and canopy resistance put directly in the Penman Monteith equation


albedo = Grass["albedo"]

def ET(one_day, canopy_resistance, Grass):
    vapour_pressure = vap_press_deficit(one_day["T"],one_day["rH"])
    Radiation =  Net_radiation (one_day["Tmax"],one_day["Tmin"],one_day["Ra_extra"], Grass["h"], one_day["R_solar"],one_day["Fraction_hour_nByN"], albedo,one_day["rH"])
    AeroD = Aerodynamic_resistance (Grass["h"],one_day["U"])
    
    ###import cmf PenmanMonteith equation
    et = cmf.PenmanMonteith(Radiation,AeroD,70, one_day["T"],vapour_pressure)
    return et


ets = []
for i in range(len(w_data)):
    d = w_data.iloc[i]
    et = ET(d, albedo, Grass)
    ets.append(et)
    print(d["Date"], et) 


# In[35]:


plt.plot(w_data["Date"],ets)

plt.xlabel("Date")
plt.ylabel("ET (mm/day)")
plt.title("Evapotraspiration (Grass)")

from matplotlib import rcParams
rcParams["figure.figsize"]= 12,7


# In[ ]:




