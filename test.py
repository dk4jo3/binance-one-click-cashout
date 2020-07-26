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
    commissionTotal = 0 # 
    tradeQuantity = 0 

    for i in response['fills']:
        amount = float(i['price']) * float(i['qty'])
        commission = float(i['commission'])
        quantity = float(i['qty'])

        # tally actual realized amount
        tradeValue += (amount - commission)
        commissionTotal += commission
        tradeQuantity += quantity

    # total amount / qty
    # return float
    return {'tradeValue': tradeValue, 'commissionTotal': commissionTotal, 'tradeQuantity': tradeQuantity}

print (getTradeInfo(tradeResponse))