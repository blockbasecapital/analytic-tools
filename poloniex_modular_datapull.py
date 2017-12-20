import requests
import json

# Constants: look at www.epochconverter.com for unix time convention
# period = 86400 (this is the number of seconds in a day)
# Epoch timestamp: 1483228800
# Timestamp in milliseconds: 1483228800000,
# Human time (GMT): Sun, 01 Jan 2017 00:00:00 GMT
startTime = '1483228800'
endTime = '1483401600'
periodSec = '86400'
fileName = "PRIME_Rebalance.txt"
base_url = 'https://poloniex.com/public'

#Create an array of your index members vs BTC
c10_symbol = [
'BTC_ETH',
'BTC_BCH',
'BTC_LTC',
'BTC_XMR',
'BTC_ETC',
'BTC_DASH',
'BTC_MAID',
'BTC_REP',
'BTC_STEEM']

currency_data = {}
header =''

for j in range(0,len(c10_symbol)):
  params = {'command':'returnChartData','currencyPair':c10_symbol[j],'start':startTime,'end':endTime,'period':periodSec}
  currency_name = str(c10_symbol[j])
  res = requests.get(base_url, params=params)
  res_str = res.content
  res_json = json.loads(res_str)
  g = str(c10_symbol[j])
  header = header+g+';'

  # get the data for the individual dates
  date_data={}
  for i in range(0,len(res_json)):
    date_data[i]=str(res_json[i]['close'])

  currency_data[currency_name]=date_data


s1 = currency_data[c10_symbol[0]]
s2 = currency_data[c10_symbol[1]]
s3 = currency_data[c10_symbol[2]]
s4 = currency_data[c10_symbol[3]]
s5 = currency_data[c10_symbol[4]]
s6 = currency_data[c10_symbol[5]]
s7 = currency_data[c10_symbol[6]]
s8 = currency_data[c10_symbol[7]]
s9 = currency_data[c10_symbol[8]]



file = open(fileName,"w")
file.write(header)
file.write('\n')

for l in range(0,len(s1)):
  inp_val = s1[l]+';'+s2[l]+';'+s3[l]+';'+s4[l]+';'+s5[l]+';'+s6[l]+';'+s7[l]+';'+s8[l]+';'+s9[l]
  file.write(inp_val)
  file.write('\n')

file.close()
