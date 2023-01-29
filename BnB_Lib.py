global PROFIT_PERCENT, HoldTime
STOCK_FEE = 0.2  # stock commission = 2 x 0.075% = 0.15%   (Using BNB to pay for fees)
PROFIT = 1 #  0.5% - 1%
HoldTime = 5 # minutes to hold open order


import time
from datetime import datetime
from BnB_Search import TIME

KeyFile="API_KEY.txt"
with open(KeyFile, "r") as myfile:
    line = myfile.readline() # Читает строку из файла
    API_SECRET=myfile.readline() # Читает строку из файла
myfile.close()
API_KEY=line.split('\n')[0] # читает строку до символов '..'
from binance_api import Binance  # API description: https://bablofil.ru/binance-api/ 
bot = Binance(API_KEY=API_KEY,  API_SECRET=API_SECRET)

def PAIR_PARAMS_UPDATE(Pair): ####################################################################################################################################
    AllOrders=bot.allOrders(symbol=Pair['Sym'], limit=5) # last 5 orders 
    LastOrder = 'NONE'
    for ord in AllOrders:  
        if ord['status']!='CANCELED': #'status' can be:  'CANCELED', 'NEW'(limit), 'FILLED'  
            LastOrder=ord        
    Pair.update({'Ord':  LastOrder}) 
    Ticker=bot.tickerBookTicker(symbol=Pair['Sym']) # {symbol, ask, askQty, bid, bidQty}
    Pair.update({'Ask':float(Ticker['askPrice'])}) 
    Pair.update({'Bid':float(Ticker['bidPrice'])})
    #if LastOrder!='NONE':
    #    LastOrder=LastOrder['type']+LastOrder['side']+' '+ str(datetime.fromtimestamp(int(LastOrder['time'])/1000).strftime('%Y.%m.%d %H:%M:%S')) #  OrdTime.strftime('%d.%m.%Y %H:%M:%S')
    #print(TIME(),Pair['Sym'],'PAIR_PARAMS_UPDATE, LastOrder:',LastOrder)

def STEP_ADAPTgg (value, step): 
   return ((int(value * 100000000) - int(value * 100000000) % int(float(step) * 100000000)) / 100000000)

def STEP_ADAPT (value, step, increase=False): ###################################################################################################################################
   return ((int(value * 100000000) - int(value * 100000000) % int(float(step) * 100000000)) / 100000000)+(float(step) if increase else 0)



def BUY_ORD_CHECK(Pair):################################################################################################################################### 
    #print(TIME(),'OrdTime=',datetime.fromtimestamp(int(Pair['Ord']['time']/1000)),' OrdAge=',int((time.time() - Pair['Ord']['time']/1000)/60),'minutes')
    if time.time() - Pair['Ord']['time']/1000 > HoldTime*60 or Pair['lot']==0: 
        if Pair['Bid']==float(Pair['Ord']['price']):
            print(Pair['Sym'],'Price still don''t change')
            return
        order = bot.cancelOrder(orderId=Pair['Ord']['orderId'], symbol=Pair['Sym'])
        print(TIME(),'Cancel BUY order for', Pair['Sym'])

