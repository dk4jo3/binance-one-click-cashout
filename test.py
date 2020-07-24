tradeResponse = {
    "symbol": "BTCUSDT",
    "orderId": 28,
    "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
    "transactTime": 1507725176595,
    "price": "0.00000000",
    "origQty": "10.00000000",
    "executedQty": "10.00000000",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "MARKET",
    "side": "SELL",
    "fills": [
        {
            "price": "4000.00000000",
            "qty": "1.00000000",
            "commission": "4.00000000",
            "commissionAsset": "USDT"
        },
        {
            "price": "3999.00000000",
            "qty": "5.00000000",
            "commission": "19.99500000",
            "commissionAsset": "USDT"
        },
        {
            "price": "3998.00000000",
            "qty": "2.00000000",
            "commission": "7.99600000",
            "commissionAsset": "USDT"
        },
        {
            "price": "3997.00000000",
            "qty": "1.00000000",
            "commission": "3.99700000",
            "commissionAsset": "USDT"
        },
        {
            "price": "3995.00000000",
            "qty": "1.00000000",
            "commission": "3.99500000",
            "commissionAsset": "USDT"
        }
    ]
}

balances = { 'asset': 'BTC', 'free': '0.00000065', 'locked': '0.00000000', 'USDT': True}

def getTradeInfo(response):

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

maxLotSize = 200
quantity = 1999

while quantity > maxLotSize:
    quantity -= maxLotSize
    print (('quantity {} is bigger than maxLotSize {}').format(quantity, maxLotSize))
else: 
    print (('quantity {} is smaller than maxLotSize {}').format(quantity, maxLotSize))


