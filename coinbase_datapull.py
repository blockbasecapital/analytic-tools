import json
import requests
import datetime

begDate = "2017-05-01"
endDate = "2017-05-10"
filename = "Coinbase-Data.txt"

start = datetime.datetime.strptime(begDate, "%Y-%m-%d")
end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

dates_rec = []

for date in date_generated:
  dates_rec.append(date.strftime("%Y-%m-%d"))

url_btc = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'
url_eth = 'https://api.coinbase.com/v2/prices/ETH-USD/spot'
url_ltc = 'https://api.coinbase.com/v2/prices/LTC-USD/spot'

file = open(filename,"w")

a = 0 # zeroth element, for indexing purpose

for i in range(0,len(dates_rec)):
  params = {'date': dates_rec[a]}
  # print(params) # uncomment for verbose mode
  res_btc = requests.get(url_btc, params=params)

  # print(dates_rec[a])
  btc = res_btc.json()
  px_btc = btc['data']['amount']

  res_eth = requests.get(url_eth, params=params)
  eth = res_eth.json()
  px_eth = eth['data']['amount']

  res_ltc = requests.get(url_ltc, params=params)
  ltc = res_ltc.json()
  px_ltc = ltc['data']['amount']

  final_string = dates_rec[a]+";"+px_btc+";"+px_eth+";"+px_ltc

  file.write(final_string + '\n')
  a = a + 1

file.close()
