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
    commissionTotal = 0 # 
    tradeQuantity = 0 

    for i in response['fills']:
    	# change from str to float
        amount = float(i['price']) * float(i['qty'])
        commission = float(i['commission'])
        quantity = float(i['qty'])

        # tally actual realized amount
        tradeValue += (amount - commission)
        commissionTotal += commission
        tradeQuantity += quantity

    # return a dict
    return {'tradeValue': tradeValue, 'commissionTotal': commissionTotal, 'tradeQuantity': tradeQuantity}

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
		commission = 0
		i['tradeQuantity'] = 0

		if ('USD' in i['asset']) == False:
			symbol = i['asset'] + 'USDT'
			symbolInfo = client.get_symbol_info(symbol)['filters']
			maxLotSize = float(next(item for item in symbolInfo if item["filterType"] == "MARKET_LOT_SIZE")['maxQty'])

			print (('market lot size for {} is {}').format(symbol, maxLotSize))

			# execute market sell 

			# if the total quatity > maxlotSize, excute multiple sell till it's below
			while quantity > maxLotSize:
				tradeResponse = marketSell(symbol, maxLotSize)
				quantity -= maxLotSize

				# check is trade is successful 
				if isinstance(tradeResponse, dict):
					tradeResponse = getTradeInfo(tradeResponse)

					# tally trade response dict
					i['tradeValue'] += tradeResponse['tradeValue']
					commission += tradeResponse['commissionTotal']
					i['tradeQuantity'] += tradeResponse['tradeQuantity']

					print (('Trade Summary: {} of {} sold for {}').format(i['tradeQuantity'], symbol, i['tradeValue']))

				# trade failed
				else:
					print ('Market sell failed')

			# total qantity below maxlotsize, execute one sell
			else: 
				tradeResponse = marketSell(symbol, quantity)
			
				if isinstance(tradeResponse, dict):
					tradeResponse = getTradeInfo(tradeResponse)

					i['tradeValue'] += tradeResponse['tradeValue']
					commission += tradeResponse['commissionTotal']
					i['tradeQuantity'] += tradeResponse['tradeQuantity']

					print (('Trade Summary: {} of {} sold for {}').format(i['tradeQuantity'], symbol, i['tradeValue']))

				else:
					print ('Market sell failed')

		else:
			pass
 
		if i['tradeQuantity'] != 0:
			i['avgPrice'] = commission / i['tradeQuantity']
		else: 
			i['avgPrice'] = 0



# Test Order 
# 'asset': 'BTC', 'free': '0.00000065', 'locked': '0.00000000', 'USDT': True}

# quantity = 100
# tradeResponse = client.create_test_order(symbol="BTCUSDT", side="buy", type="MARKET", quantity=quantity) # should be {}


getBalances()
cashMeOutside()

for i in balances:
	print (i) 
