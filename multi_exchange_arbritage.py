import gdax
import datetime
import requests
import time


def Polo(base, quote, value):
   if base == "ETH" and quote == "BTC":
       url = "https://poloniex.com/public?command=returnTicker"
       r = requests.get(url).json()
       return round(float(r['%s_%s' % (quote, base)][value]), 5)
   else:
       return "N/A"

def Kraken(base, quote, value):
   if base == "BTC": base = "XBT"
   if quote == "BTC": quote = "XBT"
   url = "https://api.kraken.com/0/public/Ticker?pair=%s%s" % (base, quote)
   r = requests.get(url).json()
   if base in ["XBT", "ETH"]:
       base = "X" + base
   else:
       base = "Z" + base
   if quote in ["XBT", "ETH"]:
       quote = "X" + quote
   else:
       quote = "Z" + quote
   return float(r["result"]["%s%s" % (base, quote)][value][0])

def Huobi(base, quote, value):
   if base == "BTC" and quote == "USD":
       if value == "p_last":
           url = "http://api.huobi.com/usdmarket/detail_btc_json.js"
           r = requests.get(url).json()
           return float(r[value])
       else:
           url = "http://api.huobi.com/usdmarket/detail_btc_json.js"
           r = requests.get(url).json()
           return float(r[value][0]["price"])
   else:
       return "N/A"

def Gdax(base, quote, value):
   public_client = gdax.PublicClient()
   xyz = float(public_client.get_product_ticker("%s-%s" % (base, quote))[value])
   return xyz
   #return float(public_client.getProductTicker(product="%s-%s" % (base, quote))[value])

def Gatecoin(base, quote, value):
   url = "https://api.gatecoin.com/Public/LiveTicker/%s%s" % (base, quote)
   r = requests.get(url).json()
   return float(r['ticker'][value])

def ETCXBT_index_price():
    url = "https://www.bitmex.com/api/v1/instrument?symbol=.ETCXBT"
    r = requests.get(url).json()
    pi = float(r[0]["lastPrice"])
    return pi

def ETC7D_price():
    url = "https://www.bitmex.com/api/v1/instrument?symbol=ETC7D"
    r = requests.get(url).json()
    p = float(r[0]["lastPrice"])
    return p

pair = [["BTC", "USD"], ["BTC", "EUR"], ["ETH", "EUR"], ["ETH", "BTC"], ["ETH", "USD"]]


def go():
    while True:
        print(datetime.datetime.now())
        for i in pair:
            price = {}

            print("%s-%s" % (i[0], i[1]))
            price["Gatecoin"] = Gatecoin(i[0], i[1], "last")
            price["Gdax"] = Gdax(i[0], i[1], "price")
            #price["Huobi"] = Huobi(i[0], i[1], "p_last")
            #price["Kraken"] = Kraken(i[0], i[1], "c")
            price["Poloniex"] = Polo(i[0], i[1], "last")

            print(", ".join(list(price.keys())) + ", Max % Dif")
            temp = list(price.values())
            temp_ = list(filter(lambda a: a != "N/A", temp))
            temp2 = list(price.keys())
            print(', '.join(map(str, temp)) + ", %s" % str(
                round((max(temp_) - min(temp_)) / min(temp_) * 100, 2)) + " (Max: %s, Min: %s)" % (
                    temp2[temp.index(max(temp_))], temp2[temp.index(min(temp_))]))

            price["Gatecoin"] = round (100 * (Gatecoin(i[0], i[1], "ask") - Gatecoin(i[0], i[1], "bid"))/Gatecoin(i[0], i[1], "ask") , 2)
            price["Gdax"] = round(100* (Gdax(i[0], i[1], "ask") - Gdax(i[0], i[1], "bid"))/Gdax(i[0], i[1], "ask") , 2)
            """a = Huobi(i[0], i[1], "sells")
                b = Huobi(i[0], i[1], "buys")"""
               #if a != "N/A" and b != "N/A":
                   #price["Huobi"] = round (100 * (a - b)/a, 2)
               #else: price["Huobi"] = "N/A"
            #price["Kraken"] = round(100 * (Kraken(i[0], i[1], "a") - Kraken(i[0], i[1], "b"))/Kraken(i[0], i[1], "a")  , 2 )
            a = Polo(i[0], i[1], "lowestAsk")
            b = Polo(i[0], i[1], "highestBid")
            if a != "N/A" and b != "N/A":
                price["Poloniex"] = round( 100 * (a - b)/a, 2)
            else: price["Poloniex"] = "N/A"

            temp = list(price.values())
            temp_ = list(filter(lambda a: a != "N/A", temp))
            temp2 = list(price.keys())
            print("spread: " + ', '.join(map(str, temp)) + "\n")
        """pi = ETCXBT_index_price()
        p = ETC7D_price()
        premium = round((p/pi-1)*100, 2)
        print("ETC7D price: " + str(p) + " .ETCXBT price: " + str(pi) )
        print("Futures trading at " + str(premium) + "% premium"+ "\n")  """

        time.sleep(15)

       #s.enter(10, 1, do_something, (sc,))
go()
"""s = sched.scheduler(time.time, time.sleep)
s.enter(10, 1, do_something, (s,))
s.run()"""