def SELL_ORDER_SET(Pair):###################################################################################################################################
    #print('Try to sell',Pair['Sym'],'Order:',Pair['Ord']['status'],'.',Pair['Ord']['side'],' ',Pair['Ord']['origQty'],'x',Pair['Ord']['price'])
    amount = float(Pair['Ord']['origQty']) # order amount of base asset
    amount = float(Pair['BaseBal']['Free']) #  
    BreakevenPrice = float(Pair['Ord']['price']) * (1+STOCK_FEE/100) # price to only return money 
    BreakevenPrice = STEP_ADAPT(BreakevenPrice, Pair['filters'][0]['tickSize'], increase=True) # price of base asset, normalised to exchange requirements 'stepSize'
    BestPrice = max(BreakevenPrice, Pair['Ask']) # if the price fall, set BreakevenPrice to return money
    if amount*BestPrice<float(Pair['filters'][2]['minNotional']):
        print('Not enought',Pair['Sym'],'to sell: have',amount,'  need',float(Pair['filters'][2]['minNotional'])/BestPrice)
        return
    new_order = bot.createOrder(
        symbol=Pair['Sym'],
        recvWindow=5000,
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',  # Good Till Cancel
        quantity=amount,
        price="{price:0.{precision}f}".format(price=BestPrice, precision=Pair['baseAssetPrecision']),
        newOrderRespType='FULL')
    if 'orderId' in new_order:  print(TIME(),'Sell', amount,Pair['Sym'],'x',BestPrice,' Profit=', round((BestPrice-float(Pair['Ord']['price']))/BestPrice*100,2),'%')
    else:                       print(TIME(),'WARNING: Sell', amount,Pair['Sym'],'x',BestPrice,'ERROR:\n',str(new_order))

def BUY_ORDER_SET(Pair):###################################################################################################################################
    if Pair['QuoteBal']['Free']<float(Pair['filters'][2]['minNotional']):  return # current balance < required balance
    if Pair['lot']==0: return # need only sell current asset
    if Pair['QuoteBal']['Free'] < Pair['lot']:
        print('Not enought money: \n Need:',Pair['lot'],Pair['quoteAsset'],' Have:',Pair['QuoteBal']['Free'],Pair['quoteAsset'])
        return
    buyprice   =Pair['Bid']
    amount = STEP_ADAPT(Pair['lot']/buyprice,      Pair['filters'][1]['stepSize']) # amount of base asset to buy, normalised to exchange requirements 'stepSize'
    QuoteAmount = buyprice * amount # amount of quote Asset (BTC) for order
    # Если в итоге получается объем торгов меньше минимально разрешенного, то ругаемся и не создаем ордер
    if amount < float(Pair['filters'][1]['stepSize']):           print('counted amount',amount,Pair['baseAsset'],' < stepSize=',Pair['filters'][1]['stepSize']);        return 
    if amount < float(Pair['filters'][1]['minQty']):             print('counted amount',amount,Pair['baseAsset'],' < minQty=',Pair['filters'][1]['minQty']);            return
    if QuoteAmount < float(Pair['filters'][2]['minNotional']):   print('QuoteAmount',QuoteAmount,Pair['quoteAsset'],' < minNotional=',Pair['filters'][2]['minNotional']);return
    new_order = bot.createOrder(
                            symbol=Pair['Sym'],
                            recvWindow=5000,
                            side='BUY',
                            type='LIMIT',
                            timeInForce='GTC',  # Good Till Cancel
                            quantity=amount,
                            price="{price:0.{precision}f}".format(price=buyprice, precision=Pair['baseAssetPrecision']),
                            newOrderRespType='FULL')
    if 'orderId' in new_order:  print(TIME(),'Buy',amount,Pair['Sym'],'x', buyprice)
    else:                       print(TIME(),'WARNING: Buy',amount,Pair['Sym'],'x', buyprice,' ERROR:\n',str(new_order)); return
    # immediately set opposite sell order
    #CanSell=False
    #start_wait = int(time.time())
    #while CanSell==False: # waiting until buy order has filled
    #    PAIR_PARAMS_UPDATE(Pair)  
    #    if Pair['Ord']!='NONE' and Pair['Ord']['side']=='BUY' and Pair['Ord']['status']=='FILLED': # order must be: buy & filled 
    #        CanSell=True
    #    else: time.sleep(5)
    #    if int(time.time())-start_wait>1*60: # wait too long
    #        order = bot.cancelOrder(orderId=Pair['Ord']['orderId'], symbol=Pair['Sym'])
    #        print(TIME(),'Cancel BUY order for', Pair['Sym'])
    #        return
    #SELL_ORDER_SET(Pair)
                                               
    
     

