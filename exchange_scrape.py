# Script to scrape all candles of all stocks on the nyse and nasdaq
# and store that data in a local mysql db for later use. Requires
# having local mysql server confiugured and running. Also requires
# creating an empty database called stock_data from command line.
import os
import finnhub
import time
import mysql.connector

if __name__ == '__main__':
  # initialize variables
  key = os.getenv('FINNHUB_API_KEY')
  client = finnhub.Client(api_key=key)
  mysqlPassword = os.getenv('MYSQL_PASSWORD')
  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password=mysqlPassword,
    database='stock_data'
  )
  mycursor = mydb.cursor()

  # get a list of all stocks on nyse and nasdaq trading in USD
  data = client.stock_symbols('US', currency='USD')
  symbols = []
  for i in data:
    symbols.append(i['symbol'])

  # get data for symbols and store in local database
  counter = 0
  for symbol in symbols:
    counter += 1
    try:
      # sleep because free plan gets rate limited to 60 req/min by finnhub
      time.sleep(1)

      # request the data, use 0 and 3 billion for unix timestamps so we get all the data
      # status field will be 'no_data' or 'ok'
      candle = client.stock_candles(symbol, 'D', 0, 3000000000)

      # we only want stocks with a year plus of data
      if candle['s'] == 'ok' and len(candle['t']) > 365:
        # create new table for the stock
        mycursor.execute(f'CREATE TABLE {symbol} (timestamp INT, open FLOAT, close FLOAT, high FLOAT, low FLOAT)')
        sql = f'INSERT INTO {symbol} (timestamp, open, close, high, low) VALUES (%s, %s, %s, %s, %s)'

        # parse the data and store in table, each timestamp gets new row
        for i in range(len(candle['t'])):
          vals = (candle['t'][i], candle['o'][i], candle['c'][i], candle['h'][i], candle['l'][i])
          mycursor.execute(sql, vals)
          mydb.commit()
    except:
      print('Failed to create a table for: ' + symbol + ' - continuing.')

    print(str(counter) + '/' + str(len(symbols)))
