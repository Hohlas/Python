from BnB_lib import *

# Server limits for all pairs
local_time = int(time.time())
limits = bot.exchangeInfo()
server_time = int(limits['serverTime'])//1000
shift_seconds = server_time-local_time
bot.set_shift_seconds(shift_seconds)
 
#################################################################################################################################################################
#tickerPrice=bot.tickerPrice()           # {symbol, price}
#tickerBookTicker=bot.tickerBookTicker() # {symbol, ask, askQty, bid, bidQty}
#myTrades=bot.myTrades(symbol='ETHBTC')   # {'commission':'0.00249', 'commissionAsset':'BNB', 'id':66452331, 'orderId':160731385, 'price':'0.0807', 'qty':'0.118', 'time': 1528033783103,...}
#AllOrders=bot.allOrders(symbol='ETHBTC', limit=5) # {'orderId':XXX, 'origQty': '1.238', 'price':'0.08151900', 'side':'SELL', 'status':'NEW', 'time':1528033790389, 'symbol':'ETHBTC',...}   
#offers = bot.depth(symbol=Pair['Sym'], limit=5) # five(5,10,20) last offers from  DOM (Depth of Market) 


LimOrders=bot.openOrders()
for Ord in LimOrders: # in all current limit orders
    NeedToAdd=True 
    for Pair in PAIRS: # find symbols, not in our list 'PAIRS'
        if Ord['symbol']==Pair['Sym']: NeedToAdd=False # this symbol already in our list 'PAIRS', no need to add
    if NeedToAdd:
        PAIRS.append({'Sym':Ord['symbol'], 'lot':0}) # lot=0 i.e. must be closed without loss (breakeven)

INFO = bot.exchangeInfo()     
for Pair in PAIRS: # 
    for Inf in INFO['symbols']: # in all cells in INFO 
        if Pair['Sym']==Inf['symbol']: # find cells with the same symbols 
            Pair.update({'Ord':  []}) # create free dict for
            Pair.update({'Bal':       # further filling
                            {'Base' :   {'Free':0, 'Lock':0}, 
                             'Quote':   {'Free':0, 'Lock':0}
                         }}) 
            Pair.update({'Inf':  Inf})
            Pair.update({'Price': {'Ask':[], 'Bid':[]}})

while True:####################################################################################################################################################
    Balances=bot.account()['balances']
    for Bal in Balances:
        for Pair in PAIRS:
            if Bal['asset']==Pair['Inf']['baseAsset']:  Pair['Bal'].update({'Base':   {'Free':float(Bal['free']), 'Lock':float(Bal['locked'])}}) # update dict Pair['Bal']['Base']
            if Bal['asset']==Pair['Inf']['quoteAsset']: Pair['Bal'].update({'Quote':  {'Free':float(Bal['free']), 'Lock':float(Bal['locked'])}}) # update dict Pair['Bal']['Quote']
    for Pair in PAIRS: 
        print(datetime.fromtimestamp(int(time.time())), Pair['Sym'])
        PAIR_PARAMS_UPDATE(Pair)
        if Pair['Ord']=='NONE': # no orders yet,    Pair['Ord']['status'] = 'FILLED' | 'CANCELED' | 'NEW' 
            BUY_ORDER_SET(Pair)  # can buy
        elif Pair['Ord']['status']=='FILLED' and Pair['Ord']['side']=='SELL': # sell order has filled
            BUY_ORDER_SET(Pair)  # can buy
        elif Pair['Ord']['status']=='NEW':  # limit order.   
            if Pair['Ord']['side']=='SELL': # sell limit order
                continue  # nothing to do. Wait, until SELL order fills
            elif Pair['Ord']['side']=='BUY': # BuyLimit order 
                BUY_ORD_CHECK(Pair)
        elif Pair['Ord']['status']=='FILLED' and Pair['Ord']['side']=='BUY': # buy order has filled
            SELL_ORDER_SET(Pair)
    time.sleep(1)
        
            
            
            
        
         
            

      
         
    
   
    
