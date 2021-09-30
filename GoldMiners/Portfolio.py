from io import BytesIO
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import math

def random_portfolios(num_portfolios, num_securities, mean_returns, cov_matrix, risk_free_rate):
    """
    Function returns a tuple containing 2 arrays. The results array is a 2D array, columns for the portfolio instance, rows for the std dev, return, and sharpe ratio respectively. weights record is an array of arrays which contain the weight of each underlying.
    Each row is for each portfolio, each column for each underlying.

    Parameters:
        num_portfolios (int): The number of portfolio instances to create
        num_securities (int): the number of securities used
        mean_returns (pandas.Series): mean return of each security. len(mean_returns) must match num_securities
        cov_matrix (pandas.DataFrame): Covariance matrix of shape n * n, where n is num_securities
        risk_free_rate (numpy.float): the risk free rate used in computation for Sharpe Ratio
    Returns:
        tuple: first element contains 2D array columns for the portfolio instance, rows for the
                std dev, return, and sharpe ratio respectively.
                second element contains weights record, an list of arrays which contain the weight of each underlying.

    """
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        # Return random floats in the half-open interval [0.0, 1.0)
        weights = np.random.random(num_securities)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualized_performance(weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


def portfolio_annualized_performance(weights, mean_returns, cov_matrix):
    """
    Function returns the annualized performance given the weights of the portfolio.
    Function assumes current means and cov are daily returns

    Parameters:
        weights (numpy.array): array containing relative weights.
        mean_returns (pandas.Series): mean return of each security. len(mean_returns) must match num_securities
        cov_matrix (pandas.DataFrame): Covariance matrix of shape n * n, where n is num_securities
    Returns:
        tuple: Tuple contains the standard deviation and returns of the portfolio, annualized.
    """
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def display_simulated_ef_with_random(stk_list, ws, T=10, conf_level = 0.05, capital=1000, num_portfolios=30000):
    """
    Function displays the efficient frontier, and the weights allocated for the minimum variance portfolio 
    and market optimal portfolio using the Monte Carlo method. 

    Parameters 
        stk_list (str): string of chosen stock symbols, split by ','
        weights (Str): string of set asset weights, split by ','
        T (int): number of days to predict
        conf_level (np.float): confidence level
        capital (int): initial investment volume
        num_portfolios (int): number of randomly generated portfolios

    """
    # Split stock symbols
    symbol_list = stk_list.split(',')
    num_securities=len(symbol_list)
    
    # Estimate risk-free rate
    bonds_return =yf.download('^TNX', start=dt.date.today()-dt.timedelta(days=365), end=dt.date.today())
    risk_free_rate = bonds_return.Close.mean()*0.01

    # Download stock data
    data = yf.download(symbol_list, start=dt.date.today()-dt.timedelta(days=365*2), end=dt.date.today())
    main_data = data['Adj Close']
    returns = main_data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    # Generate random portfolios
    results, weights = random_portfolios(num_portfolios, num_securities, mean_returns, cov_matrix, risk_free_rate)

    # Identify the Maximum Sharpe portfolio
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=returns.columns, columns=['allocation'])
    max_sharpe_allocation['allocation'] = [round(i * 100, 2) for i in max_sharpe_allocation['allocation']]
    max_sharpe_allocation = max_sharpe_allocation.T

    # Identify the Minimum Variance Portfolio
    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=returns.columns, columns=['allocation'])
    min_vol_allocation['allocation'] = [round(i * 100, 2) for i in min_vol_allocation['allocation']]
    min_vol_allocation = min_vol_allocation.T
    
    # Plot anualized portfolio return vs annualized portfolio volatility
    plt.figure(figsize=(10, 7))
    plt.grid(ls='--')
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()

    # Mark Maximum Sharpe portfolio
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Maximum Sharpe ratio')

    # Mark Minimum variance portfolio
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Minimum volatility')
    plt.title('Simulated Efficient Frontier')
    plt.xlabel('annualized volatility')
    plt.ylabel('annualized returns')
    plt.legend(labelspacing=0.8)

    buf_ef = BytesIO()
    plt.savefig(buf_ef)
    plt.close()

    # Params for Monte Carlo Simulation
    S0_list = main_data.iloc[-1].values
    sig_list = returns.std().values
    ws = np.array([float(x) for x in ws.split(',')])

    buf_min, VaR_min = display_simulated_mc(S0_list, sig_list, risk_free_rate, min_vol_allocation.loc['allocation'].values/100, T, conf_level, capital)
    buf_max, VaR_max = display_simulated_mc(S0_list, sig_list, risk_free_rate, max_sharpe_allocation.loc['allocation'].values/100, T, conf_level, capital)
    buf_mc, VaR_mc = display_simulated_mc(S0_list, sig_list, risk_free_rate, ws, T, conf_level, capital)

    return buf_ef, min_vol_allocation, max_sharpe_allocation, S0_list, sig_list, buf_min, VaR_min, buf_max, VaR_max, buf_mc, VaR_mc

def display_simulated_mc(S0_list, sig_list, risk_free_rate, weights, T=10, conf_level=0.05, capital=1000, num_sim=300):
    """
    Function displays the FV of chosen portfolio using Monte Carlo Simulation.
    
    Parameters:
        S0_list (numpy.ndarray): Initial price of underlying
        sig_list (numpy.ndarray): volatility/standard deviation of underlying
        risk_free_rate (numpy.float): risk-free rate
        weights (numpy.ndarray): weights of assets in the portfolio
        T (int): Time Steps to simulate (e.g 10 days)
        conf_level (numpy.float): confidence level (used for calculating VaR)
        capital (int): initial investment amount
        num_sim (int): number of simulations to run
    """

    # Set random seed and step length
    np.random.seed(1)
    delta_t = 1

    S = np.zeros((T+1, num_sim))
    for i in range(len(S0_list)):
        S0 = S0_list[i]
        # get price movement matrix
        ini_line = np.zeros((1, num_sim))  # set initial price
        change = (risk_free_rate  - 0.5 * sig_list[i] ** 2) * delta_t + \
                 sig_list[i] * math.sqrt(delta_t) * np.random.standard_normal((T, num_sim))
        change = np.r_[ini_line, change]
        shares = np.floor(weights[i] * capital / S0)    # shares held from the beginning
        S += shares * S0 * np.exp(np.cumsum(change, axis=0))

    # Plot MC paths
    plt.rcParams["figure.figsize"] = (10, 7)
    plt.xlim(0,T)
    plt.grid(True)
    plt.title('Prediction with Monte Carlo Simulation')
    plt.plot(S, label='Monte Carlo Simulation results')
    plt.xlabel('Days from now')
    plt.ylabel('Porfolio value')
    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    # VaR
    VaR = 0
    St = S.sum(axis=0)
    VaR = -np.percentile(St,conf_level*100)
    return buffer, VaR