# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 16:24:43 2022

@author: sigma
"""


import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
import quantecon as qe
from quantecon.markov import DiscreteDP, backward_induction, sa_indices

T = 0.08       # Time expiration (years)
vol = 0.21     # Annual volatility
r = 0.008      # Annual interest rate
strike = 14500  # Strike price
p0 = 14300        # Current price
N = 20       # Number of periods to expiration

# Time length of a period
tau = T/N

# Discount factor
beta = np.exp(-r*tau)

# Up-jump factor
u = np.exp(vol*np.sqrt(tau))

# Up-jump probability
q = 1/2 + np.sqrt(tau)*(r - (vol**2)/2)/(2*vol)

# Possible price values
ps = u**np.arange(-N, N+1) * p0

# Number of states
n = len(ps) + 1  # State n-1: "the option has been exercised"

# Number of actions
m = 2  # 0: hold, 1: exercise

# Number of feasible state-action pairs
L = n*m - 1  # At state n-1, there is only one action "do nothing"

# Arrays of state and action indices
s_indices, a_indices = sa_indices(n, m)
s_indices, a_indices = s_indices[:-1], a_indices[:-1]


# Reward vector
R = np.empty((n, m))
R[:, 0] = 0
R[:-1, 1] = strike - ps
R = R.ravel()[:-1]

# Transition probability array
Q = sparse.lil_matrix((L, n))
for i in range(L-1):
    if a_indices[i] == 0:
        Q[i, min(s_indices[i]+1, len(ps)-1)] = q
        Q[i, max(s_indices[i]-1, 0)] = 1 - q
    else:
        Q[i, n-1] = 1
Q[L-1, n-1] = 1

# Create a DiscreteDP
ddp = DiscreteDP(R, Q, beta, s_indices, a_indices)

vs, sigmas = backward_induction(ddp, N)

v = vs[0]
max_exercise_price = ps[sigmas[::-1].sum(-1)-1]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot([0, strike], [strike, 0], 'k--')
axes[0].plot(ps, v[:-1])
axes[0].set_xlim(0, strike*2)
axes[0].set_xticks(np.linspace(0, 4, 5, endpoint=True))
axes[0].set_ylim(0, strike)
axes[0].set_yticks(np.linspace(0, 2, 5, endpoint=True))
axes[0].set_xlabel('Asset Price')
axes[0].set_ylabel('Premium')
axes[0].set_title('Put Option Value')

axes[1].plot(np.linspace(0, T, N), max_exercise_price)
axes[1].set_xlim(0, T)
axes[1].set_ylim(1.6, strike)
axes[1].set_xlabel('Time to Maturity')
axes[1].set_ylabel('Asset Price')
axes[1].set_title('Put Option Optimal Exercise Boundary')
axes[1].tick_params(right='on')

plt.show()