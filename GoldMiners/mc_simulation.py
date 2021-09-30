import numpy as np
import math
import matplotlib as plt
from io import BytesIO

def mc(S0_lists, T, rf=.0065, sig=.2, M=30, num_sim=250000, cof_level=0.05):
    """
    Function prices an option using Monte Carlo Simulation

    Parameters:
        T (int): Time Steps to simulate i.e. simulation date (e.g 0.5 years)
        S0 (numpy.float): Initial price of underlying
        rf (numpy.float): risk-free rate
        sig (numpy.float): volatility/standard deviation of underlying
        M (int): The number of increments
        num_sim (int): number of simulations to run
    Returns:
        numpy.float: price of option
    """
    np.random.seed(1)  # need to set within function as each time function is called, will call a diff seed
    dt = T / M
    # get the portfolio price
    S = 0
    for S0 in S0_lists:
        # get price movement matrix
        ini_line = np.zeros((1, num_sim))  # set initial price
        change = (rf  - 0.5 * sig ** 2) * dt + \
                 sig * math.sqrt(dt) * np.random.standard_normal((M, num_sim))
        change = np.r_[ini_line, change]
        S += S0 * np.exp(np.cumsum(change, axis=0))

    # Plot MC paths
    plt.rcParams["figure.figsize"] = (20, 10)
    plt.grid(True)
    plt.plot(S, label='Monte Carlo Simulation results')
    plt.ylabel('Security Price')
    buffer = BytesIO()
    plt.savefig(buffer)
    # VaR
    St = S[-1]
    St.sort()
    VaR = St[cof_level*len(St)]
    return (S,buffer,VaR)