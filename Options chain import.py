# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 19:22:07 2023

@author: sigma
"""

# Import required libraries
import pandas as pd
import numpy as np
from scipy.stats import norm
#ip install fredapi
from fredapi import Fred
#pip install fredpy
import fredpy as fp
#pip install QuantLib
import QuantLib as ql
import statistics

import matplotlib.pyplot as plt
from tabulate import tabulate # conda install tabulate
import yfinance as yf

from BS import BS


# Get SPY option chain
spy = yf.Ticker('SPY')
options = spy.option_chain('2023-03-31')


# March 2023 335 SPY call option price
spot = 345
strike = 335
rate = 0.04
dte = 0.3945
vol = 0.2185
spy_opt = BS(spot,335,rate,dte,vol)
print(f'Option Price of SPY201231C00335000 with BS Model is {spy_opt.callPrice:0.4f}')

# March 2023 335 SPY call option price
spot = 335
strike = 335
rate = 0.04
dte = 0.3945
vol = 0.2185
spy_opt = BS(spot,335,rate,dte,vol)
print(f'Option Price of SPY201231C00335000 with BS Model is {spy_opt.callPrice:0.4f}')

# Dataframe manipulation with selected fields
df = pd.DataFrame({'Strike': df['strike'], 
                   'Price': df['lastPrice'], 
                   'ImpVol': df['impliedVolatility']})
# Check output
df.head(2)


# Derive greeks and assign to dataframe as columns
df['Delta'] = df['Gamma'] = df['Vega'] = df['Theta'] = 0.

for i in range(len(df)):
    
    df['Delta'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).callDelta
    df['Gamma'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).gamma
    df['Vega'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).vega
    df['Theta'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).callTheta
    
# Verify output
df.head()


# Visualize the data
# Plot graph iteratively
fig, ax = plt.subplots(2,2, figsize=(20,10))

ax[0,0].plot(df['Strike'], df['Delta'], color='r', label='DEC 20')
ax[0,1].plot(df['Strike'], df['Gamma'], color='b', label='DEC 20')
ax[1,0].plot(df['Strike'], df['Vega'], color='k', label='DEC 20')
ax[1,1].plot(df['Strike'], df['Theta'], color='g', label='DEC 20')
    
# Set axis title
ax[0,0].set_title('Delta'), ax[0,1].set_title('Gamma'), ax[1,0].set_title('Vega'), ax[1,1].set_title('Theta')

# Define legend
ax[0,0].legend(), ax[0,1].legend(), ax[1,0].legend(), ax[1,1].legend()

plt.show()
    