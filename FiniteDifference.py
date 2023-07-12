# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:51:27 2022

@author: sigma
"""

#European options pricing

# Importing libraries
import pandas as pd
from numpy import *

#pip install cufflinks

import cufflinks as cf
cf.set_config_file(offline=True)

# Set max row and columns to 300
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 300)


# Specify the parameters for FDM 
T    = 1/12                              # time to maturity in years
E    = 14600                            # strike price
r    = .008                            # riskfree rate
vol  = .20                            # volatility
Flag = 1                              # Flag = 1 for call, -1 for puts
NAS  = 20                             # number of asset steps 

ds   = 2* E / NAS                     # asset step size
dt   = (0.9/vol**2/NAS**2)            # time step size, for stability

NTS  = int(T / dt) + 1                # number of time steps
dt   = T / NTS                        # time step size [Expiration as int # of time steps away]


# Create asset steps i*ds
s = arange(0,(NAS+1)*ds,ds)
s

# Create time steps k*dt
t = T-arange(NTS*dt,-dt,-dt)
t
# Verify the steps size
s.shape, t.shape


# Initialize the grid with zeros
grid = zeros((len(s),len(t)))

# Subsume the grid points into a dataframe
# with asset price as index and time steps as columns
grid = pd.DataFrame(grid, index=s, columns=t)
grid

# Set Final or Initial condition at Expiration
if Flag == 1:
    grid.iloc[:,0] = maximum(s - E, 0)
else:
    grid.iloc[:,0] = maximum(E - s, 0)
    
grid


for k in range(1, len(t)):
    for i in range(1,len(s)-1):
        delta = (grid.iloc[i+1,k-1] - grid.iloc[i-1,k-1]) / (2*ds)
        gamma = (grid.iloc[i+1,k-1]-2*grid.iloc[i,k-1]+grid.iloc[i-1,k-1]) / (ds**2)
        theta = (-0.5* vol**2 * s[i]**2 * gamma) - (r*s[i]*delta) + (r*grid.iloc[i,k-1])
        
        grid.iloc[i,k] = grid.iloc[i,k-1] - (theta*dt)
    
    # Set boundary condition at S = 0
    grid.iloc[0,k] = grid.iloc[0,k-1] * (1-r*dt) # ds = rsdt + sigma*sdx, s= 0, ds = 0 
    
    # Set boundary condition at S = infinity  # gamma = 0, so you can linearly extract
    grid.iloc[len(s)-1,k] = 2*grid.iloc[len(s)-2,k] - grid.iloc[len(s)-3,k]

# Round grid values to 4 decimals
grid = around(grid,4)
grid

grid.iplot(kind = 'surface', title='Call Option values by Explicit FDM')
