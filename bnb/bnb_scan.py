"""
    429 ответ сервера - слишком частые запросы. Если игнорировать этот ответ, вас забанят по IP на срок от 2 минут до 3 дней.
"""
# pip install openpyxl
#import openpyxl
#wb = openpyxl.load_workbook('./test.xlsx') # Load in the workbook
#print(wb.get_sheet_names())  # Get sheet names
#sheet = wb['Лист1'] # Get a sheet by name 
#sheet['A1'].value # Retrieve the value of a certain cell
#val = sheet['A1'].value#считываем значение определенной ячейки
#print(val)
#ws = wb.active
#ws['A1'] = "Hello blablacode!"
#wb.save('./test.xlsx')






from binance_api import Binance 
bot = Binance(
    API_KEY='e5o0y2slDIYTLtwRaZWIfoQisUw2SdCXc1mSCtrm40UpDPQBVY5riTLJ8M408bbs',
    API_SECRET='nuzghbHr6kEBZXXzdPqgdABa2FvFCx6qMfjdT4IE902clKxlfEjY4JbgUARZvHXG'
    )
SYM='BNBBTC'
INFO = 'ddd'
# INFO = bot.exchangeInfo()                 # Настройки и лимиты биржи - /api/v1/exchangeInfo
# INFO - bot.depth(symbol=SYM,limit=5)      # Открытые ордера (книгa ордеров), limit - кол-во возвращаемых записей от 5 до 1000 
# INFO = bot.trades(symbol=SYM,limit=1)     # Последние (чужие) сделки - /api/v1/trades
# INFO = bot.klines(symbol=SYM, interval='5m', limit=1) # Данные по свечам, limit – кол-во свечей (максимум 500, по умолчанию 500)
# INFO = bot.aggTrades(symbol=SYM, limit=1) # Сжатая история сделок - /api/v1/aggTrades     
# INFO = bot.tickerPrice(symbol=SYM)        # Последняя цена по паре (или парам) 
# INFO = bot.tickerBookTicker(symbol=SYM)   # Лучшие цены покупки/продажи - /api/v3/ticker/bookTicker
INFO = bot.ticker24hr()         # Статистика за 24 часа -  /api/v1/ticker/24hr   Если symbol не указан, возвращаются данные по всем парам

print(INFO)
#temp={'askPrice': '0.00187890',
#      'askQty': '27.00000000', 
#      'bidPrice': '0.00187620', 
#      'bidQty': '15.01000000', 
#      'closeTime': 1527857716908, 
#      'count': 95211, 
#      'firstId': 20224755, 
#      'highPrice': '0.00193400', 
#      'lastId': 20319965, 
#      'lastPrice': '0.00187910', 
#      'lastQty': '12.69000000', 
#      'lowPrice': '0.00181000', 
#      'openPrice': '0.00183000', 
#      'openTime': 1527771316908}     
 
