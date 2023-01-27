from binance_api import Binance  # https://bablofil.ru/binance-api/
bot = Binance(
    API_KEY='D7...Ejj',
    API_SECRET='gwQ...u3A'
)
print('account', bot.account())