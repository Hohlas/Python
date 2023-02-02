import xlwt # Import `xlwt`         pip install xlwt
book = xlwt.Workbook()  # create xls file
book = xlwt.Workbook(encoding="utf-8")# Initialize a workbook
sheet1 = book.add_sheet("Sorted")  # Add a sheet to the workbook
sheet2 = book.add_sheet("Full_List")  # Add a sheet to the workbook  

FileName="API_KEY.txt"
with open(FileName, "r") as myfile:
    line = myfile.readline() # Читает строку из файла
    API_SECRET=myfile.readline() # Читает строку из файла
myfile.close()
API_KEY=line.split('\n')[0] # читает строку до символов '..'

from binance_api import Binance 
bot = Binance(
    API_KEY=API_KEY,
    API_SECRET=API_SECRET
    )
# INFO = bot.exchangeInfo()                 # Настройки и лимиты биржи - /api/v1/exchangeInfo
# INFO - bot.depth(symbol=SYM,limit=5)      # Открытые ордера (книгa ордеров), limit - кол-во возвращаемых записей от 5 до 1000 
# INFO = bot.trades(symbol=SYM,limit=1)     # Последние (чужие) сделки - /api/v1/trades
# INFO = bot.klines(symbol=SYM, interval='5m', limit=10) # Данные по свечам, limit – кол-во свечей (максимум 500, по умолчанию 500)
        # 1499040000000,      // Время открытия
        # "0.01634790",       // Цена открытия (Open)
        # "0.80000000",       // Максимальная цена (High)
        # "0.01575800",       // Минимальная цена (Low)
        # "0.01577100",       // Цена закрытия (Close)
        # "148976.11427815",  // Объем
        # 1499644799999,      // Время закрытия
        # "2434.19055334",    // Объем квотируемой валюты
        # 308,                // Кол-во сделок
        # "1756.87402397",    // Taker buy base asset volume
        # "28.46694368",      // Taker buy quote asset volume
        # "17928899.62484339" // Ignore
# INFO = bot.aggTrades(symbol=SYM, limit=1) # Сжатая история сделок - /api/v1/aggTrades     
# INFO = bot.tickerPrice(symbol=SYM)1        # Последняя цена по паре (или парам) 
# INFO = bot.tickerBookTicker(symbol=SYM)   # Лучшие цены покупки/продажи - - "symbol": "LTCBTC",  "bidPrice": "41",  "bidQty": "431",  "askPrice": "42",  "askQty": 9"
PAIRS = bot.ticker24hr()         # Статистика за 24 часа -  /api/v1/ticker/24hr   Если symbol не указан, возвращаются данные по всем парам

row=0; col=0    # столбцы; строки
for cell in PAIRS:
    row=0 # c нулевого стобца файла 
    for key in cell: # читаем всю строку словаря 
        #if key=='is_visible':           continue # ненужные столбцы 
        #if key=='margin_enabled':       continue # не пишем
        #if key=='deposit_frozen':       continue
        #if key=='withdrawal_frozen':    continue
        if col==0: # в нулевой строке 
            sheet2.write(col,row, key)#  пишем название (ключ)
        else:  # в остальных ниже
            sheet2.write(col,row, cell[key]) # значение ключа
        row+=1
    col+=1 
print('sheet2 created OK')

for i in range(len(PAIRS)): # разбиваем список словарей на словари
    ask=float(PAIRS[i]['askPrice'])
    bid=float(PAIRS[i]['bidPrice'])
    spred=ask-bid
    vol=float(PAIRS[i]['quoteVolume']) # Объем торгов квотируемой валюты (BTC)
    rank=int(spred/bid*vol)

    PAIRS[i].update({'SPRED':spred})    # добавляем новые
    PAIRS[i].update({'SPRED/BID':spred/bid})# значения к 
    PAIRS[i].update({'RANK':rank})     # нашему словарю
    PAIRS[i].update({'VOL': int(vol/1000)})
   
Sorted_List=sorted(PAIRS, key= lambda d: d['RANK'], reverse=True)   # сортировка списка словарей по убыванию 'RANK'
NewRows=['symbol', 'priceChangePercent', 'highPrice', 'lowPrice', 'weightedAvgPrice', 'bidPrice', 'askPrice', 'VOL', 'SPRED','SPRED/BID', 'RANK']  # перечень нужных столбцов 

for i in range(len(NewRows)):
    key=NewRows[i] # название столбца
    row=i # столбцы
    col=0 # строки
    sheet1.write(col,row, key) # пишем название столбца
    for j in Sorted_List:
        col+=1
        sheet1.write(col,row, j[key]) # заполняем все строки столбца

book.save("BnB_Pairs.xls")# Save the workbook
   
 
