global PROFIT_PERCENT, HoldTime
STOCK_FEE = 0.001  # stock commission = 2 x 0.05% = 0.001  Using BNB to pay for fees（50% discount）= 0.05%
REQUIRED_PROFIT = 0.01 #  1%
PROFIT_PERCENT = (1+REQUIRED_PROFIT) * (1+STOCK_FEE)
HoldTime = 5 # minutes to hold open order

PAIRS = [
        {'Sym':'CNDBTC', 'lot':0.0012},
        {'Sym':'MFTBTC', 'lot':0.0012},
        {'Sym':'QKCBTC', 'lot':0.0012}  
        ]

import time
from datetime import datetime
from binance_api import Binance  # API description: https://bablofil.ru/binance-api/ 

FileName="API_KEY.txt"
with open(FileName, "r") as myfile:
    line = myfile.readline() # Читает строку из файла
    API_SECRET=myfile.readline() # Читает строку из файла
myfile.close()
API_KEY=line.split('\n')[0] # читает строку до символов '..'
 
bot = Binance(API_KEY=API_KEY,  API_SECRET=API_SECRET)


def PAIR_PARAMS_UPDATE(Pair): ####################################################################################################################################
    AllOrders=bot.allOrders(symbol=Pair['Sym'], limit=5) # last 5 orders 
    LastOrder = 'NONE'
    for ord in AllOrders:  
        if ord['status']!='CANCELED': #'status' can be:  'CANCELED', 'NEW'(limit), 'FILLED'  
            LastOrder=ord        
    Pair.update({'Ord':  LastOrder}) 
    Ticker=bot.tickerBookTicker(symbol=Pair['Sym']) # {symbol, ask, askQty, bid, bidQty}
    Pair.update({'Price': {'Ask':float(Ticker['askPrice']), 'Bid':float(Ticker['bidPrice'])}})

def STEP_ADAPT (value, step): ###################################################################################################################################
   return ((int(value * 100000000) - int(value * 100000000) % int(float(step) * 100000000)) / 100000000)

def BUY_ORD_CHECK(Pair):################################################################################################################################### 
    print('OrdTime=',datetime.fromtimestamp(int(Pair['Ord']['time']/1000)),' OrdAge=',int((time.time() - Pair['Ord']['time']/1000)/60))
    if time.time() - Pair['Ord']['time']/1000 > HoldTime*60: 
        order = bot.cancelOrder(orderId=Pair['Ord']['orderId'], symbol=Pair['Sym'])
        print('Cancel BUY order for', Pair['Sym'],order)

def SELL_ORDER_SET(Pair):###################################################################################################################################
    amount = float(Pair['Ord']['origQty']) # order price in base asset (ETH)
    ProfitPrice = float(Pair['Ord']['price']) * PROFIT_PERCENT # price counted by RequiredProfit and StockFee
    ProfitPrice = STEP_ADAPT(ProfitPrice, Pair['Inf']['filters'][0]['tickSize']) # price of base asset, normalised to exchange requirements 'stepSize'
    BestPrice = max(ProfitPrice, Pair['Price']['Ask'])
    new_order = bot.createOrder(
        symbol=Pair['Sym'],
        recvWindow=5000,
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',  # Good Till Cancel
        quantity=amount,
        price="{price:0.{precision}f}".format(price=BestPrice, precision=Pair['Inf']['baseAssetPrecision']),
        newOrderRespType='FULL')
    if 'orderId' in new_order:  print('New SellOrder created:',Pair['Sym'], amount, BestPrice)
    else:                       print('BuyOrder set ERROR:',str(new_order))

def BUY_ORDER_SET(Pair):###################################################################################################################################
    if Pair['Bal']['Quote']['Free']<float(Pair['Inf']['filters'][2]['minNotional']):  return # current balance < required balance
    if Pair['lot']==0: return # need only sell current asset
    if Pair['Bal']['Quote']['Free'] < Pair['lot']:
        print('Not enought money: \n Need:',Pair['lot'],Pair['Inf']['quoteAsset'],' Have:',Pair['Bal']['Quote']['Free'],Pair['Inf']['quoteAsset'])
        return
    buyprice   =Pair['Price']['Bid']
    amount = STEP_ADAPT(Pair['lot']/buyprice,      Pair['Inf']['filters'][1]['stepSize']) # amount of base asset to buy, normalised to exchange requirements 'stepSize'
    QuoteAmount = buyprice * amount # amount of quote Asset (BTC) for order
    # Если в итоге получается объем торгов меньше минимально разрешенного, то ругаемся и не создаем ордер
    if amount < float(Pair['Inf']['filters'][1]['stepSize']):           print('counted amount',amount,Pair['Inf']['baseAsset'],' < stepSize=',Pair['Inf']['filters'][1]['stepSize']);        return 
    if amount < float(Pair['Inf']['filters'][1]['minQty']):             print('counted amount',amount,Pair['Inf']['baseAsset'],' < minQty=',Pair['Inf']['filters'][1]['minQty']);            return
    if QuoteAmount < float(Pair['Inf']['filters'][2]['minNotional']):   print('QuoteAmount',QuoteAmount,Pair['Inf']['quoteAsset'],' < minNotional=',Pair['Inf']['filters'][2]['minNotional']);return
    print('price=',buyprice,'amount=',amount)
    #new_order = bot.testOrder(
    new_order = bot.createOrder(
                            symbol=Pair['Sym'],
                            recvWindow=5000,
                            side='BUY',
                            type='LIMIT',
                            timeInForce='GTC',  # Good Till Cancel
                            quantity=amount,
                            price="{price:0.{precision}f}".format(price=buyprice, precision=Pair['Inf']['baseAssetPrecision']),
                            newOrderRespType='FULL')
    if 'orderId' in new_order:  print('New BuyOrder created:',Pair['Sym'],amount, buyprice)
    else:                       print('BuyOrder set ERROR:\n',str(new_order)); return
    CanSell=False
    start_wait = int(time.time())
    while CanSell==False: # waiting until buy order has filled
        PAIR_PARAMS_UPDATE(Pair)  
        if Pair['Ord']!='NONE' and Pair['Ord']['side']=='BUY' and Pair['Ord']['status']=='FILLED': # order must be: buy & filled 
            CanSell=True
        else: time.sleep(1)
        if int(time.time())-start_wait>1*60: # wait too long
            order = bot.cancelOrder(orderId=Pair['Ord']['orderId'], symbol=Pair['Sym'])
            print('Cancel BUY order for', Pair['Sym'],order)
            return
    SELL_ORDER_SET(Pair)
                                               
    
     

