import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

def random_portfolios(num_portfolios, num_securities, mean_returns, cov_matrix, risk_free_rate):
    """
    Function returns a tuple containing 2 arrays. The results array is a 2D array, columns for the portfolio instnace, rows for the
    std dev, return, and sharpe ratio respectively. weights record is an array of arrays which contain the weight of each underlying.
    Each row is for each portfolio, each column for each underlying

    Parameters:
        num_portfolios (int): The number of portfolio instances to create
        num_securities (int): the number of securities used
        mean_returns (pandas.Series): mean return of each security. len(mean_returns) must match num_securities
        cov_matrix (pandas.DataFrame): Covariance matrix of shape n * n, where n is num_securities
        risk_free_rate (numpy.float): the risk free rate used in computation for Sharpe Ratio
    Returns:
        tuple: first element contains 2D array columns for the portfolio instnace, rows for the
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
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
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

def display_simulated_ef_with_random(df, mean_returns, num_securities, cov_matrix, num_portfolios, risk_free_rate):
    results, weights = random_portfolios(num_portfolios, num_securities, mean_returns, cov_matrix, risk_free_rate)
    """
    Function displays the efficient frontier, and the weights allocated for the minimum variance portfolio 
    and market optimal portfolio using the Monte Carlo method. 

    Parameters 
        df (pandas.DataFrame): Dataframe containing the daily returns 
        mean_returns (pandas.Series): Mean return of each security. len(mean_returns) must match num_securities 
        cov_matrix (pandas.DataFrame): Covariance matrix of shape n * n, where n is num_securities 
        num_portfolios (int): The number of portfolio instances to create 
        risk_free_rate (numpy.float):Tthe risk free rate used in computation for Sharpe Ratio

    """
    # Identify the Maximum Sharpe portfolio
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=df.columns, columns=['allocation'])
    max_sharpe_allocation['allocation'] = [round(i * 100, 2) for i in max_sharpe_allocation['allocation']]
    max_sharpe_allocation = max_sharpe_allocation.T

    # Identify the Minimum Variance Portfolio
    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=df.columns, columns=['allocation'])
    min_vol_allocation['allocation'] = [round(i * 100, 2) for i in min_vol_allocation['allocation']]
    min_vol_allocation = min_vol_allocation.T

    # Output the portfolio return and standard deviation of the Minimum Volatility Portfolio
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Annualised Return:", round(rp_min, 2))
    print("Annualised Volatility:", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)

    # Output the portfolio return and standard deviation of the Maximum Sharpe Portfolio
    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)

    # Plot anualized portfolio return vs annualized portfolio volatility
    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()

    # Mark Maximum Sharpe portfolio
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Maximum Sharpe ratio')

    # Mark Minimum variance portfolio
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Minimum volatility')
    plt.title('Simulated Efficient Frontier')
    plt.xlabel('annualised volatility')
    plt.ylabel('annualised returns')
    plt.legend(labelspacing=0.8)