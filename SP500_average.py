# Script to calculate the 5, 10, 20, 30 year return averages of the new york stock
# exchange and compare to historical averages.
import yfinance as yf

def solveForRate(currentPrice, historicPrice, time):
  return ((currentPrice/historicPrice)**(1/time) - 1)*100

if __name__ == '__main__':
  gspc = yf.Ticker("^GSPC")
  currentPrice = gspc.info['regularMarketPrice']
  hist30 = gspc.history(period='30y')
  price30 = hist30['Close'][0]
  rate30 = solveForRate(currentPrice, price30, 30)
  hist20 = gspc.history(period='20y')
  price20 = hist20['Close'][0]
  rate20 = solveForRate(currentPrice, price20, 20)
  hist10 = gspc.history(period='10y')
  price10 = hist10['Close'][0]
  rate10 = solveForRate(currentPrice, price10, 10)
  hist5 = gspc.history(period='5y')
  price5 = hist5['Close'][0]
  rate5 = solveForRate(currentPrice, price5, 5)
  print('S&P 500 Average Yearly Returns')
  print('Best/Median/Worse calculated using data 1871-2012')
  print('        Worst   Median Best    Current')
  print('5yr:' + '   -15.6%   9.4%   27.0%   ' + str(round(rate5, 1))+'%')
  print('10yr:' + '  -2.1%    8.6%   19.0%   ' + str(round(rate10, 1))+'%')
  print('20yr:' + '   2.8%    8.1%   16.9%   ' + str(round(rate20, 1))+'%')
  print('30yr:' + '   4.1%    9.2%   13.8%   ' + str(round(rate30, 1)) + '%')
