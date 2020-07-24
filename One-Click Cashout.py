from binance.client import Client 
import keys
import json

# imoprt API keys
client = Client(keys.testPublicKey, keys.testSecretKey)

balances = []


def getBalances():
	account = client.get_account()['balances']

	pairSymbols = []
	pairs = client.get_all_tickers()
	
	# Should not edit dict it self in a loop.
	for i in account: 
		if float(i['free']) > 0.001: #exclude dust, should actually get if it's > 0.0001BTC in the future.
			balances.append(i)
	
	

	# # get available pair symbols in a list
	# for i in pairs:
	# 	pairSymbols.append(i['symbol'])


	# # check is "coin +'USDT'" symbol exits and add T/F to its dict
	# for i in balances:
	# 	ticker = i['asset'] + "USDT"
	# 	if ticker in pairSymbols:
	# 		i['USDT'] = True
	# 	else:
	# 		i['USDT'] = False

	for i in balances:
		print (i)

	return balances


def getTradeInfo(response): #return tradeValue, avgPrice

    tradeValue = 0 # w/o commission
    tradeTotal = 0 # w/ commission

    for i in response['fills']:
        amount = float(i['price']) * float(i['qty'])
        commission = float(i['commission'])

        # tally actual realized amount
        tradeValue += (amount - commission)
        tradeTotal += amount

    # total amount / qty
    avgPrice = tradeTotal / float(response['origQty'])

    # return float
    return tradeValue, avgPrice

def marketSell(symbol, quantity):

	try:
		tradeResponse = client.order_market_sell(
			    symbol=symbol,
			    quantity=quantity,
			    recvWindow=60000)
		print (('{} of {} is traded').format(symbol, quantity))
		return tradeResponse 

	except Exception as e:
		print ("Error in line:", e.message)
	


def cashMeOutside():
	for i in balances: 

		# get quantity 
		quantity = round(float(i['free']), 6)
		i['tradeValue'] = 0 
		i['avgPrice'] = 0

		if ('USD' in i['asset']) == False:
			symbol = i['asset'] + 'USDT'
			symbolInfo = client.get_symbol_info(symbol)['filters']
			maxLotSize = float(next(item for item in symbolInfo if item["filterType"] == "MARKET_LOT_SIZE")['maxQty'])

			print (('market lot size for {} is {}').format(symbol, maxLotSize))

			# execute market sell 
			while quantity > maxLotSize:
				tradeResponse = marketSell(symbol, maxLotSize)
				quantity -= maxLotSize

				if isinstance(tradeResponse, dict):
					# return amount realized and avg price
					i['tradeValue'], i['avgPrice'] = getTradeInfo(tradeResponse)
					print (quantity, i['asset'], "trade to USDT for:", i['tradeValue'], "at", i['avgPrice'])
				else:
					pass
			else: 
				tradeResponse = marketSell(symbol, quantity)
			
				# catch error
				if isinstance(tradeResponse, dict):
					# return amount realized and avg price
					i['tradeValue'], i['avgPrice'] = getTradeInfo(tradeResponse)
					print (quantity, i['asset'], "trade to USDT for:", i['tradeValue'], "at", i['avgPrice'])
				else:
					pass
		else:
			pass

# Test Order 
# 'asset': 'BTC', 'free': '0.00000065', 'locked': '0.00000000', 'USDT': True}

# quantity = 100
# tradeResponse = client.create_test_order(symbol="BTCUSDT", side="buy", type="MARKET", quantity=quantity) # should be {}


getBalances()
cashMeOutside()

for i in balances:
	print (i) 
