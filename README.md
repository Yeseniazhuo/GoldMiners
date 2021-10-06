# GoldMiners
 
## About Gold Miners
Gold Miners (https://goldminers-port-management.herokuapp.com/) is a portfolio 
visualization and management Web Tool designed by Gold Miner group, four students from 
NUS. The target user group is individual investors who are not very professional in 
investment, but are interested in building their own stock portfolios and getting their hands 
dirty in personal portfolio exploration. As a lightweight and free web tool, Gold Miners is 
very helpful and user-friendly for portfolio quantitative analytics. With this tool, individual 
investors can make better decisions when comparing and analyzing stocks and portfolios.

## Function description
### 1. Efficient frontier
#### User Input:
##### 1) Stock tickers
Currently support US stock market. No limitation on tickers number. Split by ",".
##### 2) Number of days to predict
Refers to trading days. (> 10)
##### 3) Volatility estimation period
Previous n days
##### 4) Confidence level
i.e. 0.005
##### 5) Capital invested
i.e. 1000 ($)

#### Output Figure:
###### Simulated Efficient Frontier
X-axis is the portfolio volatility, while the y-axis is the return. 

The efficient frontier is composed of the portfolio that has the highest return given a certain standard deviation, or one with lowest risk given the same level return. The red star marks the portfolio with the highest sharpe ratio, which gives us the highest risk-adjusted return. The green star marks the portfolio minimum variance portfolio which has the lowest volatility.

### 2. Portfolio Future Predict (MC simulation)
#### Additional User Input:
##### 6) Number of simulations
i.e. 300
##### 7) Customized stock weight allocation
i.e. 0.25,0.25,0.25,0.25

#### Output Figure:
Three figures of Monte Carlo Simulation on portfolio future predict will be shown.

In Function One, the weight of minimum variance portfolio and maximum Sharpe ratio portfolio has got in hand. Therefore, the price path with Monte Carlo simulation can be simulated for many times (depend on the user input before). Users can know what is likely to happen to their portfolio, and what will be the loss in the worst case. That is the idea of Value at Risk. If the confidence level input is 5%, our program will calculate what will be the loss of your portfolio in the worst 5% case. 

The additional interesting function is that Gold Miners allow user to type in the weight for any self-designed portfolio and the Monte Carlo simulation will be generated.

Under each figure, portfolio insights and information are provided. Now we put three indicators: VaR, annualized return, and the maximum drawdown. More indicators may be updated in the future.

##### a) Minimum variance portfolio
##### b) Maximum Sharpe ratio portfolio
##### c) Self-designed portfolio

## Theory behind and developer’s idea 
The efficient frontier theory was first introduced by Harry Markowitz, and is also the cornerstone for modern portfolio theory. The data is from Yahoo Finance API, with the function updated in the future, more API will be considered to use. The developing language is Python, along with Java, Html, etc.（Source code can find in https://github.com/cheryl-mxd/GoldMiners）

The coding framework are generally similar to what was taught by professor Lee in the class but is expanded to a more integrated and functional web tool with user-friendly interface, so that users can choose whatever stocks they wish to explore, optimize their portfolio and design their own allocation with a great flexibility. As far as we know, there are not many free tools like Gold Miners for individual investors to do portfolio simulation and analytics.

For the next step, we’re also thinking about how to expand our analysis tool. For example, it would also be great if we could let the investors fill in the stocks they are interested in, let our system do the event study, and tell us what is the best time to enter the market. Also, it will be amazing if our system can cover more kinds of investing assets.