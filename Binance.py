from BnB_Lib import *
from BnB_Search import *
# pip install openpyxl


 
def PAIR_PRINT(Pair):####################################################################################################################################################
    if Pair['Ord']=='NONE':  Order='NONE'
    else: Order=Pair['Ord']['status']+Pair['Ord']['side']+' '+ str(datetime.fromtimestamp(int(Pair['Ord']['time'])/1000).strftime('%Y.%m.%d %H:%M:%S'))
    print(TIME(),Pair['Sym'],'LastOrder:',Order)

 
#def CLOSE_ALL(Pair):####################################################################################################################################################
#    if BotMode!='CloseAll': return
#    Pair['lot']=0 

####################################################################################################################################################
choice = input('press Y to close all orders: ')
if choice.lower() == "y":
    print('Close all BuyLim orders mode')
    BotMode='CloseAll'
else: BotMode='NormalMode'
ReStartTime=0
while True:
    if time.time()-ReStartTime>600: # update PAIRS every 10min
        BnB_LIST=FULL_LIST_SCAN() # All Binance pairs list and settings
        PAIRS,SYM_LIST = BEST_PAIRS(BnB_LIST) # get best part of all pairs by parameters: Rank=Spred/Bid, Trades per 24H quantity, Trades per 5M quantity
        XLS_SAVE(PAIRS)
        print('PAIRS:',SYM_LIST)
        ReStartTime=time.time()
        round=0
    BALANCE_UPDATE(PAIRS)
    for Pair in PAIRS: 
        if round>0 and Pair['lot']==0: continue #  once set missing limit orders for 'none trading' pairs
        PAIR_PARAMS_UPDATE(Pair)
        if BotMode=='CloseAll':  Pair['lot']=0
        #PAIR_PRINT(Pair)
       
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
    round+=1
    if BotMode=='CloseAll': break # only one round to close all BuyLim orders  
    
            
            
        
         
            

      
         
    
   
    

