from django.http import HttpResponse
import yfinance as yf
import datetime as dt
import EfficientFrontier
import pandas as pd
import numpy as np
def get_portfolio(request):
    if request.POST:
        stocks = request.POST['stocks']
        stocks = stocks.split(',')
        day = request.POST['days']
        alpha = request.POST['alpha']
        #risk_free_return
        bonds_return =yf.download('^TNX', start=dt.date.today()-dt.timedelta(days=365), end=dt.date.today())
        risk_free_rate = bonds_return.Close.pct_change().mean()
        #tickets_parameters
        ticket = yf.download(stocks, start=dt.date.today()-dt.timedelta(days=365), end=dt.date.today())
        returns = ticket.Close.pct_change()
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        num_portfolios = 30000
        #frontier
        EfficientFrontier.display_simulated_ef_with_random(ticket.close, mean_returns, num_portfolios,
                                                    cov_matrix, num_portfolios, risk_free_rate)

